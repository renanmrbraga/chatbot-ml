# config/dicionarios.py
from __future__ import annotations

import json
from typing import Dict, List, Optional

from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

# === MÉTRICAS ===
METRICAS_VALIDAS: Dict[str, str] = {
    "populacao_total": "População Total",
    "pib_per_capita": "PIB per Capita",
    "matriculas_educacao_infantil": "Matrículas - Educação Infantil",
    "matriculas_ensino_fundamental": "Matrículas - Ensino Fundamental",
    "matriculas_ensino_medio": "Matrículas - Ensino Médio",
    "matriculas_eja": "Matrículas - EJA",
    "matriculas_educacao_especial": "Matrículas - Educação Especial",
    "matriculas_ensino_tecnico": "Matrículas - Curso Técnico",
    "turmas_educacao_infantil": "Turmas - Educação Infantil",
    "turmas_ensino_fundamental": "Turmas - Ensino Fundamental",
    "turmas_ensino_medio": "Turmas - Ensino Médio",
    "turmas_eja": "Turmas - EJA",
    "turmas_educacao_especial": "Turmas - Educação Especial",
    "turmas_ensino_tecnico": "Turmas - Curso Técnico",
    "docentes_educacao_infantil": "Docentes - Educação Infantil",
    "docentes_ensino_fundamental": "Docentes - Ensino Fundamental",
    "docentes_ensino_medio": "Docentes - Ensino Médio",
    "docentes_eja": "Docentes - EJA",
    "docentes_educacao_especial": "Docentes - Educação Especial",
    "docentes_ensino_tecnico": "Docentes - Curso Técnico",
    "escolas_educacao_infantil": "Escolas - Educação Infantil",
    "escolas_ensino_fundamental": "Escolas - Ensino Fundamental",
    "escolas_ensino_medio": "Escolas - Ensino Médio",
    "escolas_eja": "Escolas - EJA",
    "escolas_educacao_especial": "Escolas - Educação Especial",
    "escolas_ensino_tecnico": "Escolas - Curso Técnico",
    "escolas_com_biblioteca": "Infraestrutura - Bibliotecas",
    "escolas_com_laboratorio_ciencias": "Infraestrutura - Lab. Ciências",
    "escolas_com_laboratorio_informatica": "Infraestrutura - Lab. Informática",
    "escolas_com_cozinha": "Infraestrutura - Cozinhas",
    "escolas_com_refeitorio": "Infraestrutura - Refeitórios",
    "escolas_com_quadra_esportes": "Infraestrutura - Quadras",
    "escolas_com_acesso_internet": "Infraestrutura - Internet",
    "escolas_com_acessibilidade_rampas": "Infraestrutura - Acessibilidade",
    "profissionais_com_formacao_pedagogia": "Professores com Formação Pedagógica",
    "profissionais_coordenadores": "Coordenadores Pedagógicos",
    "profissionais_monitores": "Monitores Educacionais",
    "total_cursos_tecnicos": "Cursos Técnicos Ofertados",
}

HEURISTICAS: Dict[str, str] = {
    "população": "populacao_total",
    "habitantes": "populacao_total",
    "total de pessoas": "populacao_total",
    "quantidade de habitantes": "populacao_total",
    "número de habitantes": "populacao_total",
    "demografia": "populacao_total",
    "pib": "pib_per_capita",
    "renda": "pib_per_capita",
    "renda média": "pib_per_capita",
    "matrículas": "matriculas_ensino_fundamental",
    "ensino médio": "matriculas_ensino_medio",
    "educação infantil": "matriculas_educacao_infantil",
    "escolas": "escolas_ensino_fundamental",
    "biblioteca": "escolas_com_biblioteca",
    "bibliotecas": "escolas_com_biblioteca",
    "quadra": "escolas_com_quadra_esportes",
    "quadras": "escolas_com_quadra_esportes",
    "cozinha": "escolas_com_cozinha",
    "internet": "escolas_com_acesso_internet",
    "laboratório": "escolas_com_laboratorio_informatica",
    "laboratórios": "escolas_com_laboratorio_informatica",
    "curso técnico": "total_cursos_tecnicos",
    "cursos técnicos": "total_cursos_tecnicos",
    "técnico": "total_cursos_tecnicos",
}

ESTADOS: Dict[str, List[str]] = {
    "AC": ["acre", "ac"],
    "AL": ["alagoas", "al"],
    "AP": ["amapa", "ap"],
    "AM": ["amazonas", "am"],
    "BA": ["bahia", "ba"],
    "CE": ["ceara", "ce"],
    "DF": ["distrito federal", "df", "brasilia"],
    "ES": ["espirito santo", "es"],
    "GO": ["goias", "go"],
    "MA": ["maranhao", "ma"],
    "MT": ["mato grosso", "mt"],
    "MS": ["mato grosso do sul", "ms"],
    "MG": ["minas gerais", "mg"],
    "PA": ["para", "pa"],
    "PB": ["paraiba", "pb"],
    "PR": ["parana", "pr"],
    "PE": ["pernambuco", "pe"],
    "PI": ["piaui", "pi"],
    "RJ": ["rio de janeiro", "rj", "carioca"],
    "RN": ["rio grande do norte", "rn"],
    "RS": ["rio grande do sul", "rs", "gaucho", "gaúcho"],
    "RO": ["rondonia", "ro"],
    "RR": ["roraima", "rr"],
    "SC": ["santa catarina", "sc", "catarinense"],
    "SP": ["sao paulo", "sp", "paulista"],
    "SE": ["sergipe", "se"],
    "TO": ["tocantins", "to"],
}

TEMPLATE: str = """
Você é um analista de dados especialista em políticas públicas municipais.

Sua missão é analisar os dados abaixo e responder à pergunta do usuário com **clareza, lógica e profundidade interpretativa**.

⚠️ Instruções obrigatórias:
- NÃO invente dados ou conclusões.
- NÃO responda em formato de tabela.
- NÃO use frases genéricas como "é importante destacar...".

✅ Sua resposta deve conter 3 blocos:
1. **Contexto geral**: Diga o que os dados mostram em linhas gerais.
2. **Análise comparativa (se houver mais de uma cidade)**: Destaque as principais diferenças e números relevantes.
3. **Conclusão objetiva**: Diga o que pode ser inferido com base apenas nos dados fornecidos.

---

📌 Pergunta do usuário:
{pergunta}

📊 Dados disponíveis:
{dados_formatados}

📚 Tema: {tema}
📁 Fontes: {fontes}

---

Responda como se estivesse apresentando para um gestor público ou analista técnico. Evite rodeios. Seja claro e direto.
"""

TEMPLATE_METRICA: str = f"""
Você é um classificador de métricas para dashboards comparativos entre cidades brasileiras.

Com base na pergunta do usuário, identifique a melhor coluna da tabela `municipios` para gerar o gráfico comparativo entre cidades.

⚠️ Importante:
- A infraestrutura escolar refere-se **apenas às escolas de Educação Infantil, Ensino Fundamental e Médio**.
- **Não inclui escolas técnicas ou cursos técnicos**.

Use apenas uma das seguintes colunas:
{json.dumps(METRICAS_VALIDAS, indent=2, ensure_ascii=False)}

Retorne apenas um JSON válido no formato:
{{ "coluna": "matriculas_fundamental", "label": "Matrículas - Ensino Fundamental" }}

Pergunta: "{{pergunta}}"
"""

TEMPLATE_TEMA: str = """
Você é um classificador semântico para um chatbot sobre políticas públicas de cidades brasileiras.

Classifique a pergunta abaixo em **apenas um** dos seguintes temas:

- educacao
- populacao
- economia
- comparative (se for uma pergunta que compara duas ou mais cidades)

⚠️ Se a pergunta for muito vaga ou não pertencer a nenhum desses temas, **responda com \"tema\": \"llm\"**.

Retorne **apenas o JSON**, sem explicações, neste formato:

{"tema": "educacao"}

Pergunta: "{pergunta}"
"""

llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=1024,
)

TEMAS_VALIDOS: List[str] = ["educacao", "populacao", "economia", "comparative"]

NOMES_AGENTES: Dict[str, str] = {
    "EducacaoAgent": "Educação",
    "PopulacaoAgent": "População",
    "EconomiaAgent": "Economia",
    "InstitucionalAgent": "Institucional",
    "LLM": "LLM (Fallback)",
}


# Carregamento "lazy" dos agentes para evitar import circular
def load_agents() -> Dict[str, type]:
    from core.agents.educacao_agent import EducacaoAgent
    from core.agents.populacao_agent import PopulacaoAgent
    from core.agents.economia_agent import EconomiaAgent
    from core.agents.institucional_agent import InstitucionalAgent
    from core.agents.comparative_agent import ComparativeAgent

    return {
        "educacao": EducacaoAgent,
        "populacao": PopulacaoAgent,
        "economia": EconomiaAgent,
        "comparative": ComparativeAgent,
        "institucional": InstitucionalAgent,
    }


_AGENTS_CACHE: Optional[Dict[str, type]] = None


def get_agents_disponiveis() -> Dict[str, type]:
    global _AGENTS_CACHE
    if _AGENTS_CACHE is None:
        _AGENTS_CACHE = load_agents()
    return _AGENTS_CACHE
