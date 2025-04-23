# core/agents/economia_agent.py
from __future__ import annotations

import pandas as pd
from typing import Any, Dict, List, Optional

from database.connection import get_engine
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
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
        cidade_info = cidades[0] if cidades else None

        if not cidade_info:
            logger.warning("❌ Nenhuma cidade reconhecida para análise econômica.")
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida para análise econômica.",
                "dados": None,
                "fontes": [],
            }

        nome, uf = cidade_info["nome"], cidade_info["uf"]
        logger.debug(f"📍 Cidade identificada: {nome} ({uf})")

        try:
            query = """
                SELECT cidade, estado, pib_per_capita, ano_pib
                FROM municipios
                WHERE cidade = %(cidade)s
            """
            df = pd.read_sql(query, con=get_engine(), params={"cidade": nome})

            if df.empty:
                logger.warning(f"⚠️ Nenhum dado econômico encontrado para {nome}.")
                return {
                    "tipo": "erro",
                    "mensagem": f"Não foram encontrados dados econômicos para {nome}.",
                    "dados": None,
                    "fontes": [],
                }

            dados_dict: List[Dict[str, Any]] = df.to_dict(orient="records")
            logger.info(f"✅ Dados econômicos recuperados com sucesso para {nome}.")

            resposta = gerar_resposta(
                pergunta=pergunta,
                dados=dados_dict,
                tema=self.tema,
                fontes=["PostgreSQL"],
            )

            return {
                "tipo": "resposta",
                "mensagem": resposta,
                "dados": dados_dict,
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
