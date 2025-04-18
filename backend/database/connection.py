# backend/database/connection.py
import psycopg
import traceback
from utils.config import DATABASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

def get_connection(autocommit: bool = False) -> psycopg.Connection:
    """
    Estabelece e retorna uma conexão com o banco de dados PostgreSQL.
    Opcionalmente, pode habilitar autocommit.
    """
    try:
        conn = psycopg.connect(DATABASE_URL, autocommit=autocommit)
        logger.debug("🔌 Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except Exception as e:
        tb = traceback.format_exc()
        logger.critical(f"❌ Erro ao conectar ao banco de dados: {e}\n{tb}")
        raise RuntimeError("Erro crítico de conexão com o banco de dados.")
