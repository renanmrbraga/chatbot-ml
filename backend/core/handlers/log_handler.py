# core/handlers/log_handler.py
from __future__ import annotations

from typing import Any, Dict, List, Union

from database.mongo_logger import log_interacao
from utils.logger import get_logger
from utils.parser import extrair_cidades_uf

logger = get_logger(__name__)


def registrar_log(
    pergunta: str,
    resposta: str,
    fontes: List[str],
    cidade_info: Union[Dict[str, Any], List[Dict[str, Any]], None],
    tema: str,
    session_id: str = "sem_id",
) -> None:
    try:
        # ⛔️ Filtro: apenas logar se tiver fontes confiáveis
        if not any(f for f in fontes if f == "PostgreSQL" or f.startswith("http")):
            logger.warning(
                f"🚫 Log ignorado por fonte não confiável | Sessão: {session_id} | Fontes: {fontes}"
            )
            return

        cidades, _ = extrair_cidades_uf(cidade_info)

        log_interacao(
            session_id=session_id,
            user_input=pergunta,
            resposta=resposta,
            agente=tema,
            cidades=cidades,
            tema=tema,
        )

        logger.debug(
            f"📝 Log Mongo salvo | Sessão: {session_id} | Cidade(s): {cidades} | Tema: {tema}"
        )

    except Exception as e:
        logger.error(
            f"❌ Erro ao salvar log no MongoDB | Sessão: {session_id} | Erro: {e}"
        )
