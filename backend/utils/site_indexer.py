# backend/utils/site_indexer.py
import sys
import requests
from typing import Optional, List

from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.embedder import get_vectorstore
from utils.logger import get_logger
from config.config import PINECONE_API_KEY

logger = get_logger(__name__)


def limpar_html(html: str) -> List[str]:
    """
    Limpa o HTML e separa blocos importantes.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove tags inúteis
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
            "button",
        ]
    ):
        tag.decompose()

    # Pega apenas blocos significativos
    blocos = []
    for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "section", "article"]):
        texto = tag.get_text(separator=" ", strip=True)
        if texto and len(texto) > 30:  # ignora lixo pequeno
            blocos.append(texto)

    return blocos


def extrair_conteudo_site(url: str) -> List[str]:
    """
    Extrai o conteúdo principal do site em blocos separados.
    """
    try:
        logger.info(f"🌐 Acessando site: {url}")
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return limpar_html(response.text)
    except Exception as e:
        logger.error(f"❌ Erro ao acessar {url}: {e}")
        return []


def indexar_site(url: str, topico: Optional[str] = None) -> None:
    """
    Faz a indexação inteligente do site no Pinecone.
    """
    if not PINECONE_API_KEY:
        logger.error("🚫 Pinecone não configurado. A indexação está desativada.")
        return

    blocos = extrair_conteudo_site(url)
    if not blocos:
        logger.warning(f"⚠️ Nenhum conteúdo relevante encontrado para: {url}")
        return

    texto_completo = "\n\n".join(blocos)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100, separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(texto_completo)

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


# --------------- CLI (linha de comando) ----------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m utils.site_indexer https://exemplo.com [topico]")
    else:
        url = sys.argv[1]
        topico = sys.argv[2] if len(sys.argv) > 2 else None
        indexar_site(url, topico)
