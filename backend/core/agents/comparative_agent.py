# core/agents/comparative_agent.py
import pandas as pd
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import text
from database.connection import get_engine
from core.router.semantic_city import detectar_cidades
from core.router.semantic_metric import classificar_metrica
from core.llm.engine import gerar_resposta
from config.dicionarios import TEMPLATE_COMPARATIVE
from utils.logger import get_logger
from utils.export_utils import exportar_csv_base64, exportar_pdf_base64

logger = get_logger(__name__)
RespostaTipo = Dict[str, Union[str, List[Dict[str, Any]], Dict[str, Any], None]]


class ComparativeAgent:
    def __init__(self) -> None:
        self.tema = "comparative"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self,
        pergunta: str,
        cidades_detectadas: Optional[List[Dict[str, Any]]] = None,
    ) -> RespostaTipo:
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=2)
        if not cidades or len(cidades) < 2:
            return {
                "tipo": "erro",
                "mensagem": "Mencione pelo menos duas cidades para comparar.",
                "dados": None,
            }
        return self._comparar_cidades(cidades, pergunta)

    def _comparar_cidades(
        self, cidades: List[Dict[str, Any]], pergunta: str
    ) -> RespostaTipo:
        nomes = [c["nome"] for c in cidades]
        engine = get_engine()

        # 🔹 Base: população e PIB
        df_mun = pd.read_sql(
            text(
                """
                SELECT cidade, populacao_total, pib_per_capita
                FROM municipios
                WHERE cidade = ANY(:nomes)
                """
            ),
            con=engine,
            params={"nomes": nomes},
        )

        # 🔹 Educação básica
        df_edu = pd.read_sql(
            text(
                """
                SELECT m.cidade,
                    e.matriculas_ensino_fundamental,
                    e.matriculas_ensino_medio,
                    e.docentes_ensino_fundamental,
                    e.docentes_ensino_medio,
                    e.escolas_ensino_fundamental,
                    e.escolas_ensino_medio
                FROM municipios m
                LEFT JOIN educacao_basica e ON e.codigo_ibge = m.codigo_ibge
                WHERE m.cidade = ANY(:nomes)
                """
            ),
            con=engine,
            params={"nomes": nomes},
        )

        # 🔹 Infraestrutura
        df_infra = pd.read_sql(
            text(
                """
                SELECT m.cidade,
                    i.escolas_com_biblioteca,
                    i.escolas_com_laboratorio_ciencias,
                    i.escolas_com_quadra_esportes,
                    i.profissionais_com_formacao_pedagogia
                FROM municipios m
                LEFT JOIN infraestrutura_basica i ON i.codigo_ibge = m.codigo_ibge
                WHERE m.cidade = ANY(:nomes)
                """
            ),
            con=engine,
            params={"nomes": nomes},
        )

        # 🔹 Cursos técnicos (último ano disponível)
        df_tec = pd.read_sql(
            text(
                """
                SELECT m.cidade,
                    t.qt_curso_tec,
                    t.qt_mat_curso_tec
                FROM municipios m
                LEFT JOIN (
                    SELECT DISTINCT ON (codigo_ibge)
                        codigo_ibge, qt_curso_tec, qt_mat_curso_tec
                    FROM educacao_tecnica
                    ORDER BY codigo_ibge, ano_censo DESC
                ) t ON t.codigo_ibge = m.codigo_ibge
                WHERE m.cidade = ANY(:nomes)
                """
            ),
            con=engine,
            params={"nomes": nomes},
        )

        # 🔁 Merge final por cidade
        df = df_mun.merge(df_edu, on="cidade", how="outer")
        df = df.merge(df_infra, on="cidade", how="outer")
        df = df.merge(df_tec, on="cidade", how="outer")
        df = df.fillna(0)

        # 🔎 Contexto formatado
        contextos = "\n".join(
            [
                f"- **{row['cidade']}**: {', '.join(f'{k}={v:,}' for k, v in row.items() if k != 'cidade')}"
                for _, row in df.iterrows()
            ]
        )

        # 📊 Gráfico e estrutura para resposta
        chart_data = {
            "cidades": nomes,
            "metricas": [col for col in df.columns if col != "cidade"],
            "valores": {
                row["cidade"]: [row[col] for col in df.columns if col != "cidade"]
                for _, row in df.iterrows()
            },
        }

        # 🧠 LLM
        mensagem = gerar_resposta(
            pergunta=pergunta,
            dados=df.to_dict(orient="records"),
            tema=self.tema,
            fontes=["PostgreSQL"],
            prompt_template=TEMPLATE_COMPARATIVE,
            dados_formatados=df.to_markdown(index=False),
            contextos=contextos,
            comparacoes=None,
        )

        return {
            "tipo": "comparativo",
            "mensagem": mensagem,
            "dados": df.to_dict(orient="records"),
            "chart_data": chart_data,
            "csv_base64": exportar_csv_base64(df),
            "pdf_base64": exportar_pdf_base64(df, titulo="Comparativo Multivariável"),
        }
