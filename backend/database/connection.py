# chatbot-llm/backend/database/connection.py
from __future__ import annotations

import time
import traceback
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from config.config import DATABASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

_engine: Optional[Engine] = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        for attempt in range(1, 11):
            try:
                logger.debug(f"🔌 Tentando conectar ao PostgreSQL ({attempt}/10)...")
                engine = create_engine(
                    DATABASE_URL, pool_pre_ping=True, future=True, echo=False
                )
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info("✅ Engine SQLAlchemy conectado com sucesso.")
                _engine = engine
                break
            except OperationalError as e:
                logger.warning(f"⚠️ Tentativa {attempt}/10 falhou: {e}")
                time.sleep(3)
        else:
            raise RuntimeError(
                "❌ Não foi possível conectar ao banco após múltiplas tentativas."
            )
    return _engine


def get_connection() -> Connection:
    try:
        conn = get_engine().connect()
        logger.debug("🧬 Conexão SQLAlchemy obtida com sucesso.")
        return conn
    except SQLAlchemyError as e:
        tb = traceback.format_exc()
        logger.critical(f"❌ Erro ao obter conexão: {e}\n{tb}")
        raise RuntimeError("Erro ao obter conexão SQLAlchemy.")
