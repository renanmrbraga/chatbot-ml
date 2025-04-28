# core/router/semantic_router.py
from __future__ import annotations

import json
import re

from typing import List, cast
from langchain_core.prompts import ChatPromptTemplate

from config.dicionarios import TEMPLATE_TEMA, llm, TEMAS_VALIDOS, THEME_KEYWORDS
from utils.logger import get_logger

logger = get_logger(__name__)

# 🚀 Palavras que devem forçar o tema 'institucional'
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


def classificar_tema(pergunta: str) -> str:
    """
    Classifica a pergunta em um dos temas definidos em TEMAS_VALIDOS ou retorna 'llm' como fallback.
    Usa primeiro regras baseadas em keywords, e finalmente o LLM com TEMPLATE_TEMA se nada corresponder.
    """
    texto = pergunta or ""
    lower = texto.lower()

    # 0️⃣ Regras específicas para institucional
    if any(palavra in lower for palavra in PALAVRAS_INSTITUCIONAL):
        logger.info("🔵 Tema classificado manualmente como 'institucional'")
        return "institucional"

    # 1️⃣ Regras baseadas em keywords (populacao, economia, educacao, tecnica)
    for tema, patterns in THEME_KEYWORDS.items():
        if tema == "comparative":
            continue
        for pat in patterns:
            if re.search(pat, lower):
                logger.info(f"⚙️ Tema classificado via regra: {tema}")
                # deixa explícito pro MyPy que é str
                return cast(str, tema)

    # 2️⃣ Fallback via LLM usando TEMPLATE_TEMA
    logger.info("🔄 Nenhuma regra bateu. Classificando com LLM via TEMPLATE_TEMA")
    try:
        prompt_msgs = ChatPromptTemplate.from_template(TEMPLATE_TEMA).format_messages(
            pergunta=pergunta
        )
        resposta = llm.invoke(prompt_msgs)
        content = (resposta.content or "").strip()
        content = content.replace("```json", "").replace("```", "").strip()
        logger.debug(f"🧠 Saída bruta da LLM:\n{content}")

        # tenta interpretar como JSON garantindo str
        tema_llm: str = ""
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                raw = parsed.get("tema", "")
                tema_llm = raw if isinstance(raw, str) else ""
            elif isinstance(parsed, str):
                tema_llm = parsed
        except json.JSONDecodeError:
            m = re.search(r'"?tema"?\s*:\s*"?(?P<t>\w+)"?', content)
            if m and isinstance(m.group("t"), str):
                tema_llm = m.group("t")

        tema_llm = tema_llm.lower().strip()
        if tema_llm in TEMAS_VALIDOS:
            logger.info(f"✅ Tema classificado via LLM: {tema_llm}")
            return tema_llm
        logger.warning(f"⚠️ LLM retornou tema inválido: '{tema_llm}'")
    except Exception as e:
        logger.error(f"❌ Erro no fallback LLM: {e}")

    # 3️⃣ Fallback final
    logger.info("⚠️ Fallback final, atribuindo tema 'llm'")
    return "llm"
