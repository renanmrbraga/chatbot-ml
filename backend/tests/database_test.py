# backend/utils/check_db_status.py
from database.connection import get_connection

def check_database_health() -> dict:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM dados_municipios")
                total = cur.fetchone()[0]

        return {
            "status": "ok",
            "tabela_dados_municipios": "ok",
            "registros": total
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }

if __name__ == "__main__":
    from pprint import pprint
    pprint(check_database_health())
