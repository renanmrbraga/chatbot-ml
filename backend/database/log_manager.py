# backend/database/log_manager.py
from database.mongo_logger import log_interacao
from typing import Optional, Union

def adicionar_log(
    session_id: str,
    pergunta: str,
    resposta: str,
    fontes: list[str],
    cidade: Union[str, list[str], None],
    uf: Optional[str],
    tema: str
) -> None:
    """
    Registra uma interação no MongoDB.
    """
    if isinstance(cidade, list):
        cidades_list = cidade
    elif isinstance(cidade, str):
        cidades_list = [cidade]
    else:
        cidades_list = []

    log_interacao(
        session_id=session_id,
        user_input=pergunta,
        resposta=resposta,
        agente=tema,
        cidades=cidades_list,
        tema=tema
    )
