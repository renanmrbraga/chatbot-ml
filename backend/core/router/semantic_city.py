# core/router/semantic_city.py
from __future__ import annotations
import os
import numpy as np
import cohere

from typing import Optional, Any, Dict, List, Tuple, cast
from sqlalchemy import text
from functools import lru_cache
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer

from database.connection import get_engine
from utils.geo import detectar_uf
from utils.logger import get_logger
from utils.parser import normalizar, extrair_cidades_explicitamente

logger = get_logger(__name__)

PERFORMANCE_LEVEL: str = os.getenv("PERFORMANCE_LEVEL", "auto")
EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "cohere")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")
EMBEDDINGS_PATH: str = "data/embeddings_cidades.npz"

modelo_local: Optional[SentenceTransformer] = None
if PERFORMANCE_LEVEL in ("auto", "turbo"):
    try:
        modelo_local = SentenceTransformer("BAAI/bge-small-en-v1.5")
        logger.info("📌 Modelo de embedding local carregado com sucesso.")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao carregar modelo local: {e}")
        modelo_local = None

co: Optional[cohere.Client] = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None


@lru_cache(maxsize=1)
def carregar_cidades() -> Dict[str, Dict[str, Any]]:
    logger.info("📦 Carregando cidades do banco de dados via SQLAlchemy...")
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT codigo_ibge, cidade, estado FROM municipios")
        )
        linhas = result.fetchall()

    cidades: Dict[str, Dict[str, Any]] = {}
    for codigo_ibge, cidade, uf in linhas:
        nome_norm = normalizar(cidade)
        cidades[nome_norm] = {"codigo_ibge": codigo_ibge, "nome": cidade, "uf": uf}

    logger.info(f"✅ {len(cidades)} cidades carregadas e normalizadas.")
    return cidades


@lru_cache(maxsize=1)
def carregar_embeddings_cidades() -> Tuple[List[str], np.ndarray]:
    if not modelo_local:
        return [], np.array([])

    if os.path.exists(EMBEDDINGS_PATH):
        logger.info("📂 Embeddings de cidades carregados do disco.")
        data = np.load(EMBEDDINGS_PATH, allow_pickle=True)
        return data["nomes"].tolist(), data["embeddings"]

    logger.warning("⚠️ Embeddings não encontrados. Gerando on-the-fly.")
    cidades_index = carregar_cidades()
    nomes = list(cidades_index.keys())
    emb = modelo_local.encode(nomes, normalize_embeddings=True)

    os.makedirs("data", exist_ok=True)
    np.savez_compressed(EMBEDDINGS_PATH, nomes=nomes, embeddings=emb)
    logger.info("💾 Embeddings salvos em cache local.")
    return nomes, emb


def detectar_cidades(texto: str, max_cidades: int = 10) -> List[Dict[str, Any]]:
    cidades_index = carregar_cidades()
    texto_norm: str = normalizar(texto)

    # 1️⃣ Extração explícita
    cidades_exp = extrair_cidades_explicitamente(texto_norm, cidades_index, max_cidades)
    if len(cidades_exp) >= 2:
        logger.debug(
            f"🔎 Cidades extraídas diretamente: {[c['nome'] for c in cidades_exp]}"
        )
        return cast(List[Dict[str, Any]], cidades_exp[:max_cidades])

    # 2️⃣ Filtragem por estado, se não for comparativa
    is_comparativa = any(
        p in texto.lower()
        for p in ["compare", "comparar", "versus", " x ", " e ", "vs", "contra"]
    )
    uf_detectada = detectar_uf(texto_norm)
    if uf_detectada and not is_comparativa:
        logger.debug(f"🌎 UF detectada: {uf_detectada}")
        cidades_index = {
            nome: cid
            for nome, cid in cidades_index.items()
            if cid["uf"].lower() == uf_detectada.lower()
        }

    # 3️⃣ Fuzzy
    nomes_norm = list(cidades_index.keys())
    matches_fuzzy = process.extract(
        texto_norm, nomes_norm, scorer=fuzz.token_sort_ratio, limit=max_cidades * 2
    )
    fuzzy = {nome for nome, score, _ in matches_fuzzy if score >= 85}
    cidades_encontradas = set(fuzzy)

    # 4️⃣ Embeddings local
    if modelo_local:
        try:
            texto_emb = modelo_local.encode(texto_norm, normalize_embeddings=True)
            nomes_cached, emb_cidades = carregar_embeddings_cidades()
            scores = np.dot(emb_cidades, texto_emb)
            threshold = 0.45 if is_comparativa else 0.7
            for i in np.argsort(scores)[::-1][: max_cidades * 2]:
                if scores[i] >= threshold and nomes_cached[i] in cidades_index:
                    cidades_encontradas.add(nomes_cached[i])
        except Exception as e:
            logger.warning(f"⚠️ Erro embeddings locais: {e}")

    # 5️⃣ Fallback Cohere
    if not cidades_encontradas and co:
        try:
            emb_q = co.embed([texto_norm], model=EMBEDDING_MODEL).embeddings[0]
            emb_all = co.embed(nomes_norm, model=EMBEDDING_MODEL).embeddings
            scores = [np.dot(emb_q, e) for e in emb_all]
            for i in np.argsort(scores)[::-1][: max_cidades * 2]:
                if scores[i] >= 0.45:
                    cidades_encontradas.add(nomes_norm[i])
        except Exception as e:
            logger.warning(f"⚠️ Erro fallback Cohere: {e}")

    # Se nada
    if not cidades_encontradas:
        logger.warning("⚠️ Nenhuma cidade foi detectada.")
        return cast(List[Dict[str, Any]], [])

    # Agrupa por código IBGE
    agrupadas: Dict[str, Dict[str, Any]] = {}
    for nome in cidades_encontradas:
        cid = cidades_index.get(nome)
        if not cid:
            continue
        chave = normalizar(cid["nome"])
        pop = cid.get("populacao_total", 0)
        if chave not in agrupadas or pop > agrupadas[chave].get("populacao", 0):
            agrupadas[chave] = cid

    # Monta a lista final
    cidades_final: List[Dict[str, Any]] = []
    seen: set[int] = set()
    for cid in agrupadas.values():
        if cid["codigo_ibge"] not in seen:
            seen.add(cid["codigo_ibge"])
            cidades_final.append(cid)
        if len(cidades_final) >= max_cidades:
            break

    logger.debug(f"🏙️ {len(cidades_final)} cidades finais detectadas.")
    return cidades_final
