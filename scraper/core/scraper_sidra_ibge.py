# backend/scraping/scraper_sidra_ibge.py

import requests
import time
import json
import re

from pathlib import Path
from tqdm import tqdm
from typing import Any, Dict, List, Tuple, Optional

from utils.logger import get_logger

logger = get_logger(__name__)

# Caminhos
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).parent / "config" / "sidra_queries.json"
RAW_PATH = BASE_DIR / "data" / "raw" / "city_data_sidra.json"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "city_data_sidra.json"
REQUEST_DELAY = 1.5


def carregar_sidra_queries() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data: Any = json.load(f)
        return data if isinstance(data, dict) else {}


def carregar_municipios_processados() -> Dict[str, Any]:
    if RAW_PATH.exists():
        with open(RAW_PATH, "r", encoding="utf-8") as f:
            data: Any = json.load(f)
            return data if isinstance(data, dict) else {}
    return {}


def get_dado_sidra(
    tabela: str,
    variavel: str,
    codigo_municipio: int,
    tentativas: int = 3,
    espera: float = 2.0,
) -> Tuple[str, int, int]:
    url = f"https://apisidra.ibge.gov.br/values/t/{tabela}/n6/{codigo_municipio}/v/{variavel}/p/last"
    for tentativa in range(tentativas):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if (
                    len(data) > 1
                    and "V" in data[1]
                    and "D3N" in data[1]
                    and "D1N" in data[1]
                ):
                    valor = data[1]["V"].replace(".", "")
                    ano = data[1]["D3N"]
                    nome_cidade = data[1]["D1N"]
                    return nome_cidade, int(valor), int(ano)
            time.sleep(espera)
        except Exception as e:
            logger.error(
                f"Erro ao buscar {tabela}/{variavel} para {codigo_municipio}: {e}"
            )
    raise RuntimeError(f"Falha persistente no código {codigo_municipio}")


def coletar_dados_municipio(
    codigo_ibge: int,
    queries: Dict[str, Any],
) -> Tuple[Optional[str], Dict[str, Any]]:
    city_data: Dict[str, Any] = {"codigo_ibge": codigo_ibge}
    nome_cidade_padrao: Optional[str] = None

    for chave, config in queries.items():
        nome_cidade, valor, ano = get_dado_sidra(
            config["tabela"], config["variavel"], codigo_ibge
        )
        city_data[chave] = {"valor": valor, "ano": ano}
        if nome_cidade_padrao is None:
            nome_cidade_padrao = nome_cidade
        time.sleep(REQUEST_DELAY)

    return nome_cidade_padrao, city_data


def salvar_json_incremental(cidade: str, dados: Dict[str, Any]) -> None:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    all_data = carregar_municipios_processados()
    all_data[cidade] = dados
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    logger.info(f"💾 Dados salvos para cidade: {cidade}")


def carregar_lista_municipios() -> List[int]:
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    resp = requests.get(url, timeout=10)
    return [m["id"] for m in resp.json()] if resp.status_code == 200 else []


def corrigir_e_salvar_json() -> None:
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        dados_raw: Any = json.load(f)

    logger.info(f"📄 JSON bruto carregado de: {RAW_PATH} ({len(dados_raw)} registros)")

    dados_corrigidos: Dict[str, Any] = {}
    for nome, info in dados_raw.items():
        nome_corrigido = re.sub(
            r"\s*\(População residente estimada\)$", "", nome
        ).strip()
        dados_corrigidos[nome_corrigido] = info

    agrupado: Dict[str, Dict[str, Any]] = {}
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
        uf: dict(sorted(cidades.items())) for uf, cidades in sorted(agrupado.items())
    }

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(agrupado_ordenado, f, ensure_ascii=False, indent=4)

    logger.info(f"✅ JSON final salvo em: {PROCESSED_PATH}")
    if erros > 0:
        logger.warning(f"⚠️ {erros} cidades ignoradas por nome mal formatado.")


def run() -> None:
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
            # evita passar None para a função
            if cidade_nome is None:
                logger.warning(
                    f"⚠️ Nome da cidade não identificado para {codigo_ibge}. Pulando."
                )
                continue
            salvar_json_incremental(cidade_nome, dados)
        except Exception as e:
            logger.critical(f"❌ ERRO em {codigo_ibge}: {e}")
            break

    logger.info("🧹 Executando limpeza e organização final...")
    corrigir_e_salvar_json()


if __name__ == "__main__":
    run()
