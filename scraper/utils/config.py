# chatbot-llm/scraper/utils/config.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# === Diretório base do scraper ===
PROJETO_RAIZ: Path = Path(__file__).parent.parent.resolve()
ENV_PATH: Path = PROJETO_RAIZ / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# === Variáveis obrigatórias ===
DATABASE_URL: str = os.getenv("DATABASE_URL", "")

LOGS_DIR = PROJETO_RAIZ / "logs"
LOGS_DIR.mkdir(exist_ok=True)
