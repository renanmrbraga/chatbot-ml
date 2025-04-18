# backend/scraping/extrator_basico_microdados.py
import json
import pandas as pd

from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "data" / "raw" / "microdados_ed_basica_2023.csv"
JSON_PATH = BASE_DIR / "data" / "processed" / "city_data_sidra.json"

def run():
    try:
        # Carrega JSON agrupado por estado
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            city_data = json.load(f)
        logger.info(f"📄 JSON de cidades carregado: {JSON_PATH}")

        # Carrega CSV do INEP
        df = pd.read_csv(CSV_PATH, sep=";", encoding="latin1", low_memory=False)
        logger.info(f"📊 CSV do INEP carregado: {CSV_PATH} ({len(df)} linhas)")

        df["QT_PROF_PEDAGOGIA"] = pd.to_numeric(df["QT_PROF_PEDAGOGIA"], errors="coerce").clip(upper=500).fillna(0)

        ignorados = 0
        atualizados = 0

        for codigo_ibge, grupo in df.groupby("CO_MUNICIPIO"):
            cidade_info = grupo.iloc[0]
            uf = cidade_info["SG_UF"]

            cidade_json = None
            for nome, dados in city_data.get(uf, {}).items():
                if dados.get("codigo_ibge") == codigo_ibge:
                    cidade_json = city_data[uf][nome]
                    break

            if not cidade_json:
                ignorados += 1
                logger.debug(f"⚠️ Código IBGE {codigo_ibge} não encontrado no JSON ({uf})")
                continue

            educacao = {
                "ano": 2023,
                "matriculas": {
                    "infantil": int(grupo["QT_MAT_INF"].sum()),
                    "fundamental": int(grupo["QT_MAT_FUND"].sum()),
                    "medio": int(grupo["QT_MAT_MED"].sum()),
                    "eja": int(grupo["QT_MAT_EJA"].sum()),
                    "especial": int(grupo["QT_MAT_ESP"].sum())
                },
                "infraestrutura_ensino_basico": {
                    "biblioteca": int(grupo["IN_BIBLIOTECA"].sum()),
                    "lab_ciencias": int(grupo["IN_LABORATORIO_CIENCIAS"].sum()),
                    "lab_informatica": int(grupo["IN_LABORATORIO_INFORMATICA"].sum()),
                    "cozinha": int(grupo["IN_COZINHA"].sum()),
                    "refeitorio": int(grupo["IN_REFEITORIO"].sum()),
                    "quadra_esportes": int(grupo["IN_QUADRA_ESPORTES"].sum()),
                    "internet": int(grupo["IN_INTERNET"].sum()),
                    "acessibilidade_rampas": int(grupo["IN_ACESSIBILIDADE_RAMPAS"].sum())
                },
                "profissionais_ensino_basico": {
                    "professores_pedagogia": int(grupo["QT_PROF_PEDAGOGIA"].sum()),
                    "coordenadores": int(grupo["QT_PROF_COORDENADOR"].sum()),
                    "monitores": int(grupo["QT_PROF_MONITORES"].sum())
                },
                "turmas": {
                    "infantil": int(grupo["QT_TUR_INF"].sum()),
                    "fundamental": int(grupo["QT_TUR_FUND"].sum()),
                    "medio": int(grupo["QT_TUR_MED"].sum()),
                    "eja": int(grupo["QT_TUR_EJA"].sum()),
                    "especial": int(grupo["QT_TUR_ESP"].sum())
                },
                "docentes": {
                    "infantil": int(grupo["QT_DOC_INF"].sum()),
                    "fundamental": int(grupo["QT_DOC_FUND"].sum()),
                    "medio": int(grupo["QT_DOC_MED"].sum()),
                    "eja": int(grupo["QT_DOC_EJA"].sum()),
                    "especial": int(grupo["QT_DOC_ESP"].sum())
                },
                "escolas": {
                    "infantil": int(grupo["IN_INF"].sum()),
                    "fundamental": int(grupo["IN_FUND"].sum()),
                    "medio": int(grupo["IN_MED"].sum()),
                    "eja": int(grupo["IN_EJA"].sum()),
                    "especial": int(grupo["IN_ESP"].sum())
                }
            }

            cidade_json["educacao"] = educacao
            atualizados += 1

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(city_data, f, ensure_ascii=False, indent=4)

        logger.info(f"✅ Dados educacionais atualizados: {atualizados} cidades")
        if ignorados > 0:
            logger.warning(f"⚠️ {ignorados} cidades foram ignoradas por não estarem no JSON base")
        logger.info("📁 JSON atualizado com dados educacionais básicos.")

    except Exception as e:
        logger.error(f"❌ Erro ao processar dados educacionais: {e}")
