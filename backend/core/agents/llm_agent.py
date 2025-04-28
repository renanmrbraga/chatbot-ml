# core/agents/llm_agent.py
from typing import Any, Dict, List
from core.llm.engine import gerar_resposta


class LLMAgent:
    def get_dados(
        self, pergunta: str, cidades_detectadas: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # usa seu engine para gerar resposta livre
        content = gerar_resposta(pergunta)
        return {"resposta": content, "fontes": []}
