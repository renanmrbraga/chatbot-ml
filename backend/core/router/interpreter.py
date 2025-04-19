# backend/core/router/interpreter.py
from core.agents.educacao_agent import EducacaoAgent
from core.agents.populacao_agent import PopulacaoAgent
from core.agents.economia_agent import EconomiaAgent
from core.agents.institucional_agent import InstitucionalAgent
from core.agents.comparative_agent import ComparativeAgent

from core.router.semantic_router import classificar_tema
from core.router.semantic_city import detectar_cidades
from utils.logger import get_logger

logger = get_logger(__name__)

AGENTS = {
    "educacao": EducacaoAgent,
    "populacao": PopulacaoAgent,
    "economia": EconomiaAgent,
    "dashboard": ComparativeAgent,
}

def interpretar_pergunta(pergunta: str):
    if not pergunta or not pergunta.strip():
        logger.warning("⚠️ Pergunta vazia ou inválida recebida.")
        return InstitucionalAgent(), "institucional", []

    logger.info("🔍 Interpretando pergunta recebida:")
    logger.info(pergunta)

    try:
        tema = classificar_tema(pergunta)
    except Exception as e:
        logger.error(f"❌ Erro ao classificar tema: {e}")
        tema = "desconhecido"

    try:
        cidades = detectar_cidades(pergunta, max_cidades=10)
    except Exception as e:
        logger.error(f"❌ Erro ao detectar cidades: {e}")
        cidades = []

    if tema in AGENTS:
        agente_classe = AGENTS[tema]
        logger.info(f"🤖 Tema identificado: {tema} | Agente selecionado: {agente_classe.__name__}")
        return agente_classe(), tema, cidades

    logger.warning(f"⚠️ Tema '{tema}' não corresponde a nenhum agente estruturado. Usando InstitucionalAgent.")
    return InstitucionalAgent(), "institucional", cidades
