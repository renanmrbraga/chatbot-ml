# core/agents/economia_agent.py
from __future__ import annotations
import pandas as pd
from typing import Any, Dict, List, Optional
from sqlalchemy import text

from database.connection import get_engine
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
from config.dicionarios import TEMPLATE_SINGLE_CITY
from utils.logger import get_logger

logger = get_logger(__name__)


class EconomiaAgent:
    def __init__(self) -> None:
        self.tema = "economia"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self, pergunta: str, cidades_detectadas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        logger.info(f"💰 Analisando pergunta econômica: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=1)
        if not cidades:
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida para análise econômica.",
                "dados": None,
                "fontes": [],
            }

        nome = cidades[0]["nome"]
        logger.debug(f"📍 Cidade identificada: {nome}")

        try:
            query = text(
                """
                SELECT
                  m.cidade,
                  e.nome          AS estado,
                  m.pib_per_capita,
                  m.ano_pib
                FROM public.municipios m
                JOIN public.estados e
                  ON e.sigla = m.sigla_estado
                WHERE m.cidade = :cidade
                """
            )
            df = pd.read_sql(query, con=get_engine(), params={"cidade": nome})

            if df.empty:
                logger.warning(f"⚠️ Nenhum dado econômico encontrado para {nome}.")
                return {
                    "tipo": "erro",
                    "mensagem": f"Não foram encontrados dados econômicos para {nome}.",
                    "dados": None,
                    "fontes": [],
                }

            # formata só as colunas de interesse
            cols = ["cidade", "estado", "pib_per_capita", "ano_pib"]
            dados_df = df[cols]
            dados_md = dados_df.to_markdown(index=False)

            resposta = gerar_resposta(
                pergunta=pergunta,
                dados=dados_df.to_dict(orient="records"),
                tema=self.tema,
                fontes=["PostgreSQL"],
                prompt_template=TEMPLATE_SINGLE_CITY,
                dados_formatados=dados_md,
            )

            return {
                "tipo": "resposta",
                "mensagem": resposta,
                "dados": dados_df.to_dict(orient="records"),
                "fontes": ["PostgreSQL"],
            }

        except Exception as e:
            logger.error(f"❌ Erro ao consultar dados econômicos: {e}")
            return {
                "tipo": "erro",
                "mensagem": "Ocorreu um erro ao consultar os dados econômicos.",
                "dados": None,
                "fontes": [],
                "erro": str(e),
            }
