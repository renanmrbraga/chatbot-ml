# chatbot-llm/backend/core/agents/institucional_agent.py
from __future__ import annotations

from typing import Any, Dict, Optional, List
from utils.logger import get_logger
from utils.retriever import buscar_contexto
from core.llm.engine import gerar_resposta
from config.dicionarios import TEMPLATE_INSTITUCIONAL

logger = get_logger(__name__)


class InstitucionalAgent:
    def __init__(self) -> None:
        self.tema: str = "institucional"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self, pergunta: str, cidades_detectadas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        logger.info(f"🏢 Processando pergunta institucional: {pergunta}")

        try:
            textos, metadados = buscar_contexto(pergunta, top_k=5)

            # Fallback quando não há documentos
            if not textos:
                logger.warning(
                    "⚠️ Nenhum documento institucional encontrado. Fallback LLM."
                )
                resposta_fallback = gerar_resposta(
                    pergunta=pergunta,
                    dados=[],
                    tema=self.tema,
                    fontes=[],
                    prompt_template=TEMPLATE_INSTITUCIONAL,
                    dados_formatados="",
                )
                return {
                    "tipo": "resposta",
                    "mensagem": resposta_fallback,
                    "dados": [],
                    "fontes": [],
                }

            # Concatena trechos de contexto
            contexto = "\n---\n".join(textos)
            fontes = list({meta.get("source", "Desconhecido") for meta in metadados})

            # Gera resposta usando template institucional
            resposta = gerar_resposta(
                pergunta=pergunta,
                dados=[{"context": contexto}],
                tema=self.tema,
                fontes=fontes,
                prompt_template=TEMPLATE_INSTITUCIONAL,
                dados_formatados=contexto,
            )

            return {
                "tipo": "resposta",
                "mensagem": resposta,
                "dados": [{"context": contexto}],
                "fontes": fontes,
            }

        except Exception as e:
            logger.error(f"❌ Erro ao processar pergunta institucional: {e}")
            return {
                "tipo": "erro",
                "mensagem": "Erro ao acessar as informações institucionais.",
                "dados": None,
                "fontes": [],
                "erro": str(e),
            }
