# backend/database/insert_database.py
import pandas as pd

from pathlib import Path

from database.connection import get_connection
from utils.logger import get_logger

logger = get_logger(__name__)
CSV_PATH = Path(__file__).parent.parent / "data" / "processed" / "city_data_sidra_microdadosedu.csv"

def run():
    try:
        df = pd.read_csv(CSV_PATH, sep=";")
        logger.info(f"📄 CSV carregado: {CSV_PATH} ({len(df)} linhas)")
    except Exception as e:
        logger.critical(f"❌ Erro ao carregar CSV: {e}")
        raise

    expected_columns = [
        "estado", "cidade", "codigo_ibge",
        "populacao", "ano_populacao", "pib_per_capita", "ano_pib",
        "ano_educacao",
        "matriculas_infantil", "matriculas_fundamental", "matriculas_medio",
        "matriculas_eja", "matriculas_especial", "matriculas_tecnico",
        "turmas_infantil", "turmas_fundamental", "turmas_medio",
        "turmas_eja", "turmas_especial", "turmas_tecnico",
        "docentes_infantil", "docentes_fundamental", "docentes_medio",
        "docentes_eja", "docentes_especial", "docentes_tecnico",
        "escolas_infantil", "escolas_fundamental", "escolas_medio",
        "escolas_eja", "escolas_especial", "escolas_tecnico",
        "infra_basica_biblioteca", "infra_basica_lab_ciencias", "infra_basica_lab_informatica",
        "infra_basica_cozinha", "infra_basica_refeitorio", "infra_basica_quadra_esportes",
        "infra_basica_internet", "infra_basica_acessibilidade_rampas",
        "prof_basica_professores_pedagogia", "prof_basica_coordenadores", "prof_basica_monitores",
        "cursos_tecnicos_ofertados"
    ]

    df = df[expected_columns]

    col_str = ", ".join(expected_columns)
    placeholders = ", ".join(["%s"] * len(expected_columns))
    update_str = ", ".join([f"{col} = EXCLUDED.{col}" for col in expected_columns if col != "codigo_ibge"])

    query = f"""
        INSERT INTO public.dados_municipios ({col_str})
        VALUES ({placeholders})
        ON CONFLICT (codigo_ibge) DO UPDATE SET
        {update_str}
    """

    try:
        logger.info("🔌 Conectando ao PostgreSQL...")
        with get_connection() as conn:
            with conn.cursor() as cursor:
                logger.info("📥 Iniciando inserção dos dados no banco...")
                for row in df.itertuples(index=False, name=None):
                    cursor.execute(query, row)
            conn.commit()
        logger.success("✅ Dados atualizados com sucesso no banco PostgreSQL!")

    except Exception as e:
        logger.error(f"❌ Erro ao inserir dados no banco: {e}")
