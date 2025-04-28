# core/router/semantic_metric.py
from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Optional, Tuple

from langchain_core.prompts import ChatPromptTemplate

from utils.logger import get_logger
from config.dicionarios import TEMPLATE_METRICA, llm, METRICAS_VALIDAS, HEURISTICAS

logger = get_logger(__name__)


def aplicar_heuristica(pergunta: str) -> Optional[Tuple[str, str]]:
    pergunta_lower = pergunta.lower()
    for termo, coluna in HEURISTICAS.items():
        if termo in pergunta_lower:
            label = METRICAS_VALIDAS.get(coluna, coluna)
            logger.info(f"⚙️ Métrica classificada via heurística: {coluna} ({label})")
            return coluna, label
    return None


@lru_cache(maxsize=1000)
def classificar_metrica(pergunta: str) -> Tuple[str, str]:
    heuristica = aplicar_heuristica(pergunta)
    if heuristica:
        return heuristica

    try:
        prompt = ChatPromptTemplate.from_template(TEMPLATE_METRICA).format_messages(
            pergunta=pergunta
        )
        resposta = llm.invoke(prompt)
        raw_content: str = resposta.content

        logger.debug(f"📨 Resposta bruta da LLM:\n{raw_content}")

        # Tira quebras, aspas e caracteres estranhos
        content = re.sub(r"[`\r\t\\]+", "", raw_content).strip()
        content_lower = content.lower()

        logger.debug(f"🧼 Conteúdo limpo da LLM:\n{content_lower}")

        # Se for direto o nome da coluna
        if content_lower in METRICAS_VALIDAS:
            logger.info(f"✅ Métrica reconhecida diretamente: '{content_lower}'")
            return content_lower, METRICAS_VALIDAS[content_lower]

        # Tenta extrair JSON
        try:
            parsed = json.loads(content_lower)
        except json.JSONDecodeError:
            # Tenta via regex como fallback
            match = re.search(
                r'"coluna"\s*:\s*"(?P<coluna>[\w_]+)".*?"label"\s*:\s*"(?P<label>[^"]+)"',
                content_lower,
                re.DOTALL,
            )
            if match:
                parsed = {
                    "coluna": match.group("coluna").strip().lower(),
                    "label": match.group("label").strip(),
                }
                logger.warning(f"⚠️ JSON inválido, mas extraído via regex: {parsed}")
            else:
                logger.error(
                    f"❌ JSON inválido e regex falhou. Conteúdo:\n{content_lower}"
                )
                return "populacao_total", METRICAS_VALIDAS["populacao_total"]

        coluna = parsed.get("coluna", "").strip().lower()
        label = parsed.get("label", METRICAS_VALIDAS.get(coluna, "")).strip()

        if not coluna or coluna not in METRICAS_VALIDAS:
            logger.warning(f"⚠️ Coluna inválida ou não reconhecida: '{coluna}'")
            return "populacao_total", METRICAS_VALIDAS["populacao_total"]

        return coluna, label or METRICAS_VALIDAS[coluna]

    except Exception as e:
        logger.error(f"❌ Erro inesperado ao classificar métrica: {e}")
        return "populacao_total", METRICAS_VALIDAS["populacao_total"]
