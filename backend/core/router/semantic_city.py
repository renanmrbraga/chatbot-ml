# backend/core/router/semantic_city.py
import os
import re
import numpy as np
import cohere

from sqlalchemy import text
from functools import lru_cache
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer

from database.connection import get_engine
from utils.geo import detectar_uf
from utils.logger import get_logger
from utils.parser import normalizar, extrair_cidades_explicitamente  # <- Importadas daqui

logger = get_logger(__name__)

# === CONFIGURAÇÕES ===
PERFORMANCE_LEVEL = os.getenv("PERFORMANCE_LEVEL", "auto")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "cohere")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMBEDDINGS_PATH = "data/embeddings_cidades.npz"

# === MODELOS ===
modelo_local = None
if PERFORMANCE_LEVEL in ("auto", "turbo"):
    try:
        modelo_local = SentenceTransformer("BAAI/bge-small-en-v1.5")
        logger.info("📌 Modelo de embedding local carregado com sucesso.")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao carregar modelo local: {e}")
        modelo_local = None

co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None

@lru_cache(maxsize=1)
def carregar_cidades():
    logger.info("📦 Carregando cidades do banco de dados via SQLAlchemy...")
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT codigo_ibge, cidade, estado FROM dados_municipios"))
        linhas = result.fetchall()

    cidades = {}
    for codigo_ibge, cidade, uf in linhas:
        nome_norm = normalizar(cidade)
        cidades[nome_norm] = {
            "codigo_ibge": codigo_ibge,
            "nome": cidade,
            "uf": uf
        }

    logger.info(f"✅ {len(cidades)} cidades carregadas e normalizadas.")
    return cidades

@lru_cache(maxsize=1)
def carregar_embeddings_cidades():
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

def detectar_cidades(texto: str, max_cidades: int = 10) -> list[dict]:
    cidades_index = carregar_cidades()
    texto_norm = normalizar(texto)

    cidades_exp = extrair_cidades_explicitamente(texto_norm, cidades_index, max_cidades=max_cidades)
    if len(cidades_exp) >= 2:
        logger.debug(f"🔎 Cidades extraídas diretamente da pergunta: {[c['nome'] for c in cidades_exp]}")
        return cidades_exp[:max_cidades]

    is_comparativa = any(p in texto.lower() for p in ["compare", "comparar", "versus", " x ", " e ", "diferenças", "vs", "contra"])
    uf_detectada = detectar_uf(texto_norm)
    if uf_detectada:
        logger.debug(f"🌎 UF detectada: {uf_detectada}")
        if not is_comparativa:
            cidades_index = {
                nome: cid for nome, cid in cidades_index.items()
                if cid["uf"].lower() == uf_detectada.lower()
            }

    nomes_norm = list(cidades_index.keys())

    matches_fuzzy = process.extract(texto_norm, nomes_norm, scorer=fuzz.token_sort_ratio, limit=max_cidades * 2)
    fuzzy_cidades = {nome for nome, score, _ in matches_fuzzy if score >= 85}
    cidades_encontradas = set(fuzzy_cidades)

    if modelo_local:
        logger.debug("🧠 Usando embeddings locais...")
        try:
            texto_emb = modelo_local.encode(texto_norm, normalize_embeddings=True)
            nomes_cached, emb_cidades = carregar_embeddings_cidades()
            scores = np.dot(emb_cidades, texto_emb)

            min_score = 0.45 if is_comparativa else 0.7
            top_idx = np.argsort(scores)[::-1][:max_cidades * 2]

            for i in top_idx:
                score = scores[i]
                if score < min_score:
                    continue
                cidade_nome = nomes_cached[i]
                if cidade_nome in cidades_index:
                    cidades_encontradas.add(cidade_nome)
        except Exception as e:
            logger.warning(f"⚠️ Erro ao usar embeddings locais: {e}")

    if not cidades_encontradas and co:
        logger.debug("🌐 Fallback com Cohere...")
        try:
            emb_pergunta = co.embed([texto_norm], model=EMBEDDING_MODEL).embeddings[0]
            emb_cidades = co.embed(nomes_norm, model=EMBEDDING_MODEL).embeddings
            scores = [np.dot(emb_pergunta, e) for e in emb_cidades]
            for i in np.argsort(scores)[::-1][:max_cidades * 2]:
                score = scores[i]
                if score >= 0.45:
                    cidades_encontradas.add(nomes_norm[i])
        except Exception as e:
            logger.warning(f"⚠️ Erro no fallback com Cohere: {e}")

    if not cidades_encontradas:
        logger.warning("⚠️ Nenhuma cidade foi detectada.")
        return []

    cidades_final = []
    codigos_ibge = set()

    agrupadas = {}
    for nome in cidades_encontradas:
        cid = cidades_index.get(nome)
        if not cid:
            continue
        chave = normalizar(cid["nome"])
        pop = cid.get("populacao", 0)
        if chave not in agrupadas or pop > agrupadas[chave].get("populacao", 0):
            agrupadas[chave] = cid

    for cidade in agrupadas.values():
        if cidade["codigo_ibge"] not in codigos_ibge:
            codigos_ibge.add(cidade["codigo_ibge"])
            cidades_final.append(cidade)
        if len(cidades_final) >= max_cidades:
            break

    logger.debug(f"🏙️ Total de cidades finais detectadas: {len(cidades_final)}")
    return cidades_final
