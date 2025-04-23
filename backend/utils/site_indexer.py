# backend/utils/site_indexer.py
import sys
import requests

from typing import Optional
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.config import PINECONE_API_KEY
from utils.embedder import get_vectorstore
from utils.logger import get_logger

logger = get_logger(__name__)


def limpar_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "iframe",
            "svg",
            "header",
            "footer",
            "form",
            "nav",
        ]
    ):
        tag.decompose()
    texto = soup.get_text(separator="\n")
    linhas = [linha.strip() for linha in texto.splitlines()]
    return "\n".join([linha for linha in linhas if linha])


def extrair_conteudo_site(url: str) -> str:
    try:
        logger.info(f"🌐 Acessando site: {url}")
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return limpar_html(response.text)
    except Exception as e:
        logger.error(f"❌ Erro ao acessar {url}: {e}")
        return ""


def indexar_site(url: str, topico: Optional[str] = None) -> None:
    if not PINECONE_API_KEY:
        logger.error("🚫 Pinecone não configurado. A indexação está desativada.")
        return

    texto = extrair_conteudo_site(url)
    if not texto:
        logger.warning(f"⚠️ Nenhum conteúdo encontrado para: {url}")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100, separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(texto)

    if not chunks:
        logger.warning(f"⚠️ Nenhum chunk gerado para {url}")
        return

    metadatas = [
        {"source": url, "chunk": i, "topico": topico or "website"}
        for i in range(len(chunks))
    ]

    try:
        vectorstore = get_vectorstore()
        vectorstore.add_texts(chunks, metadatas=metadatas)
        logger.info(f"✅ {len(chunks)} chunks indexados de {url}")
    except Exception as e:
        logger.error(f"❌ Erro ao indexar {url}: {e}")


# ---------------- CLI ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m utils.site_indexer https://exemplo.com [topico]")
    else:
        url = sys.argv[1]
        topico = sys.argv[2] if len(sys.argv) > 2 else None
        indexar_site(url, topico)
