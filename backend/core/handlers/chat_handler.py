# core/handlers/chat_handler.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from core.handlers.fallback_handler import executar_fallback
from core.handlers.log_handler import registrar_log
from core.handlers.session_handler import registrar_resposta
from core.router.interpreter import interpretar_pergunta
from utils.logger import get_logger

logger = get_logger(__name__)


def processar_pergunta(pergunta: str, session_id: str) -> Tuple[
    str,  # resposta
    List[str],  # fontes
    Optional[Dict[str, Any]],  # cidade_info
    Optional[str],  # tema
    Optional[Any],  # agente
    Optional[Dict[str, Any]],  # dados
    Optional[str],  # comparative_base64
    Optional[str],  # csv_base64
    Optional[str],  # pdf_base64
]:
    logger.info(f"📥 Nova pergunta recebida: {pergunta}")

    resposta: str = "❌ Não consegui responder sua pergunta."
    fontes: List[str] = []
    comparative_base64: Optional[str] = None
    csv_base64: Optional[str] = None
    pdf_base64: Optional[str] = None
    dados: Optional[Dict[str, Any]] = None

    agente, tema, cidades = interpretar_pergunta(pergunta)
    agente_nome: str = agente.__class__.__name__ if agente else "LLM"
    cidade_info: Optional[Dict[str, Any]] = cidades[0] if cidades else None

    if agente:
        try:
            dados = agente.get_dados(pergunta, cidades_detectadas=cidades)
        except Exception as e:
            logger.error(f"❌ Erro ao obter dados com agente {agente_nome}: {e}")
            dados = None

    if isinstance(dados, dict):
        if dados.get("tipo") == "erro":
            resposta = str(dados.get("mensagem", resposta))
        else:
            resposta = str(dados.get("mensagem", resposta))
            fontes = list(dados.get("fontes", ["PostgreSQL"]))
            comparative_base64 = dados.get("imagem_base64")
            csv_base64 = dados.get("csv_base64")
            pdf_base64 = dados.get("pdf_base64")

            cidade_info = (
                dados.get("cidade_info")
                or cidade_info
                or (
                    dados["dados"][0]
                    if isinstance(dados.get("dados"), list) and dados["dados"]
                    else None
                )
            )
    else:
        resposta, fontes, cidade_info, agente = executar_fallback(pergunta)
        agente_nome = agente.__class__.__name__ if agente else "LLM"

    try:
        registrar_resposta(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta,
            agente_nome=agente_nome,
            fontes=fontes,
            cidades=[c["nome"] for c in cidades] if cidades else [],
            tema=tema,
        )
        registrar_log(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta,
            fontes=fontes,
            cidade_info=cidade_info,
            tema=tema,
        )
    except Exception as e:
        logger.error(
            f"❌ Erro ao registrar log no banco | Sessão: {session_id} | Erro: {e}"
        )

    logger.info(f"✅ Resposta final pronta | Agente: {agente_nome} | Fontes: {fontes}")

    return (
        resposta,
        fontes,
        cidade_info,
        tema,
        agente,
        dados,
        comparative_base64,
        csv_base64,
        pdf_base64,
    )
