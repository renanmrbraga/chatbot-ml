# backend/core/agents/populacao_agent.py
from __future__ import annotations

from typing import Optional, Dict, Any, List
from sqlalchemy import text
import pandas as pd

from database.connection import get_engine
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
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
        cidade_info = cidades[0] if cidades else None

        if not cidade_info:
            logger.warning("❌ Nenhuma cidade reconhecida na pergunta.")
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida na pergunta populacional.",
                "dados": None,
                "fontes": [],
            }

        nome, uf = cidade_info["nome"], cidade_info["uf"]
        logger.debug(f"📍 Cidade reconhecida: {nome} ({uf})")

        try:
            query = text(
                """
                SELECT cidade, estado, populacao_total AS populacao, ano_populacao
                FROM municipios
                WHERE cidade = :nome
                """
            )
            df = pd.read_sql(query, get_engine(), params={"nome": nome})

            if df.empty:
                logger.warning(f"⚠️ Nenhum dado populacional encontrado para {nome}.")
                return {
                    "tipo": "erro",
                    "mensagem": f"Não foram encontrados dados de população para {nome}.",
                    "dados": None,
                    "fontes": [],
                }

            dados_dict: Dict[str, Any] = df.to_dict(orient="records")[0]
            logger.info(f"✅ Dados populacionais encontrados para {nome}.")

            resposta: str = gerar_resposta(
                pergunta=pergunta,
                dados=[dados_dict],
                tema=self.tema,
                fontes=["PostgreSQL"],
            )

            return {
                "tipo": "resposta",
                "mensagem": resposta,
                "dados": [dados_dict],
                "fontes": ["PostgreSQL"],
            }

        except Exception as e:
            logger.error(f"❌ Erro ao consultar dados populacionais: {e}")
            return {
                "tipo": "erro",
                "mensagem": "Erro ao consultar os dados de população.",
                "dados": None,
                "fontes": [],
                "erro": str(e),
            }
