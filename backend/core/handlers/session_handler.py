# backend/core/handlers/session_handler.py
import os
from pymongo import MongoClient

from database.mongo_logger import log_interacao
from utils.logger import get_logger

logger = get_logger(__name__)

# Conexão única e compartilhável
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URL)
collection = client.chatbot_logs.messages

def registrar_resposta(
    session_id: str,
    pergunta: str,
    resposta: str,
    agente: str,
    fontes: list[str],
    cidades: list[str],
    tema: str
) -> None:
    """
    Registra uma pergunta e resposta associadas a uma sessão no MongoDB.
    """
    try:
        log_interacao(
            session_id=session_id,
            user_input=pergunta,
            resposta=resposta,
            agente=agente,
            cidades=cidades,
            tema=tema
        )
        logger.debug(f"💾 Log registrado | Sessão: {session_id} | Agente: {agente}")
    except Exception as e:
        logger.error(f"❌ Erro ao registrar mensagem no MongoDB | Sessão: {session_id} | Erro: {e}")


def get_history_for_session(session_id: str) -> list[str]:
    """
    Recupera o histórico de mensagens associadas a uma sessão do MongoDB.
    """
    try:
        logger.debug(f"📚 Recuperando histórico da sessão: {session_id}")
        mensagens = collection.find({"session_id": session_id}).sort("timestamp", 1)
        return [
            f"Usuário: {msg.get('pergunta')}\nResposta ({msg.get('agente', 'LLM')}): {msg.get('resposta')}"
            for msg in mensagens
        ]
    except Exception as e:
        logger.error(f"❌ Erro ao recuperar histórico da sessão {session_id}: {e}")
        return []
