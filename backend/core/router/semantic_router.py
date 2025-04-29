# core/router/semantic_router.py
from __future__ import annotations

import re
from typing import List, Optional, cast
from utils.logger import get_logger
from config.dicionarios import THEME_KEYWORDS

logger = get_logger(__name__)

# 🚀 Palavras que forçam o tema 'institucional'
PALAVRAS_INSTITUCIONAL = [
    "grupo houer",
    "houer",
    "empresa",
    "qualidade",
    "certificação",
    "infraestrutura",
    "sustentabilidade",
    "projetos de engenharia",
    "ppp",
    "concessão",
]


def classificar_tema(pergunta: str) -> Optional[str]:
    """
    Classifica a pergunta em um dos temas definidos pelo projeto.
    - Se tiver alguma palavra de Houer, retorna 'institucional'.
    - Se bater em algum tema de THEME_KEYWORDS, retorna esse tema.
    - Caso contrário, retorna None (nenhum tema).
    """
    texto = pergunta or ""
    lower = texto.lower()

    # 0️⃣ Se for algo institucional sobre Houer, força 'institucional'
    if any(palavra in lower for palavra in PALAVRAS_INSTITUCIONAL):
        logger.info("🔵 Tema classificado manualmente como 'institucional'")
        return "institucional"

    # 1️⃣ Classificação por palavras-chave para os demais temas
    for tema, patterns in THEME_KEYWORDS.items():
        if tema == "comparative":
            continue  # comparativo tratado em outro módulo
        for pat in patterns:
            if re.search(pat, lower):
                logger.info(f"⚙️ Tema classificado via regra: {tema}")
                return cast(str, tema)

    # 2️⃣ Sem match: retorna None - podendo escalar para fallback do llm ---> ele escolher o tema
    logger.info(
        "⚠️ Nenhuma regra bateu e não é institucional por Houer. Nenhum tema definido."
    )
    return None
