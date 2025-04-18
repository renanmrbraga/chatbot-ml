# backend/database/log_manager.py
from database.mongo_logger import log_interacao
from typing import Optional

def adicionar_log(
    session_id: str,
    pergunta: str,
    resposta: str,
    fontes: list[str],
    cidade: Optional[str],
    uf: Optional[str],
    tema: str
) -> None:
    """
    Registra uma interação no MongoDB.
    """
    log_interacao(
        session_id=session_id,
        user_input=pergunta,
        resposta=resposta,
        agente=tema,
        cidades=[cidade] if cidade else [],
        tema=tema
    )
