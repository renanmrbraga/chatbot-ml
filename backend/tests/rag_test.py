# chatbot-llm/backend/tests/rag_test.py
from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from utils.embedder import get_vectorstore


def buscar_documentos(query: str) -> List[Document]:
    """
    Busca os documentos mais relevantes no vectorstore do Pinecone.

    Retorna uma lista de Document, garantindo tipagem correta.
    """
    retriever = get_vectorstore().as_retriever()
    documentos: List[Document] = retriever.get_relevant_documents(query)
    return documentos


def responder_com_llm(query: str, documentos: List[Document]) -> str:
    """
    Gera uma resposta baseada nos documentos fornecidos usando o modelo ChatGroq.

    Recebe a query e os documentos, retorna sempre uma string.
    """
    # Concatena todo o conteúdo dos documentos
    context: str = "\n\n".join(doc.page_content for doc in documentos)

    prompt: PromptTemplate = PromptTemplate.from_template(
        """
Você é um especialista da empresa Houer. Responda com base apenas no conteúdo abaixo.

Contexto:
{context}

Pergunta: {query}

Resposta completa e clara:
"""
    )
    # Monta a chain e invoca
    chain = prompt | ChatGroq(model_name="gemma2-9b-it")
    resposta_obj = chain.invoke({"context": context, "query": query})
    # Assegura que retornamos sempre str
    return str(resposta_obj)


if __name__ == "__main__":
    pergunta: str = "Quem é a Houer e o que ela faz?"
    documentos: List[Document] = buscar_documentos(pergunta)

    print("\n📄 Documentos encontrados:")
    for i, doc in enumerate(documentos, start=1):
        snippet = doc.page_content[:400].replace("\n", " ")
        print(f"\n--- Documento {i} ---\n{snippet}...\n")

    resposta_final: str = responder_com_llm(pergunta, documentos)
    print("\n🧠 Resposta da LLM:")
    print(resposta_final)
