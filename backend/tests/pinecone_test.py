# tests/pinecone_test.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")
index_name = os.getenv("PINECONE_INDEX")

# Instancia o cliente Pinecone
pc = Pinecone(api_key=api_key)

# Verifica se o índice existe
indices = pc.list_indexes().names()
if index_name in indices:
    print(f"✅ Conectado ao índice '{index_name}' no ambiente '{environment}'")
else:
    print("❌ Índice não encontrado.")
    print("Índices disponíveis:", indices)
