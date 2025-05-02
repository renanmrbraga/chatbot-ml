# chatbot-llm/backend/utils/embedder.py
from typing import Any
from pinecone import Pinecone, Index
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore

from config.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX,
    EMBEDDING_MODEL,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def get_embedder() -> Embeddings:
    """
    Inicializa o embedder HuggingFace para português-inglês.
    """
    try:
        logger.debug(
            f"🧠 Carregando modelo de embeddings HuggingFace: {EMBEDDING_MODEL}"
        )
        embedder = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},  # use "cuda" se tiver GPU
            encode_kwargs={"normalize_embeddings": True},  # normaliza vetores
        )
        logger.info("✅ Modelo de embeddings HuggingFace carregado com sucesso.")
        return embedder
    except Exception as e:
        logger.critical(f"❌ Erro ao carregar modelo de embeddings HuggingFace: {e}")
        raise RuntimeError(f"Falha ao inicializar o modelo de embeddings: {e}")


def get_vectorstore() -> VectorStore:
    """
    Conecta ao índice remoto do Pinecone com o embedder atual.
    """
    try:
        embedder = get_embedder()
        logger.debug("🔗 Inicializando Pinecone com novo SDK...")

        pc = Pinecone(api_key=PINECONE_API_KEY)
        index: Index = pc.Index(name=PINECONE_INDEX)

        logger.debug(f"🔍 Usando índice Pinecone: {PINECONE_INDEX}")
        vectorstore = PineconeVectorStore(
            index=index,
            embedding=embedder,
            text_key="text",
        )

        logger.info("✅ Conexão com o índice Pinecone estabelecida com sucesso.")
        return vectorstore
    except Exception as e:
        logger.critical(f"❌ Erro ao conectar ao índice Pinecone: {e}")
        raise RuntimeError(f"Falha ao conectar ao banco vetorial Pinecone: {e}")
