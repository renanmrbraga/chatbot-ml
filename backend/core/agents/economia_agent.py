# backend/core/agents/economia_agent.py
from database.connection import get_connection
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
from utils.logger import get_logger

logger = get_logger(__name__)

class EconomiaAgent:
    def __init__(self):
        self.tema = "economia"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(self, pergunta: str, cidades_detectadas: list[dict] = None) -> dict:
        logger.info(f"💰 Analisando pergunta econômica: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=1)
        cidade_info = cidades[0] if cidades else None

        if not cidade_info:
            logger.warning("❌ Nenhuma cidade reconhecida para análise econômica.")
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível identificar uma cidade válida para análise econômica.",
                "dados": None,
                "fontes": []
            }

        nome, uf = cidade_info["nome"], cidade_info["uf"]
        logger.debug(f"📍 Cidade identificada: {nome} ({uf})")

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT cidade, estado, pib_per_capita, ano_pib
                        FROM dados_municipios
                        WHERE cidade = %s
                    """, (nome,))
                    row = cur.fetchone()
                    colnames = [desc[0] for desc in cur.description]

            if not row:
                logger.warning(f"⚠️ Nenhum dado econômico encontrado para {nome}.")
                return {
                    "tipo": "erro",
                    "mensagem": f"Não foram encontrados dados econômicos para {nome}.",
                    "dados": None,
                    "fontes": []
                }

            dados_dict = dict(zip(colnames, row))
            logger.info(f"✅ Dados econômicos recuperados com sucesso para {nome}.")

            resposta = gerar_resposta(
                pergunta=pergunta,
                dados=[dados_dict],
                tema=self.tema,
                fontes=["PostgreSQL"]
            )

            return {
                "tipo": "resposta",
                "mensagem": resposta,
                "dados": [dados_dict],
                "fontes": ["PostgreSQL"]
            }

        except Exception as e:
            logger.error(f"❌ Erro ao consultar dados econômicos: {e}")
            return {
                "tipo": "erro",
                "mensagem": "Ocorreu um erro ao consultar os dados econômicos.",
                "dados": None,
                "fontes": [],
                "erro": str(e)
            }
