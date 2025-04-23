# utils/formatters.py
from typing import Any, Optional, Dict, List, Tuple, Union, cast

from config.dicionarios import NOMES_AGENTES


def nome_agente_formatado(agente: Optional[Union[str, Any]]) -> str:
    """
    Retorna o nome amigável do agente para exibição.
    """
    if isinstance(agente, str):
        return cast(str, NOMES_AGENTES.get(agente, "LLM (Fallback)"))

    if agente is None:
        return cast(str, NOMES_AGENTES.get("None", "LLM (Fallback)"))

    classe_nome: str = agente.__class__.__name__
    return cast(str, NOMES_AGENTES.get(classe_nome, classe_nome))


def formatar_contexto_para_llm(
    documentos: List[str], metadatas: List[Dict[str, Any]]
) -> Tuple[str, List[str]]:
    """
    Junta os documentos (separados por '---') e retorna também as fontes únicas.
    """
    contexto: str = "\n---\n".join(documentos)
    fontes_set: set[str] = set()
    for meta in metadatas:
        arquivo: Any = meta.get("arquivo", "Desconhecido")
        fontes_set.add(str(arquivo))
    fontes: List[str] = list(fontes_set)
    return contexto, fontes


def formatar_dados(dados: Union[List[Dict[str, Any]], Dict[str, Any]]) -> str:
    """
    Converte lista de dicionários ou dicionário único em tabela markdown-like.
    """
    if not dados:
        return "Nenhum dado disponível."

    if isinstance(dados, dict) and "context" in dados:
        return str(dados["context"])

    if isinstance(dados, dict):
        dados_lista: List[Dict[str, Any]] = [dados]
    else:
        dados_lista = dados

    if not dados_lista or not isinstance(dados_lista[0], dict):
        return "Nenhum dado disponível."

    colunas: List[str] = [str(col) for col in dados_lista[0].keys()]
    linhas: List[List[str]] = [colunas] + [
        [str(linha.get(col, "")) for col in colunas] for linha in dados_lista
    ]

    header: str = " | ".join(colunas)
    separador: str = " | ".join(["---"] * len(colunas))
    corpo: str = "\n".join(" | ".join(linha) for linha in linhas[1:])

    return f"{header}\n{separador}\n{corpo}"
