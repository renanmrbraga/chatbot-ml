# chatbot-llm/backend/core/engine.py
import json
import hashlib
import os
from typing import Optional, List, Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from config.dicionarios import llm
from utils.formatters import formatar_dados
from utils.logger import get_logger

logger = get_logger(__name__)
CACHE_DIR = "cache/llm"
os.makedirs(CACHE_DIR, exist_ok=True)


def gerar_chave_cache(texto_unico: str) -> str:
    return hashlib.sha256(texto_unico.encode("utf-8")).hexdigest()


def carregar_do_cache(chave: str) -> Optional[str]:
    path = os.path.join(CACHE_DIR, f"{chave}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # garante que retornamos Optional[str], não Any
        raw = data.get("resposta")
        return raw if isinstance(raw, str) else None
    return None


def salvar_em_cache(chave: str, resposta: str) -> None:
    path = os.path.join(CACHE_DIR, f"{chave}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"resposta": resposta}, f, ensure_ascii=False)


def gerar_resposta(
    pergunta: str,
    dados: List[Dict[str, Any]],
    fontes: Optional[List[str]] = None,
    prompt_template: Optional[str] = None,
    **template_vars: Any,
) -> str:
    """
    Gera a resposta usando estritamente o prompt_template fornecido pelo agent.
    Todos os parâmetros adicionais (dados_formatados, contextos, comparacoes, etc.)
    devem ser passados via template_vars.
    """
    if not prompt_template:
        logger.error("❌ Bug: prompt_template não foi fornecido pelo agent.")
        raise ValueError("Nenhum prompt_template fornecido a gerar_resposta.")

    # formata dados e monta string de fontes
    dados_formatados = template_vars.pop("dados_formatados", formatar_dados(dados))
    fontes_str = ", ".join(fontes or ["Fonte desconhecida"])

    # calcula chave e tenta cache
    texto_cache = pergunta + dados_formatados + fontes_str
    chave = gerar_chave_cache(texto_cache)
    cached = carregar_do_cache(chave)
    if cached:
        logger.debug("⚡ Resposta recuperada do cache.")
        return cached

    # usa estritamente o template passado pelo agent
    prompt = ChatPromptTemplate.from_template(prompt_template).format_messages(
        pergunta=pergunta,
        dados_formatados=dados_formatados,
        fontes=fontes_str,
        **template_vars,
    )
    raw = llm.invoke(prompt).content
    # cast para str e strip para garantir retorno do tipo correto
    raw_text = raw if isinstance(raw, str) else str(raw)
    resposta = raw_text.strip()

    salvar_em_cache(chave, resposta)
    logger.debug(f"🧠 Resposta gerada:\n{resposta}")
    return resposta
