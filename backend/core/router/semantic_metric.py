# ✅ backend/core/router/semantic_metric.py
import json
import re
from langchain_core.prompts import ChatPromptTemplate

from utils.llm_instance import llm
from utils.logger import get_logger
from utils.llm_utils import TEMPLATE_METRICA
from utils.metricas import METRICAS_VALIDAS, HEURISTICAS

logger = get_logger(__name__)


def aplicar_heuristica(pergunta: str) -> tuple[str, str] | None:
    pergunta_lower = pergunta.lower()
    for termo, coluna in HEURISTICAS.items():
        if termo in pergunta_lower:
            label = METRICAS_VALIDAS.get(coluna, coluna)
            logger.info(f"⚙️ Métrica classificada via heurística: {coluna} ({label})")
            return coluna, label
    return None


def classificar_metrica(pergunta: str) -> tuple[str, str]:
    # 1️⃣ Heurística primeiro
    heuristica = aplicar_heuristica(pergunta)
    if heuristica:
        return heuristica

    try:
        # 2️⃣ LLM fallback
        prompt = ChatPromptTemplate.from_template(TEMPLATE_METRICA).format_messages(pergunta=pergunta)
        resposta = llm.invoke(prompt)
        raw_content = resposta.content

        logger.debug(f"📨 Resposta bruta da LLM:\n{raw_content}")

        # 🧼 Limpeza total
        content = re.sub(r"[`\n\r\t\"'\\]+", "", raw_content).strip()
        content_lower = content.lower()

        logger.debug(f"🧼 Conteúdo limpo da LLM:\n{content_lower}")

        # ✅ Caso especial: retorno direto
        if content_lower in METRICAS_VALIDAS:
            logger.info(f"✅ Métrica reconhecida diretamente: '{content_lower}'")
            return content_lower, METRICAS_VALIDAS[content_lower]

        # ⚠️ JSON ou regex fallback
        try:
            parsed = json.loads(content_lower)
        except json.JSONDecodeError:
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
                logger.error(f"❌ JSON inválido e regex falhou. Conteúdo:\n{content_lower}")
                return "", "Comparação geral entre cidades"

        coluna = parsed.get("coluna", "").strip().lower()
        label = parsed.get("label", METRICAS_VALIDAS.get(coluna, "")).strip()

        if not coluna or coluna not in METRICAS_VALIDAS:
            logger.warning(f"⚠️ Coluna inválida ou não reconhecida: '{coluna}' | Conteúdo limpo: '{content_lower}'")
            return "", "Comparação geral entre cidades"

        return coluna, label or METRICAS_VALIDAS.get(coluna)

    except Exception as e:
        logger.warning(f"⚠️ Falha ao classificar métrica: {e}")
        return "", "Comparação geral entre cidades (default)"
