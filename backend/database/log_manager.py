# database/log_manager.py
from typing import Optional, Union, List

from database.mongo_logger import log_interacao


def adicionar_log(
    session_id: str,
    pergunta: str,
    resposta: str,
    fontes: List[str],
    cidade: Union[str, List[str], None],
    uf: Optional[str],
    tema: str,
) -> None:
    """
    Registra uma interação no MongoDB.
    """
    if isinstance(cidade, list):
        cidades_list: List[str] = cidade
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
        tema=tema,
    )
