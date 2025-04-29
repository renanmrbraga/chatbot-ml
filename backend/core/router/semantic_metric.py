# core/router/semantic_metric.py
from __future__ import annotations

import re
from functools import lru_cache
from typing import Optional, Tuple

from utils.logger import get_logger
from config.dicionarios import METRICAS_VALIDAS, HEURISTICAS

logger = get_logger(__name__)


def aplicar_heuristica(pergunta: str) -> Optional[Tuple[str, str]]:
    """
    Verifica termos-chave em HEURISTICAS para identificar coluna e label.
    """
    pergunta_lower = pergunta.lower()
    for termo, coluna in HEURISTICAS.items():
        if termo in pergunta_lower:
            label = METRICAS_VALIDAS.get(coluna, coluna)
            logger.info(f"⚙️ Métrica classificada via heurística: {coluna} ({label})")
            return coluna, label
    return None


@lru_cache(maxsize=1000)
def classificar_metrica(pergunta: str) -> Tuple[str, str]:
    """
    Classifica a métrica com base em heurísticas definidas.
    Se nada for encontrado, retorna 'populacao_total' por padrão.
    """
    heuristica = aplicar_heuristica(pergunta)
    if heuristica:
        return heuristica

    # Fallback final determinístico
    logger.info(
        "⚠️ Nenhuma heurística encontrou métrica. Usando padrão 'populacao_total'."
    )
    return "populacao_total", METRICAS_VALIDAS["populacao_total"]
