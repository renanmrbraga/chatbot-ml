# backend/core/handlers/log_handler.py
from database.log_manager import adicionar_log
from utils.logger import get_logger

logger = get_logger(__name__)


def registrar_log(
    pergunta: str,
    resposta: str,
    fontes: list[str],
    cidade_info: dict | list | None,
    tema: str,
    session_id: str = "sem_id"
) -> None:
    """
    Registra a interação no banco de logs com informações relevantes.
    """
    try:
        cidade = None
        uf = None

        if isinstance(cidade_info, dict):
            cidade = cidade_info.get("nome")
            uf = cidade_info.get("uf")
        elif isinstance(cidade_info, list) and cidade_info:
            cidade = cidade_info[0].get("nome")
            uf = cidade_info[0].get("uf")

        adicionar_log(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta,
            fontes=fontes,
            cidade=cidade,
            uf=uf,
            tema=tema,
        )

        logger.debug(
            f"📝 Log registrado com sucesso | Sessão: {session_id} | Cidade: {cidade} | UF: {uf} | Tema: {tema}"
        )

    except Exception as e:
        logger.error(f"❌ Erro ao registrar log no banco | Sessão: {session_id} | Erro: {e}")
