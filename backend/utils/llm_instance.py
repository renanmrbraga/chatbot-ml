# utils/llm_instance.py
from langchain_groq import ChatGroq
from utils.config import GROQ_API_KEY

llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=1024
)
