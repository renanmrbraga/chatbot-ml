# backend/core/handlers/fallback_handler.py
from core.router.semantic_city import detectar_cidades
from core.llm.engine import gerar_resposta
from core.agents.educacao_agent import EducacaoAgent
from utils.retriever import buscar_contexto
from utils.logger import get_logger

logger = get_logger(__name__)

def executar_fallback(pergunta: str):
    logger.warning("🟡 Nenhum agente atribuído. Iniciando fallback híbrido.")

    cidade_info = None
    fontes = []
    resposta = "🤖 Não consegui identificar a cidade nem encontrar dados relevantes."
    agente = None

    try:
        # 1️⃣ Detecta cidades
        cidades = detectar_cidades(pergunta)
        cidade_info = cidades[0] if cidades else None

        # 2️⃣ Fallback estruturado: tenta via EducacaoAgent
        if cidade_info:
            logger.info(f"📍 Tentando fallback estruturado via Educação para cidade: {cidade_info['nome']}")
            agente = EducacaoAgent()
            dados = agente.get_dados(pergunta)

            if dados and not (isinstance(dados, dict) and dados.get("tipo") == "erro"):
                fontes = dados.get("fontes", ["PostgreSQL"])
                resposta = dados.get("mensagem") or gerar_resposta(pergunta, dados.get("dados", {}), tema="educacao", fontes=fontes)
                return resposta, fontes, cidade_info, agente
            else:
                logger.warning("⚠️ Fallback estruturado via Educação falhou.")

        # 3️⃣ Fallback semântico: busca por embeddings
        logger.info("📚 Buscando contexto por embeddings (RAG)")
        documentos, metadatas = buscar_contexto(pergunta)

        if documentos:
            contexto = "\n---\n".join(documentos)
            fontes = list(set(meta.get("arquivo", "Desconhecido") for meta in metadatas))
            resposta = gerar_resposta(pergunta, {"context": contexto}, tema="institucional", fontes=fontes)
            return resposta, fontes, None, None

        logger.warning("⚠️ Nenhum documento relevante encontrado via embeddings.")

    except Exception as e:
        logger.error(f"❌ Erro no fallback: {e}")
        resposta = f"❌ Ocorreu um erro no fallback: {e}"

    return resposta, fontes, cidade_info, agente
