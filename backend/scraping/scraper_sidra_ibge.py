# backend/scraping/scraper_sidra_ibge.py
import requests
import time
import json
import re

from pathlib import Path
from tqdm import tqdm

from utils.logger import get_logger

logger = get_logger(__name__)

# Caminhos
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).parent / "config" / "sidra_queries.json"
RAW_PATH = BASE_DIR / "data" / "raw" / "city_data_sidra.json"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "city_data_sidra.json"
REQUEST_DELAY = 1.5

# Carrega config
def carregar_sidra_queries():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Carrega dados já processados
def carregar_municipios_processados():
    if RAW_PATH.exists():
        with open(RAW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Consulta à API do SIDRA
def get_dado_sidra(tabela, variavel, codigo_municipio, tentativas=3, espera=2):
    url = f"https://apisidra.ibge.gov.br/values/t/{tabela}/n6/{codigo_municipio}/v/{variavel}/p/last"
    for tentativa in range(tentativas):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) > 1 and "V" in data[1] and "D3N" in data[1] and "D1N" in data[1]:
                    valor = data[1]["V"].replace(".", "")
                    ano = data[1]["D3N"]
                    nome_cidade = data[1]["D1N"]
                    return nome_cidade, int(valor), int(ano)
            time.sleep(espera)
        except Exception as e:
            logger.error(f"Erro ao buscar {tabela}/{variavel} para {codigo_municipio}: {e}")
    raise RuntimeError(f"Falha persistente no código {codigo_municipio}")

# Extrai dados de um município
def coletar_dados_municipio(codigo_ibge, queries):
    city_data = {"codigo_ibge": codigo_ibge}
    nome_cidade_padrao = None
    for chave, config in queries.items():
        nome_cidade, valor, ano = get_dado_sidra(config["tabela"], config["variavel"], codigo_ibge)
        city_data[chave] = {
            "valor": valor,
            "ano": ano
        }
        if not nome_cidade_padrao:
            nome_cidade_padrao = nome_cidade
        time.sleep(REQUEST_DELAY)
    return nome_cidade_padrao, city_data

def salvar_json_incremental(cidade, dados):
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    all_data = carregar_municipios_processados()
    all_data[cidade] = dados
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    logger.info(f"💾 Dados salvos para cidade: {cidade}")

# Lista de municípios
def carregar_lista_municipios():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    resp = requests.get(url, timeout=10)
    return [m["id"] for m in resp.json()] if resp.status_code == 200 else []

# Pós-processamento: corrigir nomes e organizar por UF
def corrigir_e_salvar_json():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        dados_raw = json.load(f)

    logger.info(f"📄 JSON bruto carregado de: {RAW_PATH} ({len(dados_raw)} registros)")

    dados_corrigidos = {}
    for nome, info in dados_raw.items():
        nome_corrigido = re.sub(r"\s*\(População residente estimada\)$", "", nome).strip()
        dados_corrigidos[nome_corrigido] = info

    agrupado = {}
    erros = 0
    for nome_completo, conteudo in dados_corrigidos.items():
        match = re.match(r"^(.*) \((\w{2})\)$", nome_completo)
        if not match:
            logger.warning(f"⚠️ Nome inválido (sem UF): {nome_completo}")
            erros += 1
            continue
        nome_cidade, uf = match.groups()
        agrupado.setdefault(uf, {})[nome_cidade] = conteudo

    agrupado_ordenado = {
        uf: dict(sorted(cidades.items()))
        for uf, cidades in sorted(agrupado.items())
    }

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(agrupado_ordenado, f, ensure_ascii=False, indent=4)

    logger.info(f"✅ JSON final salvo em: {PROCESSED_PATH}")
    if erros > 0:
        logger.warning(f"⚠️ {erros} cidades ignoradas por nome mal formatado.")

# Execução principal
def run():
    queries = carregar_sidra_queries()
    dados_existentes = carregar_municipios_processados()
    cidades_prontas = set(dados_existentes.keys())
    municipios = carregar_lista_municipios()

    logger.info(f"🚀 Iniciando coleta SIDRA para {len(municipios)} municípios")

    for codigo_ibge in tqdm(municipios, desc="🔄 Coletando cidades"):
        if any(str(codigo_ibge) in c for c in cidades_prontas):
            continue
        try:
            cidade_nome, dados = coletar_dados_municipio(codigo_ibge, queries)
            salvar_json_incremental(cidade_nome, dados)
        except Exception as e:
            logger.critical(f"❌ ERRO em {codigo_ibge}: {e}")
            break

    logger.info("🧹 Executando limpeza e organização final...")
    corrigir_e_salvar_json()

if __name__ == "__main__":
    run()
