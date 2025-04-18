# backend/core/router/interpreter.py
from core.router.semantic_router import classificar_tema
from core.router.semantic_city import detectar_cidades

from core.agents.educacao_agent import EducacaoAgent
from core.agents.populacao_agent import PopulacaoAgent
from core.agents.economia_agent import EconomiaAgent
from core.agents.institucional_agent import InstitucionalAgent
from core.agents.comparative_agent import ComparativeAgent

from utils.logger import get_logger

logger = get_logger(__name__)

# Mapeamento direto tema → classe
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

    logger.info(f"🔍 Interpretando pergunta recebida:")
    logger.info(pergunta)

    # Classificação de tema
    try:
        tema = classificar_tema(pergunta)
    except Exception as e:
        logger.error(f"❌ Erro ao classificar tema: {e}")
        tema = "desconhecido"

    # Detecção de cidades
    try:
        cidades = detectar_cidades(pergunta, max_cidades=10)
    except Exception as e:
        logger.error(f"❌ Erro ao detectar cidades: {e}")
        cidades = []

    # Seleção do agente com base no tema
    if tema in AGENTS:
        agente_classe = AGENTS[tema]
        logger.info(f"🤖 Tema identificado: {tema} | Agente selecionado: {agente_classe.__name__}")
        return agente_classe(), tema, cidades

    # Fallback semântico
    logger.warning(f"⚠️ Tema '{tema}' não corresponde a nenhum agente estruturado. Usando InstitucionalAgent.")
    return InstitucionalAgent(), "institucional", cidades
