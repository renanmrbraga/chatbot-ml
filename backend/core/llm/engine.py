# backend/core/llm/engine.py
import json
import hashlib
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from utils.config import GROQ_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=0.4,
    max_tokens=1024
)

TEMPLATE = """
Você é um analista de dados especialista em políticas públicas municipais.

Seu papel é analisar os dados abaixo e responder à pergunta do usuário com **clareza, objetividade e interpretação**.

A resposta deve:
- Ser escrita em linguagem natural, como se estivesse explicando para alguém curioso.
- Incluir comparações com valores exatos (números reais) das cidades.
- Destacar diferenças e similaridades de forma objetiva.
- Evitar frases genéricas como "é importante destacar...".
- Não repetir dados brutos em formato de tabela. Interprete, compare e conclua.
- Não inventar valores ou extrapolar o que está nos dados.

---

📌 Pergunta:
{pergunta}

📊 Dados:
{dados_formatados}

📁 Fontes: {fontes}
📚 Tema: {tema}
---

Responda de forma concisa e explicativa, como um analista experiente.
"""

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

# === Principal ===
def gerar_resposta(pergunta: str, dados: list[dict], tema: str = "desconhecido", fontes: list[str] = None) -> str:
    try:
        if not dados:
            return "Desculpe, não encontrei dados suficientes para responder à pergunta."

        dados_formatados = formatar_dados(dados)
        fontes_str = ", ".join(fontes or ["Fonte desconhecida"])
        chave = gerar_chave_cache(pergunta, dados_formatados)

        resposta_cache = carregar_do_cache(chave)
        if resposta_cache:
            logger.debug(f"⚡ Resposta recuperada do cache.")
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

def formatar_dados(dados: list[dict] | dict) -> str:
    """
    Converte os dados em um formato de tabela de texto legível para o prompt.

    Aceita tanto uma lista de dicionários (modo padrão) quanto um único dicionário com chave 'context'.
    """
    if not dados:
        return "Nenhum dado disponível."

    # Caso especial: contexto puro (agent_institucional)
    if isinstance(dados, dict) and "context" in dados:
        return dados["context"]

    # Garante que estamos lidando com lista de dicionários
    if isinstance(dados, dict):
        dados = [dados]

    colunas = list(dados[0].keys())
    linhas = [colunas] + [[str(linha.get(col, "")) for col in colunas] for linha in dados]
    header = " | ".join(colunas)
    separador = " | ".join(["---"] * len(colunas))
    corpo = "\n".join([" | ".join(linha) for linha in linhas[1:]])

    return f"{header}\n{separador}\n{corpo}"
