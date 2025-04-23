# utils/geo.py
# utils/geo.py
import re
from typing import Optional, cast

from utils.parser import normalizar
from utils.logger import get_logger

logger = get_logger(__name__)


def detectar_uf(texto: str) -> Optional[str]:
    """
    Detecta a sigla de UF (estado) a partir de sinônimos ou menções no texto.
    Retorna a sigla (ex: "SP") ou None se não encontrar.
    """
    texto_norm: str = normalizar(texto)

    # importa ESTADOS só quando a função é chamada, quebrando o ciclo
    from config.dicionarios import ESTADOS

    for sigla, termos in ESTADOS.items():
        for termo in termos:
            if re.search(rf"\b{re.escape(termo)}\b", texto_norm):
                logger.debug(f"🌎 UF detectada: {sigla} via termo '{termo}'")
                return cast(str, sigla)

    logger.debug("🌎 Nenhuma UF detectada.")
    return None
