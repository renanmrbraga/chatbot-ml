# core/router/interpreter.py
from __future__ import annotations

from typing import Tuple, Type, Dict, List, Any, Protocol, runtime_checkable
import re
from utils.logger import get_logger
from core.router.semantic_router import classificar_tema
from core.router.semantic_city import detectar_cidades

from core.agents.educacao_agent import EducacaoAgent
from core.agents.tecnica_agent import TecnicaAgent
from core.agents.populacao_agent import PopulacaoAgent
from core.agents.economia_agent import EconomiaAgent
from core.agents.comparative_agent import ComparativeAgent
from core.agents.institucional_agent import InstitucionalAgent
from core.agents.llm_agent import LLMAgent

logger = get_logger(__name__)


@runtime_checkable
class AgentType(Protocol):
    def get_dados(
        self, pergunta: str, cidades_detectadas: List[Dict[str, Any]]
    ) -> Dict[str, Any]: ...


def load_agents() -> Dict[str, Type[AgentType]]:
    # Mapeamento de agentes disponíveis
    return {
        "educacao": EducacaoAgent,
        "educacao_tecnica": TecnicaAgent,
        "tecnica": TecnicaAgent,
        "populacao": PopulacaoAgent,
        "economia": EconomiaAgent,
        "comparative": ComparativeAgent,
        "institucional": InstitucionalAgent,
        "llm": LLMAgent,
    }


AGENTS_DISPONIVEIS = load_agents()


def interpretar_pergunta(pergunta: str) -> Tuple[AgentType, str, List[Dict[str, Any]]]:
    if not pergunta or not pergunta.strip():
        logger.warning("⚠️ Pergunta vazia ou inválida recebida.")
        return InstitucionalAgent(), "institucional", []

    logger.info("🔍 Interpretando pergunta recebida:")
    logger.info(pergunta)

    # 1️⃣ Detectar cidades primeiro
    try:
        cidades = detectar_cidades(pergunta, max_cidades=10)
    except Exception as e:
        logger.error(f"❌ Erro ao detectar cidades: {e}")
        cidades = []

    # 2️⃣ Se 2+ cidades, forçar comparative
    if len(cidades) >= 2:
        tema = "comparative"
        logger.info(
            f"⚙️ Mais de uma cidade detectada ({len(cidades)}). Override tema para 'comparative'."
        )
    else:
        # 3️⃣ Classificar tema via classificar_tema
        try:
            tema = classificar_tema(pergunta)
        except Exception as e:
            logger.error(f"❌ Erro ao classificar tema: {e}")
            tema = "institucional"

    # 4️⃣ Selecionar agente: se tema não existir, usar LLMAgent
    agente_classe = AGENTS_DISPONIVEIS.get(tema, LLMAgent)
    logger.info(
        f"🤖 Tema identificado: {tema} | Agente selecionado: {agente_classe.__name__}"
    )
    return agente_classe(), tema, cidades
