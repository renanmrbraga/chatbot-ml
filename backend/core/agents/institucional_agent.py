# core/agents/agent_institucional.py
from __future__ import annotations

from typing import Any, Dict, Optional, List

from langchain_core.documents import Document
from utils.logger import get_logger
from utils.embedder import get_vectorstore
from core.llm.engine import gerar_resposta
from core.router.semantic_city import detectar_cidades

logger = get_logger(__name__)


class InstitucionalAgent:
    def __init__(self) -> None:
        self.tema: str = "institucional"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self, pergunta: str, cidades_detectadas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        logger.info(f"🏢 Processando pergunta institucional: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta)
        cidade_info = cidades[0] if cidades else None  # noqa: F841

        try:
            retriever = get_vectorstore().as_retriever()
            documentos: List[Document] = retriever.invoke(pergunta)

            if not documentos:
                logger.warning("⚠️ Nenhum documento institucional encontrado.")
                return {
                    "tipo": "erro",
                    "mensagem": "Desculpe, não encontrei nenhuma informação institucional relevante para essa pergunta.",
                    "dados": None,
                    "fontes": [],
                }

            contexto: str = "\n---\n".join([doc.page_content for doc in documentos])
            fontes: List[str] = list(
                set(doc.metadata.get("source", "Desconhecido") for doc in documentos)
            )

            resposta: str = gerar_resposta(
                pergunta=pergunta,
                dados={"context": contexto},
                tema=self.tema,
                fontes=fontes,
            )

            return {
                "tipo": "resposta",
                "mensagem": resposta,
                "dados": {"context": contexto},
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
