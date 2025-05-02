# chatbot-llm/backend/tests/pinecone_test.py
from typing import Optional
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

api_key: Optional[str] = os.getenv("PINECONE_API_KEY")
environment: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
index_name: Optional[str] = os.getenv("PINECONE_INDEX")

if api_key is None or index_name is None:
    raise ValueError("❌ API Key ou nome do índice Pinecone não configurado.")

# Instancia o cliente Pinecone
pc = Pinecone(api_key=api_key)

# Verifica se o índice existe
indices: list[str] = pc.list_indexes().names()
if index_name in indices:
    print(f"✅ Conectado ao índice '{index_name}' no ambiente '{environment}'")
else:
    print("❌ Índice não encontrado.")
    print("Índices disponíveis:", indices)
