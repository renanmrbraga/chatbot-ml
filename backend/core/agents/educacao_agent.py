# core/agents/educacao_agent.py
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


class EducacaoAgent:
    def __init__(self) -> None:
        self.tema = "educacao"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(
        self, pergunta: str, cidades_detectadas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        logger.info(f"📚 Analisando pergunta educacional: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=1)
        if not cidades:
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida na pergunta educacional.",
                "dados": None,
                "fontes": [],
            }

        nome = cidades[0]["nome"]
        logger.debug(f"📍 Cidade reconhecida: {nome}")

        # Busca todos os campos de educacao_basica + infraestrutura_basica
        qry = text(
            """
            SELECT
              m.cidade,
              e.nome                                        AS estado,

              -- dados de educação básica
              eb.ano_dados,
              eb.matriculas_educacao_infantil,
              eb.matriculas_ensino_fundamental,
              eb.matriculas_ensino_medio,
              eb.matriculas_eja,
              eb.matriculas_educacao_especial,
              eb.matriculas_ensino_tecnico,

              eb.turmas_educacao_infantil,
              eb.turmas_ensino_fundamental,
              eb.turmas_ensino_medio,
              eb.turmas_eja,
              eb.turmas_educacao_especial,
              eb.turmas_ensino_tecnico,

              eb.docentes_educacao_infantil,
              eb.docentes_ensino_fundamental,
              eb.docentes_ensino_medio,
              eb.docentes_eja,
              eb.docentes_educacao_especial,
              eb.docentes_ensino_tecnico,

              eb.escolas_educacao_infantil,
              eb.escolas_ensino_fundamental,
              eb.escolas_ensino_medio,
              eb.escolas_eja,
              eb.escolas_educacao_especial,
              eb.escolas_ensino_tecnico,

              -- infraestrutura da educação básica
              ib.escolas_com_biblioteca,
              ib.escolas_com_laboratorio_ciencias,
              ib.escolas_com_laboratorio_informatica,
              ib.escolas_com_cozinha,
              ib.escolas_com_refeitorio,
              ib.escolas_com_quadra_esportes,
              ib.escolas_com_acesso_internet,
              ib.escolas_com_acessibilidade_rampas,

              ib.profissionais_com_formacao_pedagogia,
              ib.profissionais_coordenadores,
              ib.profissionais_monitores

            FROM public.municipios m
            JOIN public.estados e
              ON e.sigla = m.sigla_estado

            LEFT JOIN public.educacao_basica eb
              ON eb.codigo_ibge = m.codigo_ibge

            LEFT JOIN public.infraestrutura_basica ib
              ON ib.codigo_ibge = m.codigo_ibge

            WHERE m.cidade = :cidade
        """
        )

        df = pd.read_sql(qry, con=get_engine(), params={"cidade": nome})

        if df.empty:
            logger.warning(f"⚠️ Sem dados educacionais para {nome}.")
            return {
                "tipo": "erro",
                "mensagem": f"Não foram encontrados dados de educação básica para {nome}.",
                "dados": None,
                "fontes": [],
            }

        # Formata para o LLM
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
