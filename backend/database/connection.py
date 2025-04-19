# backend/database/connection.py
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from utils.config import DATABASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

# === Criação segura do Engine global ===
try:
    engine: Engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        future=True,
        echo=False  # coloque True para debug de queries
    )
    logger.debug("🔌 SQLAlchemy engine criado com sucesso.")
except Exception as e:
    tb = traceback.format_exc()
    logger.critical(f"❌ Erro ao criar engine SQLAlchemy: {e}\n{tb}")
    raise RuntimeError("Erro crítico ao inicializar engine do banco.")

# === Acesso ao engine (uso avançado ou ORM) ===
def get_engine() -> Engine:
    """
    Retorna o engine SQLAlchemy para uso com pandas, ORM ou execução manual de SQL.
    """
    return engine

# === Contexto de conexão simplificado (uso raw com 'with') ===
def get_connection() -> Connection:
    """
    Retorna uma conexão ativa com o banco, para ser usada com 'with' ou execução direta:
        with get_connection() as conn:
            conn.execute(text("SELECT ..."))
    """
    try:
        conn = engine.connect()
        logger.debug("🧬 Conexão SQLAlchemy obtida com sucesso.")
        return conn
    except SQLAlchemyError as e:
        tb = traceback.format_exc()
        logger.critical(f"❌ Erro ao obter conexão: {e}\n{tb}")
        raise RuntimeError("Erro ao obter conexão SQLAlchemy.")
