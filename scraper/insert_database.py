# scraper/core/insert_database.py
import pandas as pd
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.engine import Engine
from utils.connection import get_engine
from utils.logger import get_logger

logger = get_logger(__name__)

# Caminhos dos arquivos
BASE_DIR = Path(__file__).parent
PATH_JSON = BASE_DIR / "data" / "processed" / "municipios.csv"
PATH_CSV_BASICO = BASE_DIR / "data" / "external" / "microdados_ed_basica_2023.csv"
PATH_CSV_TECNICO = (
    BASE_DIR / "data" / "external" / "suplemento_cursos_tecnicos_2023.csv"
)


def inserir_estados_municipios(engine: Engine) -> None:
    df = pd.read_csv(PATH_JSON, encoding="utf-8")
    df = df.rename(
        columns={
            "Estado": "sigla_estado",
            "Cidade": "cidade",
            "Código_IBGE": "codigo_ibge",
            "População": "populacao_total",
            "Ano_População": "ano_populacao",
            "PIB": "pib_per_capita",
            "Ano_PIB": "ano_pib",
        }
    )
    df["sigla_estado"] = df["sigla_estado"].str.strip()
    df["cidade"] = df["cidade"].str.strip()

    estados = (
        df[["sigla_estado"]]
        .drop_duplicates()
        .rename(columns={"sigla_estado": "sigla"})
        .assign(nome=lambda d: d["sigla"])
    )
    municipios = df.to_dict(orient="records")

    with engine.begin() as conn:
        logger.info("🗺️ Inserindo estados a partir do CSV processado...")
        conn.execute(
            text(
                """
            INSERT INTO estados (sigla, nome)
            VALUES (:sigla, :nome)
            ON CONFLICT (sigla) DO NOTHING
        """
            ),
            estados.to_dict(orient="records"),
        )

        logger.info("🏙️ Inserindo municípios a partir do CSV processado...")
        conn.execute(
            text(
                """
            INSERT INTO municipios
                (codigo_ibge, sigla_estado, cidade, populacao_total, ano_populacao, pib_per_capita, ano_pib)
            VALUES
                (:codigo_ibge, :sigla_estado, :cidade, :populacao_total, :ano_populacao, :pib_per_capita, :ano_pib)
            ON CONFLICT (codigo_ibge) DO UPDATE SET
                sigla_estado    = EXCLUDED.sigla_estado,
                cidade          = EXCLUDED.cidade,
                populacao_total = EXCLUDED.populacao_total,
                ano_populacao   = EXCLUDED.ano_populacao,
                pib_per_capita  = EXCLUDED.pib_per_capita,
                ano_pib         = EXCLUDED.ano_pib
        """
            ),
            municipios,
        )

    logger.info("🗺️ Estados e municípios inseridos/atualizados com sucesso.")


def inserir_educacao_basica(engine: Engine) -> None:
    logger = get_logger(__name__)

    needed = [
        "CO_MUNICIPIO",
        "NU_ANO_CENSO",
        # Matrículas
        "QT_MAT_INF",
        "QT_MAT_INF_CRE",
        "QT_MAT_INF_PRE",
        "QT_MAT_FUND",
        "QT_MAT_FUND_AI",
        "QT_MAT_FUND_AF",
        "QT_MAT_MED",
        "QT_MAT_EJA",
        "QT_MAT_ESP",
        "QT_MAT_PROF_TEC",
        # Turmas
        "QT_TUR_INF",
        "QT_TUR_INF_CRE",
        "QT_TUR_INF_PRE",
        "QT_TUR_FUND",
        "QT_TUR_FUND_AI",
        "QT_TUR_FUND_AF",
        "QT_TUR_MED",
        "QT_TUR_EJA",
        "QT_TUR_ESP",
        "QT_TUR_PROF",
        # Docentes
        "QT_DOC_INF",
        "QT_DOC_INF_CRE",
        "QT_DOC_INF_PRE",
        "QT_DOC_FUND",
        "QT_DOC_FUND_AI",
        "QT_DOC_FUND_AF",
        "QT_DOC_MED",
        "QT_DOC_EJA",
        "QT_DOC_ESP",
        "QT_DOC_PROF_TEC",
        # Flags de escolas
        "IN_INF",
        "IN_FUND",
        "IN_MED",
        "IN_EJA",
        "IN_ESP",
        "IN_PROF_TEC",
        # Infraestrutura
        "IN_BIBLIOTECA",
        "IN_LABORATORIO_CIENCIAS",
        "IN_LABORATORIO_INFORMATICA",
        "IN_COZINHA",
        "IN_REFEITORIO",
        "IN_QUADRA_ESPORTES_COBERTA",
        "IN_QUADRA_ESPORTES_DESCOBERTA",
        "IN_ACESSO_INTERNET_COMPUTADOR",
        "IN_ACESSIBILIDADE_RAMPAS",
        # Profissionais de apoio
        "QT_PROF_PEDAGOGIA",
        "QT_PROF_COORDENADOR",
        "QT_PROF_MONITORES",
    ]

    # 1) carrega só o necessário
    df = pd.read_csv(
        PATH_CSV_BASICO,
        sep=";",
        encoding="latin-1",
        usecols=needed,
        low_memory=False,
    )

    # 2) agrega por município+ano
    agg = df.groupby(["CO_MUNICIPIO", "NU_ANO_CENSO"], as_index=False).sum()

    # 3–5) consolida matrículas, turmas, docentes
    agg["matriculas_educacao_infantil"] = agg[
        ["QT_MAT_INF", "QT_MAT_INF_CRE", "QT_MAT_INF_PRE"]
    ].sum(axis=1)
    agg["matriculas_ensino_fundamental"] = agg[
        ["QT_MAT_FUND", "QT_MAT_FUND_AI", "QT_MAT_FUND_AF"]
    ].sum(axis=1)
    agg["matriculas_ensino_medio"] = agg["QT_MAT_MED"]
    agg["matriculas_eja"] = agg["QT_MAT_EJA"]
    agg["matriculas_educacao_especial"] = agg["QT_MAT_ESP"]
    agg["matriculas_ensino_tecnico"] = agg["QT_MAT_PROF_TEC"]

    agg["turmas_educacao_infantil"] = agg[
        ["QT_TUR_INF", "QT_TUR_INF_CRE", "QT_TUR_INF_PRE"]
    ].sum(axis=1)
    agg["turmas_ensino_fundamental"] = agg[
        ["QT_TUR_FUND", "QT_TUR_FUND_AI", "QT_TUR_FUND_AF"]
    ].sum(axis=1)
    agg["turmas_ensino_medio"] = agg["QT_TUR_MED"]
    agg["turmas_eja"] = agg["QT_TUR_EJA"]
    agg["turmas_educacao_especial"] = agg["QT_TUR_ESP"]
    agg["turmas_ensino_tecnico"] = agg["QT_TUR_PROF"]

    agg["docentes_educacao_infantil"] = agg[
        ["QT_DOC_INF", "QT_DOC_INF_CRE", "QT_DOC_INF_PRE"]
    ].sum(axis=1)
    agg["docentes_ensino_fundamental"] = agg[
        ["QT_DOC_FUND", "QT_DOC_FUND_AI", "QT_DOC_FUND_AF"]
    ].sum(axis=1)
    agg["docentes_ensino_medio"] = agg["QT_DOC_MED"]
    agg["docentes_eja"] = agg["QT_DOC_EJA"]
    agg["docentes_educacao_especial"] = agg["QT_DOC_ESP"]
    agg["docentes_ensino_tecnico"] = agg["QT_DOC_PROF_TEC"]

    # 6) prepara educacao_basica, agora incluindo turmas_educacao_especial
    df_edu = agg.rename(
        columns={
            "CO_MUNICIPIO": "codigo_ibge",
            "NU_ANO_CENSO": "ano_dados",
            "IN_INF": "escolas_educacao_infantil",
            "IN_FUND": "escolas_ensino_fundamental",
            "IN_MED": "escolas_ensino_medio",
            "IN_EJA": "escolas_eja",
            "IN_ESP": "escolas_educacao_especial",
            "IN_PROF_TEC": "escolas_ensino_tecnico",
        }
    )[
        [
            "codigo_ibge",
            "ano_dados",
            # matrículas
            "matriculas_educacao_infantil",
            "matriculas_ensino_fundamental",
            "matriculas_ensino_medio",
            "matriculas_eja",
            "matriculas_educacao_especial",
            "matriculas_ensino_tecnico",
            # turmas (incluída a especial)
            "turmas_educacao_infantil",
            "turmas_ensino_fundamental",
            "turmas_ensino_medio",
            "turmas_eja",
            "turmas_educacao_especial",
            "turmas_ensino_tecnico",
            # docentes
            "docentes_educacao_infantil",
            "docentes_ensino_fundamental",
            "docentes_ensino_medio",
            "docentes_eja",
            "docentes_educacao_especial",
            "docentes_ensino_tecnico",
            # escolas
            "escolas_educacao_infantil",
            "escolas_ensino_fundamental",
            "escolas_ensino_medio",
            "escolas_eja",
            "escolas_educacao_especial",
            "escolas_ensino_tecnico",
        ]
    ]

    # 7) prepara infraestrutura (sem mudanças)
    df_infra = pd.DataFrame(
        {
            "codigo_ibge": agg["CO_MUNICIPIO"],
            "escolas_com_biblioteca": agg["IN_BIBLIOTECA"],
            "escolas_com_laboratorio_ciencias": agg["IN_LABORATORIO_CIENCIAS"],
            "escolas_com_laboratorio_informatica": agg["IN_LABORATORIO_INFORMATICA"],
            "escolas_com_cozinha": agg["IN_COZINHA"],
            "escolas_com_refeitorio": agg["IN_REFEITORIO"],
            "escolas_com_quadra_esportes": agg["IN_QUADRA_ESPORTES_COBERTA"]
            + agg["IN_QUADRA_ESPORTES_DESCOBERTA"],
            "escolas_com_acesso_internet": agg["IN_ACESSO_INTERNET_COMPUTADOR"],
            "escolas_com_acessibilidade_rampas": agg["IN_ACESSIBILIDADE_RAMPAS"],
            "profissionais_com_formacao_pedagogia": agg["QT_PROF_PEDAGOGIA"],
            "profissionais_coordenadores": agg["QT_PROF_COORDENADOR"],
            "profissionais_monitores": agg["QT_PROF_MONITORES"],
        }
    )

    # 8) insere/atualiza
    with engine.begin() as conn:
        conn.execute(
            text(
                f"""
            INSERT INTO public.educacao_basica ({', '.join(df_edu.columns)})
            VALUES ({', '.join(f":{c}" for c in df_edu.columns)})
            ON CONFLICT (codigo_ibge) DO UPDATE
              SET {', '.join(f"{c}=EXCLUDED.{c}" for c in df_edu.columns if c!="codigo_ibge")}
        """
            ),
            df_edu.to_dict(orient="records"),
        )

        conn.execute(
            text(
                f"""
            INSERT INTO public.infraestrutura_basica ({', '.join(df_infra.columns)})
            VALUES ({', '.join(f":{c}" for c in df_infra.columns)})
            ON CONFLICT (codigo_ibge) DO UPDATE
              SET {', '.join(f"{c}=EXCLUDED.{c}" for c in df_infra.columns if c!="codigo_ibge")}
        """
            ),
            df_infra.to_dict(orient="records"),
        )

    logger.info("📘 Educação básica e infraestrutura atualizadas com sucesso.")


def inserir_educacao_tecnica(engine: Engine) -> None:
    logger = get_logger(__name__)

    # Colunas exatas do CSV
    needed = [
        "CO_MUNICIPIO",
        "NU_ANO_CENSO",
        "QT_CURSO_TEC",
        "QT_MAT_CURSO_TEC",
        "QT_CURSO_TEC_CT",
        "QT_MAT_CURSO_TEC_CT",
        "QT_CURSO_TEC_NM",
        "QT_MAT_CURSO_TEC_NM",
        "QT_CURSO_TEC_CONC",
        "QT_MAT_CURSO_TEC_CONC",
        "QT_CURSO_TEC_SUBS",
        "QT_MAT_TEC_SUBS",  # sem "CURSO" no nome
        "QT_CURSO_TEC_EJA",
        "QT_MAT_TEC_EJA",  # sem "CURSO" no nome
    ]

    # 1) Carrega CSV com usecols ajustado
    df = pd.read_csv(
        PATH_CSV_TECNICO,
        sep=";",
        encoding="latin-1",
        usecols=needed,
        low_memory=False,
    )

    # 2) Normaliza e renomeia para schema
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(
        columns={
            "co_municipio": "codigo_ibge",
            "nu_ano_censo": "ano_censo",
            "qt_curso_tec": "qt_curso_tec",
            "qt_mat_curso_tec": "qt_mat_curso_tec",
            "qt_curso_tec_ct": "cursos_integrados_ct",
            "qt_mat_curso_tec_ct": "matriculas_integrados_ct",
            "qt_curso_tec_nm": "cursos_nivel_medio_nm",
            "qt_mat_curso_tec_nm": "matriculas_nivel_medio_nm",
            "qt_curso_tec_conc": "cursos_concomitantes",
            "qt_mat_curso_tec_conc": "matriculas_concomitantes",
            "qt_curso_tec_subs": "cursos_subsequentes",
            "qt_mat_tec_subs": "matriculas_subsequentes",
            "qt_curso_tec_eja": "cursos_eja",
            "qt_mat_tec_eja": "matriculas_eja",
        }
    )

    # 3) Agrega métricas por município+ano
    agg = df.groupby(["codigo_ibge", "ano_censo"], as_index=False).sum(
        numeric_only=True
    )

    # 3.1) Preenche zeros para municípios sem dados técnicos
    # obtém todos os municípios e anos presentes
    munis = pd.read_sql_query("SELECT codigo_ibge FROM public.municipios", engine)
    anos = agg["ano_censo"].unique()
    # cria combinações de municípios x anos
    full_index = pd.MultiIndex.from_product(
        [munis["codigo_ibge"], anos], names=["codigo_ibge", "ano_censo"]
    ).to_frame(index=False)
    # faz left-merge e zera valores faltantes
    agg = full_index.merge(agg, on=["codigo_ibge", "ano_censo"], how="left").fillna(0)

    # 4) Seleciona colunas que o schema espera
    cols = [
        "codigo_ibge",
        "ano_censo",
        "qt_curso_tec",
        "qt_mat_curso_tec",
        "cursos_integrados_ct",
        "matriculas_integrados_ct",
        "cursos_nivel_medio_nm",
        "matriculas_nivel_medio_nm",
        "cursos_concomitantes",
        "matriculas_concomitantes",
        "cursos_subsequentes",
        "matriculas_subsequentes",
        "cursos_eja",
        "matriculas_eja",
    ]
    df_tec = agg[cols].astype(
        {c: int for c in cols if c not in ("codigo_ibge", "ano_censo")}
    )

    # 5) Insere ou atualiza no banco
    with engine.begin() as conn:
        conn.execute(
            text(
                f"""
            INSERT INTO public.educacao_tecnica ({', '.join(cols)})
            VALUES ({', '.join(f":{c}" for c in cols)})
            ON CONFLICT (codigo_ibge, ano_censo) DO UPDATE
              SET {', '.join(f"{c}=EXCLUDED.{c}"
                             for c in cols
                             if c not in ('codigo_ibge','ano_censo'))}
        """
            ),
            df_tec.to_dict(orient="records"),
        )

    logger.info("⚙️ Educação técnica atualizada com sucesso.")


def run() -> None:
    try:
        engine = get_engine()
        inserir_estados_municipios(engine)
        inserir_educacao_basica(engine)
        inserir_educacao_tecnica(engine)
        logger.info("🚀 Dados inseridos com sucesso no banco!")
    except Exception as e:
        logger.critical(f"🔥 Falha ao inserir dados: {e}")


if __name__ == "__main__":
    run()
