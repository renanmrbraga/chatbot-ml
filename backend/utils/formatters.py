# utils/formatters.py
NOMES_AGENTES = {
    "EducacaoAgent": "Educação",
    "ComparativeAgent": "Dashboard Comparativo",
    "PopulacaoAgent": "População",
    "EconomiaAgent": "Economia",
    "InstitucionalAgent": "Institucional",
    "LLM": "LLM (Fallback)",
}

def nome_agente_formatado(agente) -> str:
    """
    Retorna o nome amigável do agente com base no mapeamento.
    """
    if isinstance(agente, str):
        return NOMES_AGENTES.get(agente, "LLM (Fallback)")
    if agente is None:
        return NOMES_AGENTES.get("None", "LLM (Fallback)")
    return NOMES_AGENTES.get(agente.__class__.__name__, agente.__class__.__name__)

def formatar_contexto_para_llm(documentos: list[str], metadatas: list[dict]) -> tuple[str, list[str]]:
    contexto = "\n---\n".join(documentos)
    fontes = list(set(meta.get("arquivo", "Desconhecido") for meta in metadatas))
    return contexto, fontes
