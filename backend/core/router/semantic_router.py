# core/router/semantic_router.py
from __future__ import annotations

import json
import re
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate

from config.dicionarios import TEMPLATE_TEMA, llm, TEMAS_VALIDOS
from utils.logger import get_logger

logger = get_logger(__name__)


def limpar_marcacoes(texto: str) -> str:
    return texto.replace("```json", "").replace("```", "").strip()


def heuristica_comparativa(pergunta: str) -> bool:
    comparacoes = [
        r"\bcompare\b",
        r"\bcomparar\b",
        r"\bversus\b",
        r"\bvs\b",
        r"\bcontra\b",
        r" [xX] ",
        r"\bmelhor cidade\b",
        r"\bmais desenvolvida\b",
        r"\bmenor desigualdade\b",
        r"\bmaior investimento\b",
        r"\bdiferenças entre\b",
        r"\b(em|de|entre)\s+\w+\s+e\s+\w+",
    ]
    return any(re.search(p, pergunta.lower()) for p in comparacoes)


def classificar_tema(pergunta: str) -> str:
    if not pergunta or not pergunta.strip():
        logger.warning("⚠️ Pergunta vazia ou inválida.")
        return "llm"

    if heuristica_comparativa(pergunta):
        logger.info("⚙️ Tema classificado via heurística: comparative")
        return "comparative"

    try:
        prompt = ChatPromptTemplate.from_template(TEMPLATE_TEMA).format_messages(
            pergunta=pergunta
        )
        resposta = llm.invoke(prompt)
        content: str = limpar_marcacoes(resposta.content.strip())
        logger.debug(f"🧠 Saída bruta da LLM:\n{content}")

        parsed: Dict[str, Any]
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r'"?tema"?\s*:\s*"?(?P<tema>\w+)"?', content)
            if match:
                regex_tema = match.group("tema").lower()
                logger.warning(
                    f"⚠️ JSON inválido, tema extraído via regex: {regex_tema}"
                )
                return regex_tema if regex_tema in TEMAS_VALIDOS else "llm"
            raise

        tema: str = parsed.get("tema", "").lower()
        if tema in TEMAS_VALIDOS:
            logger.info(f"✅ Tema classificado com sucesso: {tema}")
            return tema

        logger.warning(f"⚠️ Tema '{tema}' fora da lista de válidos.")

    except Exception as e:
        logger.error(f"❌ Erro ao classificar tema: {e}")

    return "llm"
