# backend/core/router/semantic_router.py
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from utils.config import GROQ_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

# Instância da LLM
llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=512
)

# Temas disponíveis
TEMAS_VALIDOS = ["educacao", "populacao", "economia", "dashboard"]

# Prompt de classificação
TEMPLATE = """
Você é um classificador semântico para um chatbot sobre políticas públicas de cidades brasileiras.

Classifique a pergunta abaixo em **apenas um** dos seguintes temas:

- educacao
- populacao
- economia
- dashboard (se for uma pergunta que compara duas ou mais cidades)

⚠️ Se a pergunta for muito vaga ou não pertencer a nenhum desses temas, **responda com "tema": "llm"**.

Retorne **apenas o JSON**, sem explicações, neste formato:

{"tema": "educacao"}

Pergunta: "{pergunta}"
"""

# Função para limpar a resposta
def limpar_marcacoes(texto: str) -> str:
    return texto.replace("```json", "").replace("```", "").strip()

# Heurística leve para detectar perguntas comparativas
def heuristica_comparativa(pergunta: str) -> bool:
    comparacoes = [
        r"\bcompare\b", r"\bcomparar\b", r"\bversus\b", r"\bvs\b", r"\bcontra\b",
        r" [xX] ", r"\bmelhor cidade\b", r"\bmais desenvolvida\b",
        r"\bmenor desigualdade\b", r"\bmaior investimento\b", r"\bdiferenças entre\b",
        r"\b(em|de|entre)\s+\w+\s+e\s+\w+"  # exemplo: "entre Recife e Salvador"
    ]
    return any(re.search(p, pergunta.lower()) for p in comparacoes)

# Classificação principal
def classificar_tema(pergunta: str) -> str:
    if not pergunta or not pergunta.strip():
        logger.warning("⚠️ Pergunta vazia ou inválida.")
        return "llm"

    if heuristica_comparativa(pergunta):
        logger.info("⚙️ Tema classificado via heurística: dashboard")
        return "dashboard"

    try:
        prompt = ChatPromptTemplate.from_template(TEMPLATE).format_messages(pergunta=pergunta)
        resposta = llm.invoke(prompt)
        content = limpar_marcacoes(resposta.content.strip())
        logger.debug(f"🧠 Saída bruta da LLM:\n{content}")

        # Parsing seguro com fallback
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r'"?tema"?\s*:\s*"?(?P<tema>\w+)"?', content)
            if match:
                tema = match.group("tema").lower()
                logger.warning(f"⚠️ JSON inválido, tema extraído via regex: {tema}")
                return tema if tema in TEMAS_VALIDOS else "llm"
            raise

        tema = parsed.get("tema", "").lower()
        if tema in TEMAS_VALIDOS:
            logger.info(f"✅ Tema classificado com sucesso: {tema}")
            return tema

        logger.warning(f"⚠️ Tema '{tema}' fora da lista de válidos.")

    except Exception as e:
        logger.error(f"❌ Erro ao classificar tema: {e}")

    return "llm"
