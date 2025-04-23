# core/router/interpreter.py
from __future__ import annotations

from typing import Tuple, Type, Union, Any, Dict, List, Protocol, runtime_checkable
from core.agents.institucional_agent import InstitucionalAgent
from core.router.semantic_router import classificar_tema
from core.router.semantic_city import detectar_cidades
from config.dicionarios import get_agents_disponiveis
from utils.logger import get_logger

logger = get_logger(__name__)

AGENTS_DISPONIVEIS = get_agents_disponiveis()


@runtime_checkable
class AgentType(Protocol):
    def get_dados(
        self, pergunta: str, cidades_detectadas: List[Dict[str, Any]]
    ) -> Dict[str, Any]: ...


def interpretar_pergunta(pergunta: str) -> Tuple[AgentType, str, List[Dict[str, Any]]]:
    if not pergunta or not pergunta.strip():
        logger.warning("⚠️ Pergunta vazia ou inválida recebida.")
        return InstitucionalAgent(), "institucional", []

    logger.info("🔍 Interpretando pergunta recebida:")
    logger.info(pergunta)

    try:
        tema: str = classificar_tema(pergunta)
    except Exception as e:
        logger.error(f"❌ Erro ao classificar tema: {e}")
        tema = "desconhecido"

    try:
        cidades: List[Dict[str, Any]] = detectar_cidades(pergunta, max_cidades=10)
    except Exception as e:
        logger.error(f"❌ Erro ao detectar cidades: {e}")
        cidades = []

    if tema in AGENTS_DISPONIVEIS:
        agente_classe: Type[AgentType] = AGENTS_DISPONIVEIS[tema]
        logger.info(
            f"🤖 Tema identificado: {tema} | Agente selecionado: {agente_classe.__name__}"
        )
        return agente_classe(), tema, cidades

    logger.warning(
        f"⚠️ Tema '{tema}' não corresponde a nenhum agente estruturado. Usando InstitucionalAgent."
    )
    return InstitucionalAgent(), "institucional", cidades
