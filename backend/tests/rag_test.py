# tests/rag_test.py
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from utils.embedder import get_vectorstore

# 1. Consulta semântica no Chroma
def buscar_documentos(query):
    retriever = get_vectorstore().as_retriever()
    return retriever.get_relevant_documents(query)

# 2. Gera resposta com LLM baseada nos docs
def responder_com_llm(query, documentos):
    context = "\n\n".join([doc.page_content for doc in documentos])
    prompt = PromptTemplate.from_template("""
Você é um especialista da empresa Houer. Responda com base apenas no conteúdo abaixo.

Contexto:
{context}

Pergunta: {query}

Resposta completa e clara:
""")
    chain = prompt | ChatGroq(model_name="gemma2-9b-it")  # ou gemma-2b-it
    return chain.invoke({"context": context, "query": query})

# 3. Execução
if __name__ == "__main__":
    pergunta = "Quem é a Houer e o que ela faz?"
    documentos = buscar_documentos(pergunta)

    print("\n📄 Documentos encontrados:")
    for i, doc in enumerate(documentos, 1):
        print(f"\n--- Documento {i} ---\n{doc.page_content[:400]}...\n")

    resposta = responder_com_llm(pergunta, documentos)
    print("\n🧠 Resposta da LLM:")
    print(resposta)
