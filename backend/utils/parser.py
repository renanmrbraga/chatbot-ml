# ✅ utils/parser.py
import unicodedata
import re
from functools import lru_cache
from rapidfuzz import fuzz

@lru_cache(maxsize=64)
def normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode("ascii").strip()

def extrair_nome_uf(cidade_info):
    """
    Extrai o nome da cidade e a UF de uma estrutura dict ou list[dict].
    Retorna (None, None) se não for possível extrair.
    """
    if isinstance(cidade_info, list) and cidade_info:
        return cidade_info[0].get("nome"), cidade_info[0].get("uf")
    elif isinstance(cidade_info, dict):
        return cidade_info.get("nome"), cidade_info.get("uf")
    return None, None

def extrair_cidades_uf(cidade_info):
    """
    Extrai lista de nomes de cidades e a UF principal (com maior população se possível).
    """
    cidades = []
    uf = None

    if isinstance(cidade_info, dict):
        cidades = [cidade_info.get("nome")]
        uf = cidade_info.get("uf")
    elif isinstance(cidade_info, list) and cidade_info:
        cidades = [c.get("nome") for c in cidade_info if "nome" in c]
        if all(isinstance(c, dict) for c in cidade_info):
            uf = max(cidade_info, key=lambda c: c.get("populacao", 0)).get("uf")

    return cidades, uf

def extrair_cidades_explicitamente(texto: str, cidades_index: dict, max_cidades: int = 10) -> list[dict]:
    texto_norm = normalizar(texto)
    encontradas = []

    for nome, dados in cidades_index.items():
        nome_norm = normalizar(nome)
        padrao = rf"\b{re.escape(nome_norm)}\b"

        if re.search(padrao, texto_norm) or fuzz.partial_ratio(nome_norm, texto_norm) >= 90:
            if dados not in encontradas:
                encontradas.append(dados)

        if len(encontradas) >= max_cidades:
            break

    return encontradas

def formatar_historico_mensagens(mensagens: list[dict]) -> list[str]:
    """
    Formata o histórico bruto do Mongo em uma lista de strings legíveis.
    """
    return [
        f"Usuário: {msg.get('pergunta')}\nResposta ({msg.get('agente', 'LLM')}): {msg.get('resposta')}"
        for msg in mensagens
    ]
