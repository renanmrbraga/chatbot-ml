# backend/core/handlers/chat_handler.py
from core.handlers.fallback_handler import executar_fallback
from core.handlers.log_handler import registrar_log
from core.handlers.session_handler import registrar_resposta
from core.router.interpreter import interpretar_pergunta
from utils.logger import get_logger
from utils.parser import extrair_nome_uf  # ✅ nova importação

logger = get_logger(__name__)


def processar_pergunta(pergunta: str, session_id: str):
    logger.info(f"📥 Nova pergunta recebida: {pergunta}")

    # Valores padrão
    resposta = "❌ Não consegui responder sua pergunta."
    fontes = []
    dashboard_base64 = None
    csv_base64 = None
    pdf_base64 = None
    dados = None

    # === Interpretação ===
    agente, tema, cidades = interpretar_pergunta(pergunta)
    agente_nome = agente.__class__.__name__ if agente else "LLM"
    cidade_info = cidades[0] if cidades else None

    # === Execução do agente ===
    if agente:
        try:
            dados = agente.get_dados(pergunta, cidades_detectadas=cidades)
        except Exception as e:
            logger.error(f"❌ Erro ao obter dados com agente {agente_nome}: {e}")
            dados = None

    # === Resposta com dados ===
    if isinstance(dados, dict):
        if dados.get("tipo") == "erro":
            resposta = dados["mensagem"]
        else:
            resposta = dados.get("mensagem", resposta)
            fontes = dados.get("fontes", ["PostgreSQL"])
            dashboard_base64 = dados.get("imagem_base64")
            csv_base64 = dados.get("csv_base64")
            pdf_base64 = dados.get("pdf_base64")

            cidade_info = dados.get("cidade_info") or cidade_info or (
                dados["dados"][0] if isinstance(dados.get("dados"), list) and dados["dados"] else None
            )

    else:
        resposta, fontes, cidade_info, agente = executar_fallback(pergunta)
        agente_nome = agente.__class__.__name__ if agente else "LLM"

    # === Registro ===
    try:
        registrar_resposta(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta,
            agente_nome=agente_nome,
            fontes=fontes,
            cidades=[c["nome"] for c in cidades],
            tema=tema
        )
        registrar_log(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta,
            fontes=fontes,
            cidade_info=cidade_info,
            tema=tema
        )
    except Exception as e:
        logger.error(f"❌ Erro ao registrar log no banco | Sessão: {session_id} | Erro: {e}")

    logger.info(f"✅ Resposta final pronta | Agente: {agente_nome} | Fontes: {fontes}")

    return resposta, fontes, cidade_info, tema, agente, dados, dashboard_base64, csv_base64, pdf_base64
