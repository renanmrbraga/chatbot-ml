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
        metric_col, label = classificar_metrica(pergunta)

        # Escolhe SQL conforme métrica
        if metric_col in ("populacao_total", "pib_per_capita"):
            sql = text(
                f"""
                SELECT m.cidade, m.{metric_col} AS valor
                  FROM public.municipios m
                 WHERE m.cidade = ANY(:names)
            """
            )
        elif metric_col.startswith("escolas_com_") or metric_col.startswith(
            "profissionais_"
        ):
            sql = text(
                f"""
                SELECT m.cidade, i.{metric_col} AS valor
                  FROM public.municipios m
                  LEFT JOIN public.infraestrutura_basica i
                    ON i.codigo_ibge = m.codigo_ibge
                 WHERE m.cidade = ANY(:names)
            """
            )
        elif any(
            metric_col.startswith(pref)
            for pref in ("matriculas_", "turmas_", "docentes_", "escolas_")
        ):
            sql = text(
                f"""
                SELECT m.cidade, d.{metric_col} AS valor
                  FROM public.municipios m
                  LEFT JOIN public.educacao_basica d
                    ON d.codigo_ibge = m.codigo_ibge
                 WHERE m.cidade = ANY(:names)
            """
            )
        else:
            # educacao_tecnica: pega censo mais recente
            sql = text(
                f"""
                SELECT m.cidade, t.{metric_col} AS valor
                  FROM public.municipios m
                  LEFT JOIN (
                      SELECT DISTINCT ON (codigo_ibge) codigo_ibge, {metric_col}
                        FROM public.educacao_tecnica
                       ORDER BY codigo_ibge, ano_censo DESC
                  ) t
                    ON t.codigo_ibge = m.codigo_ibge
                 WHERE m.cidade = ANY(:names)
            """
            )

        # Executa consulta
        engine = get_engine()
        df = pd.read_sql(sql, con=engine, params={"names": nomes})

        # 1) Contextos
        records = df.to_dict(orient="records")
        contextos = "\n".join(f"- **{r['cidade']}:** {r['valor']:,}" for r in records)

        # 2) Comparações simples (duas cidades)
        if len(records) >= 2:
            c1, c2 = records[0], records[1]
            diff = abs((c1.get("valor") or 0) - (c2.get("valor") or 0))
            comparacoes = f"{c1['cidade']}: {c1['valor']:,} vs {c2['cidade']}: {c2['valor']:,} → diferença de {diff:,}"
        else:
            comparacoes = None

        # 3) Formatação
        dados_md = df.to_markdown(index=False)
        chart_data = {
            "cidades": nomes,
            "metricas": [metric_col],
            "valores": {r["cidade"]: [r.get("valor") or 0] for r in records},
        }

        # Gera mensagem via LLM
        mensagem = gerar_resposta(
            pergunta=pergunta,
            dados=records,
            tema=self.tema,
            fontes=["PostgreSQL"],
            prompt_template=TEMPLATE_COMPARATIVE,
            dados_formatados=dados_md,
            contextos=contextos,
            comparacoes=comparacoes,
        )

        return {
            "tipo": "comparativo",
            "mensagem": mensagem,
            "dados": records,
            "chart_data": chart_data,
            "csv_base64": exportar_csv_base64(df),
            "pdf_base64": exportar_pdf_base64(df, titulo=f"Comparação: {label}"),
        }
