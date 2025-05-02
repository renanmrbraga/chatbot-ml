# chatbot-llm/scraper/utils/logger.py
from utils.connection import get_connection
import subprocess
import os

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "postgres", "init.sql"
)

# Obtém a string de conexão SQLAlchemy
engine = get_connection().engine
url = engine.url

# Monta o comando pg_dump
pg_dump_cmd = [
    "pg_dump",
    f"--dbname=postgresql://{url.username}:{url.password}@{url.host}:{url.port}/{url.database}",
    "--file",
    OUTPUT_PATH,
    "--no-owner",
    "--no-privileges",
    "--clean",
    "--if-exists",
    "--encoding=UTF8",
]

# Executa o pg_dump
try:
    subprocess.run(pg_dump_cmd, check=True)
    print(f"✅ Banco exportado com sucesso para {OUTPUT_PATH}")
except subprocess.CalledProcessError as e:
    print(f"❌ Falha ao exportar o banco: {e}")
