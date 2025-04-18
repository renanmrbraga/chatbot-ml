# backend/scraping/extrator_tecnico_microdados.py
import json
import pandas as pd

from pathlib import Path
from collections import defaultdict

from utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "data" / "raw" / "suplemento_cursos_tecnicos_2023.csv"
JSON_PATH = BASE_DIR / "data" / "processed" / "city_data_sidra.json"

def run():
    try:
        logger.info("📄 Lendo dados técnicos do INEP...")
        df = pd.read_csv(CSV_PATH, sep=";", encoding="latin1", low_memory=False)
        logger.info(f"📊 CSV carregado com {len(df)} registros")

        logger.info("🗂️ Lendo JSON de cidades já existente...")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            city_data = json.load(f)

        atualizados = 0
        ignorados = 0

        logger.info("🔄 Enriquecendo dados por município...")
        for cod_ibge, grupo in df.groupby("CO_MUNICIPIO"):
            municipio_data = defaultdict(int)

            for _, row in grupo.iterrows():
                municipio_data["matriculas_tecnico"] += int(pd.to_numeric(row["QT_MAT_CURSO_TEC"], errors="coerce") or 0)
                municipio_data["cursos_tecnicos_ofertados"] += int(pd.to_numeric(row["QT_CURSO_TEC"], errors="coerce") or 0)

            escolas_tecnicas = grupo["CO_ENTIDADE"].nunique()

            cidade_json = None
            for uf, cidades in city_data.items():
                for nome, dados in cidades.items():
                    if dados.get("codigo_ibge") == cod_ibge:
                        cidade_json = dados
                        break
                if cidade_json:
                    break

            if not cidade_json:
                ignorados += 1
                logger.debug(f"⚠️ Código IBGE não encontrado no JSON base: {cod_ibge}")
                continue

            if "educacao" not in cidade_json:
                cidade_json["educacao"] = {}

            educacao = cidade_json["educacao"]

            educacao["matriculas"] = {**educacao.get("matriculas", {}), "tecnico": municipio_data["matriculas_tecnico"]}
            educacao["turmas"] = {**educacao.get("turmas", {}), "tecnico": 0}
            educacao["docentes"] = {**educacao.get("docentes", {}), "tecnico": 0}
            educacao["escolas"] = {**educacao.get("escolas", {}), "tecnico": escolas_tecnicas}
            educacao["cursos_tecnicos_ofertados"] = municipio_data["cursos_tecnicos_ofertados"]
            educacao["ano"] = 2023

            atualizados += 1

        logger.info(f"✅ Municípios atualizados: {atualizados}")
        if ignorados > 0:
            logger.warning(f"⚠️ Municípios ignorados por ausência no JSON base: {ignorados}")

        logger.info("💾 Salvando JSON atualizado com dados técnicos...")
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(city_data, f, ensure_ascii=False, indent=4)

        logger.info("✅ Extração de dados técnicos finalizada com sucesso!")

    except Exception as e:
        logger.error(f"❌ Erro durante a extração técnica: {e}")
