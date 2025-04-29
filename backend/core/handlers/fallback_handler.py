# core/handlers/fallback_handler.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from utils.logger import get_logger

logger = get_logger(__name__)


def executar_fallback(pergunta: str) -> Tuple[
    str,
    List[str],
    Optional[Dict[str, Any]],
    Optional[Any],
]:
    logger.warning("🚫 Fallback LLM desativado. Nenhuma resposta será gerada.")
    return (
        "Desculpe, não encontrei dados confiáveis para responder sua pergunta.",
        [],
        None,
        None,
    )
