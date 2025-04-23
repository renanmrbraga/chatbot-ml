# backend/utils/retriever.py
from typing import List, Tuple, Dict, Any
from utils.logger import get_logger
from utils.embedder import get_vectorstore

logger = get_logger(__name__)
vectorstore = get_vectorstore()


def buscar_contexto(
    pergunta: str, top_k: int = 5
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Busca os documentos semanticamente mais relevantes para a pergunta.

    Retorna:
    - Lista com os textos dos documentos.
    - Lista com os metadados associados.
    """
    try:
        logger.debug(f"🔍 Iniciando busca semântica para: '{pergunta}' (top_k={top_k})")
        resultados = vectorstore.similarity_search_with_score(pergunta, k=top_k)

        documentos: List[str] = [doc.page_content for doc, _ in resultados]
        metadatas: List[Dict[str, Any]] = [doc.metadata for doc, _ in resultados]

        for meta in metadatas:
            origem = meta.get("source") or meta.get("arquivo") or "desconhecido"
            logger.debug(f"📄 Documento relacionado: {origem}")

        logger.info(f"📚 {len(documentos)} documentos recuperados com embeddings.")
        return documentos, metadatas

    except Exception as e:
        logger.error(f"❌ Erro ao buscar contexto semântico: {e}")
        return [], []
