# chatbot-llm/backend/core/handlers/session_handler.py
from __future__ import annotations

import os
from typing import List, cast
from pymongo.collection import Collection
from pymongo import MongoClient

from database.mongo_logger import log_interacao
from utils.logger import get_logger
from utils.parser import formatar_historico_mensagens

logger = get_logger(__name__)

# Conexão única e compartilhável
MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
client: MongoClient = MongoClient(MONGO_URL)
collection: Collection = client.chatbot_logs.messages


def registrar_resposta(
    session_id: str,
    pergunta: str,
    resposta: str,
    agente_nome: str,
    fontes: List[str],
    cidades: List[str],
    tema: str,
) -> None:
    """
    Registra uma pergunta e resposta associadas a uma sessão no MongoDB.
    """
    try:
        log_interacao(
            session_id=session_id,
            user_input=pergunta,
            resposta=resposta,
            agente=agente_nome,
            cidades=cidades,
            tema=tema,
        )
        logger.debug(
            f"💾 Log registrado | Sessão: {session_id} | Agente: {agente_nome}"
        )
    except Exception as e:
        logger.error(
            f"❌ Erro ao registrar mensagem no MongoDB | Sessão: {session_id} | Erro: {e}"
        )


def get_history_for_session(session_id: str) -> List[str]:
    """
    Recupera o histórico de mensagens associadas a uma sessão do MongoDB.
    """
    try:
        logger.debug(f"📚 Recuperando histórico da sessão: {session_id}")
        mensagens = collection.find({"session_id": session_id}).sort("timestamp", 1)
        return cast(List[str], formatar_historico_mensagens(list(mensagens)))
    except Exception as e:
        logger.error(f"❌ Erro ao recuperar histórico da sessão {session_id}: {e}")
        return cast(List[str], [])
