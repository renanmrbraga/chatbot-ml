# chatbot-llm/backend/core/router/semantic_city.py
from __future__ import annotations

import re
import numpy as np
from typing import Any, Dict, List, Tuple, cast
from functools import lru_cache
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer
from sqlalchemy import text

from database.connection import get_engine
from utils.geo import detectar_uf
from utils.logger import get_logger
from utils.parser import normalizar, extrair_cidades_explicitamente
from config.config import PERFORMANCE_LEVEL, EMBEDDINGS_PATH

logger = get_logger(__name__)

# Carregamento opcional do modelo de embeddings local
modelo_local: SentenceTransformer | None = None
if PERFORMANCE_LEVEL in ("auto", "turbo"):
    try:
        modelo_local = SentenceTransformer("BAAI/bge-small-en-v1.5")
        logger.info("📌 Modelo de embedding local carregado com sucesso.")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao carregar modelo local: {e}")
        modelo_local = None


@lru_cache(maxsize=1)
def carregar_cidades() -> Dict[str, Dict[str, Any]]:
    logger.info("📦 Carregando cidades do banco de dados via SQLAlchemy...")
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT
                  m.codigo_ibge,
                  m.cidade,
                  m.sigla_estado AS uf,
                  e.nome         AS estado
                FROM public.municipios m
                JOIN public.estados e
                  ON e.sigla = m.sigla_estado
                """
            )
        )
        linhas = result.fetchall()

    cidades: Dict[str, Dict[str, Any]] = {}
    for codigo_ibge, cidade, uf, estado in linhas:
        nome_norm = normalizar(cidade)
        cidades[nome_norm] = {
            "codigo_ibge": codigo_ibge,
            "nome": cidade,
            "uf": uf,
            "estado": estado,
        }

    logger.info(f"✅ {len(cidades)} cidades carregadas e normalizadas.")
    return cidades


@lru_cache(maxsize=1)
def carregar_embeddings_cidades() -> Tuple[List[str], np.ndarray]:
    if not modelo_local:
        return [], np.array([])

    if EMBEDDINGS_PATH.exists():
        logger.info("📂 Embeddings de cidades carregados do disco.")
        data = np.load(EMBEDDINGS_PATH, allow_pickle=True)
        return data["nomes"].tolist(), data["embeddings"]

    logger.warning("⚠️ Embeddings não encontrados. Gerando on-the-fly.")
    cidades_index = carregar_cidades()
    nomes = list(cidades_index.keys())
    emb = modelo_local.encode(nomes, normalize_embeddings=True)

    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(EMBEDDINGS_PATH, nomes=nomes, embeddings=emb)
    logger.info("💾 Embeddings salvos em cache local.")
    return nomes, emb


def detectar_cidades(texto: str, max_cidades: int = 10) -> List[Dict[str, Any]]:
    cidades_index = carregar_cidades()
    texto_norm = normalizar(texto)

    # 1️⃣ Se for comparativa, usar apenas match literal para todas as cidades mencionadas
    is_comparativa = any(
        termo in texto.lower()
        for termo in [
            "compare",
            "comparar",
            "versus",
            " vs ",
            " x ",
            ",",
            " e ",
            " ou ",
        ]
    )
    if is_comparativa:
        literal_matches = []
        for nome_norm, cid in cidades_index.items():
            if re.search(rf"\b{re.escape(nome_norm)}\b", texto_norm):
                literal_matches.append(cid)
        if literal_matches:
            normals = [normalizar(c["nome"]) for c in literal_matches]
            filtered = []
            for idx, cid in enumerate(literal_matches):
                norm = normals[idx]
                if any(other != norm and norm in other for other in normals):
                    continue
                filtered.append(cid)
            nomes = [c["nome"] for c in filtered]
            logger.debug(f"🔎 (Comparativa literal) Cidades extraídas: {nomes}")
            return filtered

    # 2️⃣ Match literal exato para 1 única cidade
    for nome_norm in sorted(cidades_index.keys(), key=len, reverse=True):
        if re.search(rf"\b{re.escape(nome_norm)}\b", texto_norm):
            cid = cidades_index[nome_norm]
            logger.debug(f"🔎 Match literal único: {cid['nome']}")
            return [cid]

    # 3️⃣ Extração explícita via parser (fallback para singular)
    cidades_exp = extrair_cidades_explicitamente(texto_norm, cidades_index, max_cidades)
    if cidades_exp:
        cidades_ordenadas = sorted(
            cidades_exp, key=lambda c: len(normalizar(c["nome"])), reverse=True
        )
        nomes = [c["nome"] for c in cidades_ordenadas]
        logger.debug(f"🔎 Cidades extraídas via parser: {nomes}")
        return cast(List[Dict[str, Any]], cidades_ordenadas[:max_cidades])

    # 4️⃣ Filtragem por estado, se não comparativa
    uf_detectada = detectar_uf(texto_norm)
    if uf_detectada and not is_comparativa:
        logger.debug(f"🌎 UF detectada: {uf_detectada}")
        cidades_index = cast(
            Dict[str, Dict[str, Any]],
            {
                nome: cid
                for nome, cid in cidades_index.items()
                if cid["uf"].lower() == uf_detectada.lower()
            },
        )

    # 5️⃣ Fuzzy matching
    nomes_norm = list(cidades_index.keys())
    matches = process.extract(
        texto_norm, nomes_norm, scorer=fuzz.token_sort_ratio, limit=max_cidades * 2
    )
    fuzzy = {nome for nome, score, _ in matches if score >= 85}
    cidades_encontradas = set(fuzzy)

    # 6️⃣ Embeddings local (se disponível)
    if modelo_local:
        try:
            texto_emb = modelo_local.encode(texto_norm, normalize_embeddings=True)
            nomes_cached, emb_cidades = carregar_embeddings_cidades()
            scores = np.dot(emb_cidades, texto_emb)
            threshold = 0.45 if is_comparativa else 0.7
            for idx in np.argsort(scores)[::-1][: max_cidades * 2]:
                nn = nomes_cached[idx]
                if scores[idx] >= threshold and nn in cidades_index:
                    cidades_encontradas.add(nn)
        except Exception as e:
            logger.warning(f"⚠️ Erro embeddings locais: {e}")

    if not cidades_encontradas:
        logger.warning("⚠️ Nenhuma cidade foi detectada.")
        return []

    # 7️⃣ Agrupamento final, evitando duplicatas
    agrupadas: Dict[str, Dict[str, Any]] = {}
    for nome_norm in cidades_encontradas:
        if nome_norm not in cidades_index:
            continue
        cid = cidades_index[nome_norm]
        chave = normalizar(cid["nome"])
        pop = cid.get("populacao_total", 0)
        if chave not in agrupadas or pop > agrupadas[chave].get("populacao", 0):
            agrupadas[chave] = cid

    cidades_final: List[Dict[str, Any]] = []
    seen = set()
    for cid in agrupadas.values():
        if cid["codigo_ibge"] not in seen:
            seen.add(cid["codigo_ibge"])
            cidades_final.append(cid)
        if len(cidades_final) >= max_cidades:
            break

    logger.debug(f"🏙️ {len(cidades_final)} cidades finais detectadas.")
    return cidades_final
