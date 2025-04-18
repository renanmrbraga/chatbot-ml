# backend/utils/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Diretório base do projeto
PROJETO_RAIZ = Path(__file__).parent.parent.resolve()

# Sempre usa .env único
ENV_PATH = PROJETO_RAIZ / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Variáveis obrigatórias
DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL não definida.")
if GROQ_API_KEY is None:
    raise ValueError("❌ GROQ_API_KEY não definida.")

# Variáveis de embedding
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Diretórios utilizados
PROMPT_DIR = PROJETO_RAIZ / "core" / "prompts"  # usado se quiser reintegrar .txt no futuro
LOGS_DIR = PROJETO_RAIZ / "logs"
DATA_DIR = PROJETO_RAIZ / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
UPLOADS_TEMP_DIR = PROJETO_RAIZ / "uploads_temp"

# Criação de pastas essenciais
for pasta in [LOGS_DIR, UPLOADS_TEMP_DIR]:
    pasta.mkdir(parents=True, exist_ok=True)
