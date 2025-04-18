# backend/core/router/uf_matcher.py
import re
import unicodedata
from functools import lru_cache
from utils.logger import get_logger

logger = get_logger(__name__)

# 🔁 Mapeamento estado → siglas + sinônimos + regionalismos
ESTADOS = {
    "AC": ["acre", "ac"],
    "AL": ["alagoas", "al"],
    "AP": ["amapa", "ap"],
    "AM": ["amazonas", "am"],
    "BA": ["bahia", "ba"],
    "CE": ["ceara", "ce"],
    "DF": ["distrito federal", "df", "brasilia"],
    "ES": ["espirito santo", "es"],
    "GO": ["goias", "go"],
    "MA": ["maranhao", "ma"],
    "MT": ["mato grosso", "mt"],
    "MS": ["mato grosso do sul", "ms"],
    "MG": ["minas gerais", "mg"],
    "PA": ["para", "pa"],
    "PB": ["paraiba", "pb"],
    "PR": ["parana", "pr"],
    "PE": ["pernambuco", "pe"],
    "PI": ["piaui", "pi"],
    "RJ": ["rio de janeiro", "rj", "carioca"],
    "RN": ["rio grande do norte", "rn"],
    "RS": ["rio grande do sul", "rs", "gaucho", "gaúcho"],
    "RO": ["rondonia", "ro"],
    "RR": ["roraima", "rr"],
    "SC": ["santa catarina", "sc", "catarinense"],
    "SP": ["sao paulo", "sp", "paulista"],
    "SE": ["sergipe", "se"],
    "TO": ["tocantins", "to"],
}

@lru_cache(maxsize=64)
def normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode("ascii")

def detectar_uf(texto: str) -> str | None:
    """
    Detecta a sigla de UF (estado) a partir de sinônimos ou menções no texto.
    """
    texto_norm = normalizar(texto)

    for sigla, termos in ESTADOS.items():
        for termo in termos:
            if re.search(rf"\b{re.escape(termo)}\b", texto_norm):
                logger.debug(f"🌎 UF detectada: {sigla} via termo '{termo}'")
                return sigla

    logger.debug("🌎 Nenhuma UF detectada.")
    return None
