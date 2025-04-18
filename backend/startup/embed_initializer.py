# backend/startup/embed_initializer.py
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from core.router.semantic_city import carregar_cidades, normalizar
from utils.logger import get_logger

logger = get_logger(__name__)

EMBEDDINGS_PATH = "data/embeddings_cidades.npz"
MODEL_NAME = "BAAI/bge-small-en-v1.5"


def inicializar_embeddings():
    if os.path.exists(EMBEDDINGS_PATH):
        logger.info("📂 Embeddings de cidades já estão salvos. Nenhuma ação necessária.")
        return

    logger.info("⚙️ Nenhum embedding encontrado. Iniciando geração...")
    try:
        modelo = SentenceTransformer(MODEL_NAME)
        nomes = list(carregar_cidades().keys())
        embeddings = modelo.encode(nomes, normalize_embeddings=True)

        os.makedirs("data", exist_ok=True)
        np.savez_compressed(EMBEDDINGS_PATH, nomes=nomes, embeddings=embeddings)

        logger.info(f"✅ Embeddings de {len(nomes)} cidades salvos com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro ao gerar embeddings no startup: {e}")
