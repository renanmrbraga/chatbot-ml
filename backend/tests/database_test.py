# chatbot-llm/backend/tests/database_test.py
from typing import Any, Dict
from sqlalchemy import text
from database.connection import get_engine


def check_database_health() -> Dict[str, Any]:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM municipios"))
            total: int = result.scalar_one()

        return {"status": "ok", "tabela_municipios": "ok", "registros": total}

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}


if __name__ == "__main__":
    from pprint import pprint

    pprint(check_database_health())
