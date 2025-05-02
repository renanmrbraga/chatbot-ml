# chatbot-llm/backend/core/agents/tecnica_agent.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
from sqlalchemy import text
import pandas as pd

from database.connection import get_engine
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
from config.dicionarios import TEMPLATE_SINGLE_CITY
from utils.logger import get_logger

logger = get_logger(__name__)


class TecnicaAgent:
    def __init__(self) -> None:
        self.tema = "educacao_tecnica"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self, pergunta: str, cidades_detectadas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        logger.info(f"🔧 Analisando pergunta de educação técnica: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=1)
        if not cidades:
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida para educação técnica.",
                "dados": None,
                "fontes": [],
            }

        nome = cidades[0]["nome"]
        logger.debug(f"📍 Cidade reconhecida: {nome}")

        query = text(
            """
            WITH et_latest AS (
              SELECT
                codigo_ibge,
                MAX(ano_censo) AS ano_tecnica
              FROM public.educacao_tecnica
              GROUP BY codigo_ibge
            )
            SELECT
              m.cidade,
              e.nome                      AS estado,
              et.ano_censo                AS ano_censo,
              et.qt_curso_tec,
              et.qt_mat_curso_tec,
              et.cursos_integrados_ct,
              et.matriculas_integrados_ct,
              et.cursos_nivel_medio_nm,
              et.matriculas_nivel_medio_nm,
              et.cursos_concomitantes,
              et.matriculas_concomitantes,
              et.cursos_subsequentes,
              et.matriculas_subsequentes,
              et.cursos_eja,
              et.matriculas_eja
            FROM public.municipios m
            JOIN public.estados e
              ON e.sigla = m.sigla_estado
            JOIN et_latest el
              ON el.codigo_ibge = m.codigo_ibge
            JOIN public.educacao_tecnica et
              ON et.codigo_ibge = m.codigo_ibge
             AND et.ano_censo = el.ano_tecnica
            WHERE m.cidade = :cidade
        """
        )

        df = pd.read_sql(query, con=get_engine(), params={"cidade": nome})
        if df.empty:
            logger.warning(f"⚠️ Sem dados de educação técnica para {nome}.")
            return {
                "tipo": "erro",
                "mensagem": f"Não foram encontrados dados de educação técnica para {nome}.",
                "dados": None,
                "fontes": [],
            }

        # prepara markdown e lista de registros
        dados_md = df.to_markdown(index=False)
        registros = df.to_dict(orient="records")

        resposta = gerar_resposta(
            pergunta=pergunta,
            dados=registros,
            tema=self.tema,
            fontes=["PostgreSQL"],
            prompt_template=TEMPLATE_SINGLE_CITY,
            dados_formatados=dados_md,
        )

        return {
            "tipo": "resposta",
            "mensagem": resposta,
            "dados": registros,
            "fontes": ["PostgreSQL"],
        }
