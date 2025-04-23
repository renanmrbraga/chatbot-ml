# core/handlers/fallback_handler.py
from __future__ import annotations

from typing import Optional, Tuple, List, Dict, Any

from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
from core.agents.educacao_agent import EducacaoAgent
from utils.retriever import buscar_contexto
from utils.formatters import formatar_contexto_para_llm
from utils.logger import get_logger

logger = get_logger(__name__)


def executar_fallback(pergunta: str) -> Tuple[
    str,  # resposta
    List[str],  # fontes
    Optional[Dict[str, Any]],  # cidade_info
    Optional[Any],  # agente
]:
    logger.warning("🟡 Nenhum agente atribuído. Iniciando fallback híbrido.")

    cidade_info: Optional[Dict[str, Any]] = None
    fontes: List[str] = []
    resposta: str = (
        "🤖 Não consegui identificar a cidade nem encontrar dados relevantes."
    )
    agente: Optional[Any] = None

    try:
        cidades = detectar_cidades(pergunta)
        cidade_info = cidades[0] if cidades else None

        if cidade_info:
            logger.info(
                f"📍 Tentando fallback estruturado via Educação para cidade: {cidade_info['nome']}"
            )
            agente = EducacaoAgent()
            dados = agente.get_dados(pergunta)

            if dados and not (isinstance(dados, dict) and dados.get("tipo") == "erro"):
                fontes = dados.get("fontes", ["PostgreSQL"])
                resposta = dados.get("mensagem") or gerar_resposta(
                    pergunta, dados.get("dados", {}), tema="educacao", fontes=fontes
                )
                return resposta, fontes, cidade_info, agente
            else:
                logger.warning("⚠️ Fallback estruturado via Educação falhou.")

        logger.info("📚 Buscando contexto por embeddings (RAG)")
        documentos, metadatas = buscar_contexto(pergunta)

        if documentos:
            contexto, fontes = formatar_contexto_para_llm(documentos, metadatas)
            resposta = gerar_resposta(
                pergunta, {"context": contexto}, tema="institucional", fontes=fontes
            )
            return resposta, fontes, None, None

        logger.warning("⚠️ Nenhum documento relevante encontrado via embeddings.")

    except Exception as e:
        logger.error(f"❌ Erro no fallback: {e}")
        resposta = f"❌ Ocorreu um erro no fallback: {e}"

    return resposta, fontes, cidade_info, agente
