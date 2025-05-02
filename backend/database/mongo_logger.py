# chatbot-llm/backend/database/mongo_logger.py
import os
from typing import List

from pymongo import MongoClient, errors
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URL)
collection = client.chatbot_logs.messages


def log_interacao(
    session_id: str,
    user_input: str,
    resposta: str,
    agente: str,
    cidades: List[str],
    tema: str,
) -> None:
    """
    Registra uma interação completa no MongoDB com segurança.
    """
    doc = {
        "timestamp": datetime.utcnow(),
        "session_id": session_id,
        "pergunta": user_input,
        "resposta": resposta,
        "agente": agente,
        "tema": tema,
        "cidades": cidades or [],
    }

    try:
        collection.insert_one(doc)
        logger.debug(f"🗃️ Interação registrada no MongoDB | Sessão: {session_id}")
    except errors.PyMongoError as e:
        logger.error(f"❌ Erro ao salvar log no MongoDB: {e}")
