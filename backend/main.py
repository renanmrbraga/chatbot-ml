# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.handlers.chat_handler import processar_pergunta
from core.handlers.session_handler import get_history_for_session
from utils.logger import get_logger
from utils.formatters import nome_agente_formatado
from utils.parser import extrair_nome_uf

from startup.embed_initializer import inicializar_embeddings

logger = get_logger(__name__)
app = FastAPI(title="Chatbot PPPs API", version="1.0")

inicializar_embeddings()

# -------------------- CORS -------------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Schemas -------------------- #
class ChatRequest(BaseModel):
    pergunta: str
    session_id: str

# -------------------- Endpoints -------------------- #
@app.get("/")
def health():
    return {"status": "ok", "mensagem": "✅ Chatbot PPPs rodando com sucesso."}

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    logger.info(f"💬 Nova pergunta recebida | Sessão: {req.session_id}")

    resposta, fontes, cidade_info, tema, agente, dados, dashboard_base64, csv_base64, pdf_base64 = processar_pergunta(
        req.pergunta, req.session_id
    )

    cidade, uf = extrair_nome_uf(cidade_info)

    # 🔒 Serialização segura dos dados
    dados_serializaveis = {}
    if isinstance(dados, dict):
        dados_serializaveis = {
            k: v for k, v in dados.items()
            if not callable(v) and not hasattr(v, "__dict__")
        }
    elif isinstance(dados, list):
        dados_serializaveis = dados

    return JSONResponse({
        "resposta": resposta,
        "agente": nome_agente_formatado(agente),
        "fontes": fontes,
        "cidade": cidade,
        "uf": uf,
        "tema": tema,
        "dados_brutos": dados_serializaveis,
        "dashboard_base64": dashboard_base64,
        "csv_base64": csv_base64,
        "pdf_base64": pdf_base64,
        "history": get_history_for_session(req.session_id),
    })
