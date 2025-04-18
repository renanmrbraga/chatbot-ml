# backend/utils/embedder.py
from pinecone import Pinecone
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from utils.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX,
    COHERE_API_KEY,
    EMBEDDING_MODEL
)
from utils.logger import get_logger

logger = get_logger(__name__)

def get_embedder():
    """
    Inicializa o embedder Cohere via LangChain.
    """
    try:
        model_name = EMBEDDING_MODEL
        logger.debug(f"🧠 Carregando modelo de embeddings Cohere: {model_name}")
        embedder = CohereEmbeddings(
            model=model_name,
            cohere_api_key=COHERE_API_KEY,
            user_agent="chatppp"
        )
        logger.info("✅ Modelo de embeddings Cohere carregado com sucesso.")
        return embedder
    except Exception as e:
        logger.critical(f"❌ Erro ao carregar modelo de embeddings Cohere ({model_name}): {e}")
        raise RuntimeError(f"Falha ao inicializar o modelo de embeddings: {e}")


def get_vectorstore():
    """
    Conecta ao índice remoto do Pinecone com o embedder atual.
    """
    try:
        embedder = get_embedder()
        logger.debug("🔗 Inicializando Pinecone com novo SDK...")

        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(name=PINECONE_INDEX)

        logger.debug(f"🔍 Usando índice Pinecone: {PINECONE_INDEX}")
        vectorstore = PineconeVectorStore(
            index=index,
            embedding=embedder,
            text_key="text"
        )

        logger.info("✅ Conexão com o índice Pinecone estabelecida com sucesso.")
        return vectorstore

    except Exception as e:
        logger.critical(f"❌ Erro ao conectar ao índice Pinecone: {e}")
        raise RuntimeError(f"Falha ao conectar ao banco vetorial Pinecone: {e}")
