# backend/utils/config.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# === Diretório base do projeto ===
PROJETO_RAIZ: Path = Path(__file__).parent.parent.resolve()

# === Carregamento do .env ===
ENV_PATH: Path = PROJETO_RAIZ / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# === Variáveis obrigatórias ===
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não definida.")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY não definida.")

# === Variáveis de embedding ===
PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX: Optional[str] = os.getenv("PINECONE_INDEX")
EMBEDDING_PROVIDER: Optional[str] = os.getenv("EMBEDDING_PROVIDER")
EMBEDDING_MODEL: Optional[str] = os.getenv("EMBEDDING_MODEL")

# === Configurações de Performance ===
PERFORMANCE_LEVEL: str = os.getenv("PERFORMANCE_LEVEL", "auto")
EMBEDDINGS_PATH: Path = PROJETO_RAIZ / "data" / "embeddings_cidades.npz"

# === Diretórios utilizados ===
PROMPT_DIR: Path = PROJETO_RAIZ / "core" / "prompts"
LOGS_DIR: Path = PROJETO_RAIZ / "logs"
DATA_DIR: Path = PROJETO_RAIZ / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
UPLOADS_TEMP_DIR: Path = PROJETO_RAIZ / "uploads_temp"

# === Criação de pastas essenciais ===
for pasta in [LOGS_DIR, UPLOADS_TEMP_DIR]:
    pasta.mkdir(parents=True, exist_ok=True)
