# chatbot-llm/backend/main.py
from __future__ import annotations
from typing import Any, Dict, List, Callable, Awaitable

from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import Response
from pydantic import BaseModel

from config.ngrok import get_ngrok_origin
from core.handlers.chat_handler import processar_pergunta
from core.handlers.session_handler import get_history_for_session
from utils.logger import get_logger
from utils.formatters import nome_agente_formatado
from utils.parser import extrair_nome_uf
from startup.embed_initializer import inicializar_embeddings

logger = get_logger(__name__)
app = FastAPI(title="Chatbot PPPs API", version="1.0")

# Inicia embeddings
inicializar_embeddings()


class ChatRequest(BaseModel):  # type: ignore[misc]
    pergunta: str
    session_id: str


# CORS
ngrok_url = get_ngrok_origin()
allow_origins: List[str] = [
    "https://chatbot-llm.vercel.app",
    "http://localhost:3000",
]
if ngrok_url:
    allow_origins.append(ngrok_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")  # type: ignore[misc]
async def log_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    body = await request.body()
    logger.debug(f"[RAW REQUEST] {body!r}")
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)  # type: ignore[misc]
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    body = await request.body()
    logger.error(f"[VALIDATION ERROR] body={body!r} errors={exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.get("/health")  # type: ignore[misc]
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")  # type: ignore[misc]
def chat_endpoint(req: ChatRequest = Body(...)) -> JSONResponse:
    logger.info(f"💬 Nova pergunta recebida | Sessão: {req.session_id}")

    (
        resposta,
        fontes,
        cidade_info,
        tema,
        agente,
        dados,
        chart_data,
        csv_base64,
        pdf_base64,
    ) = processar_pergunta(req.pergunta, req.session_id)

    cidade, uf = extrair_nome_uf(cidade_info)

    return JSONResponse(
        {
            "resposta": resposta,
            "agente": nome_agente_formatado(agente),
            "fontes": fontes,
            "cidade": cidade,
            "uf": uf,
            "tema": tema,
            "dados_brutos": dados,
            "chart_data": chart_data,
            "csv_base64": csv_base64,
            "pdf_base64": pdf_base64,
            "history": get_history_for_session(req.session_id),
        }
    )
