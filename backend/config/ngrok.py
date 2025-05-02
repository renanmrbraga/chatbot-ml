# chatbot-llm/backend/config/ngrok_origin.py
from typing import Optional


def get_ngrok_origin() -> Optional[str]:
    try:
        with open("/app/ngrok/.env.runtime", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("NGROK_URL="):
                    return line.strip().split("=", 1)[1]
    except FileNotFoundError:
        return None

    return None
