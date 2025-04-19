# backend/core/handlers/log_handler.py
from database.log_manager import adicionar_log
from utils.logger import get_logger
from utils.parser import extrair_cidades_uf

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
        cidades, uf = extrair_cidades_uf(cidade_info)

        adicionar_log(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta,
            fontes=fontes,
            cidade=cidades,
            uf=uf,
            tema=tema,
        )

        logger.debug(
            f"📝 Log registrado com sucesso | Sessão: {session_id} | Cidade(s): {cidades} | UF: {uf} | Tema: {tema}"
        )

    except Exception as e:
        logger.error(f"❌ Erro ao registrar log no banco | Sessão: {session_id} | Erro: {e}")
