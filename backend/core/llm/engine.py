# backend/core/llm/engine.py
import json
import hashlib
import os

from langchain_core.prompts import ChatPromptTemplate

from utils.config import GROQ_API_KEY
from utils.logger import get_logger
from utils.llm_instance import llm  # ✅ Fonte única de verdade
from utils.llm_utils import TEMPLATE, formatar_dados

logger = get_logger(__name__)

# === Cache ===
CACHE_DIR = "cache/llm"
os.makedirs(CACHE_DIR, exist_ok=True)


def gerar_chave_cache(pergunta: str, dados_formatados: str) -> str:
    texto = pergunta.strip().lower() + dados_formatados.strip().lower()
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def carregar_do_cache(chave: str) -> str | None:
    caminho = os.path.join(CACHE_DIR, f"{chave}.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)["resposta"]
    return None


def salvar_em_cache(chave: str, resposta: str) -> None:
    caminho = os.path.join(CACHE_DIR, f"{chave}.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"resposta": resposta}, f, ensure_ascii=False)


def gerar_resposta(pergunta: str, dados: list[dict], tema: str = "desconhecido", fontes: list[str] = None) -> str:
    try:
        if not dados:
            return "Desculpe, não encontrei dados suficientes para responder à pergunta."

        dados_formatados = formatar_dados(dados)
        fontes_str = ", ".join(fontes or ["Fonte desconhecida"])
        chave = gerar_chave_cache(pergunta, dados_formatados)

        resposta_cache = carregar_do_cache(chave)
        if resposta_cache:
            logger.debug("⚡ Resposta recuperada do cache.")
            return resposta_cache

        prompt = ChatPromptTemplate.from_template(TEMPLATE).format_messages(
            pergunta=pergunta,
            dados_formatados=dados_formatados,
            fontes=fontes_str,
            tema=tema
        )

        resposta = llm.invoke(prompt).content.strip()
        salvar_em_cache(chave, resposta)
        logger.debug(f"🧠 Resposta gerada:\n{resposta}")
        return resposta

    except Exception as e:
        logger.error(f"❌ Erro ao gerar resposta interpretada: {e}")
        return "Ocorreu um erro ao gerar a resposta com base nos dados disponíveis."
