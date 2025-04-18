# backend/core/agents/comparative_agent.py
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

from database.connection import get_connection
from core.llm.engine import gerar_resposta, gerar_chave_cache, carregar_do_cache, salvar_em_cache
from core.router.semantic_city import detectar_cidades
from core.router.semantic_metric import classificar_metrica
from utils.logger import get_logger
from utils.export_utils import exportar_csv_base64, exportar_pdf_base64

logger = get_logger(__name__)

class ComparativeAgent:
    def __init__(self):
        self.tema = "dashboard"
        logger.debug(f"🧠 {self.__class__.__name__} inicializado.")

    def get_dados(self, pergunta: str, cidades_detectadas: list[dict] = None) -> dict:
        logger.info(f"📊 Analisando pergunta: {pergunta}")
        cidades = cidades_detectadas or detectar_cidades(pergunta, max_cidades=10)

        if not cidades or len(cidades) < 2:
            logger.warning("⚠️ Menos de duas cidades reconhecidas.")
            return {
                "tipo": "erro",
                "mensagem": "A pergunta deve mencionar pelo menos duas cidades para comparação.",
                "dados": None,
                "fontes": []
            }

        return self._comparar_cidades(cidades, pergunta)

    def _comparar_cidades(self, cidades: list[dict], pergunta: str) -> dict:
        nomes = [c["nome"] for c in cidades]
        logger.info(f"🏙️ Cidades para comparação: {', '.join(nomes)}")

        metrica, label = classificar_metrica(pergunta)
        logger.info(f"📈 Métrica classificada: {label} ({metrica or 'comparação geral'})")

        # Monta a query dinamicamente
        if metrica:
            query = f"""
                SELECT cidade, estado, {metrica} AS valor
                FROM dados_municipios
                WHERE cidade = ANY(%s)
            """
        else:
            query = """
                SELECT cidade, estado,
                       populacao, pib_per_capita,
                       matriculas_fundamental, matriculas_medio,
                       escolas_fundamental, escolas_medio,
                       infra_basica_biblioteca, infra_basica_quadra_esportes,
                       cursos_tecnicos_ofertados
                FROM dados_municipios
                WHERE cidade = ANY(%s)
            """

        try:
            with get_connection() as conn:
                df = pd.read_sql(query, conn, params=(nomes,))
        except Exception as e:
            logger.error(f"❌ Erro ao executar query: {e}")
            return {
                "tipo": "erro",
                "mensagem": "Erro ao consultar o banco de dados.",
                "dados": None,
                "fontes": []
            }

        if df.empty or df["cidade"].nunique() < 2:
            logger.warning("⚠️ Menos de duas cidades válidas encontradas no banco.")
            return {
                "tipo": "erro",
                "mensagem": "Não foi possível encontrar dados suficientes para comparar essas cidades.",
                "dados": None,
                "fontes": []
            }

        dados_dict = df.to_dict(orient="records")
        chave = gerar_chave_cache(pergunta, df.to_markdown(index=False))
        resposta_cache = carregar_do_cache(chave)

        if resposta_cache:
            resposta = resposta_cache
            logger.debug("⚡ Resposta carregada do cache.")
        else:
            resposta = gerar_resposta(
                pergunta=pergunta,
                dados=dados_dict,
                tema=self.tema,
                fontes=["PostgreSQL"]
            )
            salvar_em_cache(chave, resposta)

        imagem_base64 = ""
        if "valor" in df.columns:
            imagem_base64 = self._gerar_grafico(df, coluna="valor", label=label)
        elif "populacao" in df.columns:
            imagem_base64 = self._gerar_grafico(df, coluna="populacao", label="População")

        return {
            "tipo": "comparativo",
            "mensagem": resposta,
            "dados": dados_dict,
            "fontes": ["PostgreSQL"],
            "imagem_base64": imagem_base64,
            "csv_base64": exportar_csv_base64(df),
            "pdf_base64": exportar_pdf_base64(df, titulo=f"Comparação: {label}")
        }

    def _gerar_grafico(self, df: pd.DataFrame, coluna: str, label: str) -> str:
        if coluna not in df.columns:
            logger.warning(f"⚠️ Coluna '{coluna}' não encontrada para gráfico.")
            return ""

        try:
            df_sorted = df.sort_values(by=coluna, ascending=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(df_sorted["cidade"], df_sorted[coluna], color="#4c8bf5")
            ax.set_xlabel(label)
            ax.set_title(f"Comparação: {label}")
            ax.grid(True, linestyle="--", alpha=0.5)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format="png")
            plt.close(fig)
            buf.seek(0)
            return base64.b64encode(buf.read()).decode("utf-8")

        except Exception as e:
            logger.error(f"❌ Erro ao gerar gráfico para coluna '{coluna}': {e}")
            return ""
