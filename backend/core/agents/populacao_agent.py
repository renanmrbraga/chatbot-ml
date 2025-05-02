# chatbot-llm/backend/core/agents/populacao_agent.py
from __future__ import annotations

from typing import Optional, Dict, Any, List
from sqlalchemy import text
import pandas as pd

from database.connection import get_engine
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
from config.dicionarios import TEMPLATE_SINGLE_CITY
from utils.logger import get_logger

logger = get_logger(__name__)


class PopulacaoAgent:
    def __init__(self) -> None:
        self.tema: str = "populacao"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self, pergunta: str, cidades_detectadas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        logger.info(f"👥 Analisando pergunta sobre população: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=1)
        if not cidades:
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida.",
                "dados": None,
                "fontes": [],
            }

        nome = cidades[0]["nome"]
        df = pd.read_sql(
            text(
                """
                SELECT
                  m.cidade,
                  m.populacao_total AS populacao,
                  m.ano_populacao
                FROM public.municipios m
                WHERE m.cidade = :nome
            """
            ),
            con=get_engine(),
            params={"nome": nome},
        )
        if df.empty:
            return {
                "tipo": "erro",
                "mensagem": f"Sem dados de população para {nome}.",
                "dados": None,
                "fontes": [],
            }

        # Dados formatados como markdown
        dados_md = df.to_markdown(index=False)

        # CHAMA SEMPRE O TEMPLATE ÚNICO
        resposta = gerar_resposta(
            pergunta=pergunta,
            dados=[df.to_dict(orient="records")[0]],
            tema=self.tema,
            fontes=["PostgreSQL"],
            prompt_template=TEMPLATE_SINGLE_CITY,
            dados_formatados=dados_md,
        )

        return {
            "tipo": "resposta",
            "mensagem": resposta,
            "dados": df.to_dict(orient="records"),
            "fontes": ["PostgreSQL"],
        }
