# chatbot-llm/backend/config/dicionarios.py
from __future__ import annotations

import json
import re
from typing import Dict, List, Optional

from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

# === MÉTRICAS ===
METRICAS_VALIDAS: Dict[str, str] = {
    # Demografia e economia
    "populacao_total": "População Total",
    "pib_per_capita": "PIB per Capita",
    # Matrículas
    "matriculas_educacao_infantil": "Matrículas - Educação Infantil",
    "matriculas_ensino_fundamental": "Matrículas - Ensino Fundamental",
    "matriculas_ensino_medio": "Matrículas - Ensino Médio",
    "matriculas_eja": "Matrículas - EJA",
    "matriculas_educacao_especial": "Matrículas - Educação Especial",
    "matriculas_ensino_tecnico": "Matrículas - Curso Técnico Básico",
    # Turmas
    "turmas_educacao_infantil": "Turmas - Educação Infantil",
    "turmas_ensino_fundamental": "Turmas - Ensino Fundamental",
    "turmas_ensino_medio": "Turmas - Ensino Médio",
    "turmas_eja": "Turmas - EJA",
    "turmas_educacao_especial": "Turmas - Educação Especial",
    "turmas_ensino_tecnico": "Turmas - Curso Técnico Básico",
    # Docentes
    "docentes_educacao_infantil": "Docentes - Educação Infantil",
    "docentes_ensino_fundamental": "Docentes - Ensino Fundamental",
    "docentes_ensino_medio": "Docentes - Ensino Médio",
    "docentes_eja": "Docentes - EJA",
    "docentes_educacao_especial": "Docentes - Educação Especial",
    "docentes_ensino_tecnico": "Docentes - Curso Técnico Básico",
    # Escolas
    "escolas_educacao_infantil": "Escolas - Educação Infantil",
    "escolas_ensino_fundamental": "Escolas - Ensino Fundamental",
    "escolas_ensino_medio": "Escolas - Ensino Médio",
    "escolas_eja": "Escolas - EJA",
    "escolas_educacao_especial": "Escolas - Educação Especial",
    "escolas_ensino_tecnico": "Escolas - Curso Técnico Básico",
    # Infraestrutura
    "escolas_com_biblioteca": "Infraestrutura - Bibliotecas",
    "escolas_com_laboratorio_ciencias": "Infraestrutura - Lab. Ciências",
    "escolas_com_laboratorio_informatica": "Infraestrutura - Lab. Informática",
    "escolas_com_cozinha": "Infraestrutura - Cozinhas",
    "escolas_com_refeitorio": "Infraestrutura - Refeitórios",
    "escolas_com_quadra_esportes": "Infraestrutura - Quadras",
    "escolas_com_acesso_internet": "Infraestrutura - Internet",
    "escolas_com_acessibilidade_rampas": "Infraestrutura - Acessibilidade",
    # Profissionais de apoio
    "profissionais_com_formacao_pedagogia": "Profissionais com Formação Pedagógica",
    "profissionais_coordenadores": "Coordenadores Pedagógicos",
    "profissionais_monitores": "Monitores Educacionais",
    # Cursos Técnicos (educacao_tecnica)
    "qt_curso_tec": "Cursos Técnicos - Total de Cursos",
    "qt_mat_curso_tec": "Matrículas - Total de Cursos Técnicos",
    "cursos_integrados_ct": "Cursos Técnicos Integrados (CT)",
    "matriculas_integrados_ct": "Matrículas - Cursos Integrados (CT)",
    "cursos_nivel_medio_nm": "Cursos Técnicos Nível Médio (NM)",
    "matriculas_nivel_medio_nm": "Matrículas - Cursos Nível Médio (NM)",
    "cursos_concomitantes": "Cursos Técnicos Concomitantes",
    "matriculas_concomitantes": "Matrículas - Cursos Concomitantes",
    "cursos_subsequentes": "Cursos Técnicos Subsequentes",
    "matriculas_subsequentes": "Matrículas - Cursos Subsequentes",
    "cursos_eja": "Cursos Técnicos EJA",
    "matriculas_eja": "Matrículas - Cursos EJA",
}

# — seus padrões comparativos fixos —
COMPARATIVE_PATTERNS: List[str] = [
    r"\bcompare\b",
    r"\bcomparar\b",
    r"\bversus\b",
    r"\bvs\b",
    r"\bcontra\b",
    r"\bmais desenvolvida\b",
    r"\bmenor desigualdade\b",
]

# — heurísticas mapeando termo de busca → coluna do banco —
HEURISTICAS: Dict[str, str] = {
    # População
    "população total": "populacao_total",
    "total da população": "populacao_total",
    "população residente": "populacao_total",
    "população estimada": "populacao_total",
    "população projetada": "populacao_total",
    "população municipal": "populacao_total",
    "população": "populacao_total",
    "populacao": "populacao_total",
    "habitantes": "populacao_total",
    "total de pessoas": "populacao_total",
    "total de moradores": "populacao_total",
    "moradores": "populacao_total",
    "residentes": "populacao_total",
    "quantidade de habitantes": "populacao_total",
    "número de habitantes": "populacao_total",
    "estimativa populacional": "populacao_total",
    "ano de referência população": "ano_populacao",
    "ano de referência da população": "ano_populacao",
    "ano da população": "ano_populacao",
    "ano populacao": "ano_populacao",
    # Economia
    "pib per capita": "pib_per_capita",
    "pib percapita": "pib_per_capita",
    "pib": "pib_per_capita",
    "produto interno bruto per capita": "pib_per_capita",
    "produto interno bruto": "pib_per_capita",
    "valor do pib per capita": "pib_per_capita",
    "valor do pib": "pib_per_capita",
    "renda per capita": "pib_per_capita",
    "renda média per capita": "pib_per_capita",
    "ano do pib": "ano_pib",
    "ano de referência pib": "ano_pib",
    "ano do produto interno bruto": "ano_pib",
    "ano pib": "ano_pib",
    # Educação Básica — matrículas
    "matrículas educação infantil": "matriculas_educacao_infantil",
    "matriculas educacao infantil": "matriculas_educacao_infantil",
    "matriculas de educacao infantil": "matriculas_educacao_infantil",
    "matriculas no ensino infantil": "matriculas_educacao_infantil",
    "matrículas ensino fundamental": "matriculas_ensino_fundamental",
    "matriculas ensino fundamental": "matriculas_ensino_fundamental",
    "matriculas de ensino fundamental": "matriculas_ensino_fundamental",
    "matriculas no ensino fundamental": "matriculas_ensino_fundamental",
    "matrículas ensino médio": "matriculas_ensino_medio",
    "matriculas ensino medio": "matriculas_ensino_medio",
    "matriculas de ensino medio": "matriculas_ensino_medio",
    "matriculas no ensino medio": "matriculas_ensino_medio",
    "matrículas eja": "matriculas_eja",
    "matriculas eja": "matriculas_eja",
    "matriculas de eja": "matriculas_eja",
    "matrículas de eja": "matriculas_eja",
    "matriculas no eja": "matriculas_eja",
    "matrículas educação especial": "matriculas_educacao_especial",
    "matriculas educacao especial": "matriculas_educacao_especial",
    "matriculas de educacao especial": "matriculas_educacao_especial",
    "matriculas no educacao especial": "matriculas_educacao_especial",
    "matrículas técnico básico": "matriculas_ensino_tecnico",
    "matriculas tecnico basico": "matriculas_ensino_tecnico",
    "matriculas em ensino tecnico": "matriculas_ensino_tecnico",
    # Educação Básica — turmas
    "turmas de educação infantil": "turmas_educacao_infantil",
    "turmas educação infantil": "turmas_educacao_infantil",
    "turmas no ensino infantil": "turmas_educacao_infantil",
    "turmas de ensino fundamental": "turmas_ensino_fundamental",
    "turmas ensino fundamental": "turmas_ensino_fundamental",
    "turmas no ensino fundamental": "turmas_ensino_fundamental",
    "turmas de ensino médio": "turmas_ensino_medio",
    "turmas ensino médio": "turmas_ensino_medio",
    "turmas no ensino médio": "turmas_ensino_medio",
    "turmas eja": "turmas_eja",
    "turmas de eja": "turmas_eja",
    "turmas no eja": "turmas_eja",
    "turmas de educação especial": "turmas_educacao_especial",
    "turmas educação especial": "turmas_educacao_especial",
    "turmas técnico básico": "turmas_ensino_tecnico",
    "turmas de tecnico basico": "turmas_ensino_tecnico",
    # Educação Básica — docentes
    "docentes educação infantil": "docentes_educacao_infantil",
    "professores educação infantil": "docentes_educacao_infantil",
    "docentes ensino fundamental": "docentes_ensino_fundamental",
    "professores ensino fundamental": "docentes_ensino_fundamental",
    "docentes ensino médio": "docentes_ensino_medio",
    "professores ensino médio": "docentes_ensino_medio",
    "docentes eja": "docentes_eja",
    "professores eja": "docentes_eja",
    "docentes educação especial": "docentes_educacao_especial",
    "docentes de educação especial": "docentes_educacao_especial",
    "professores educação especial": "docentes_educacao_especial",
    "professores de educação especial": "docentes_educacao_especial",
    "professores de educação especial": "docentes_educacao_especial",
    "docentes técnico básico": "docentes_ensino_tecnico",
    "professores técnico básico": "docentes_ensino_tecnico",
    # Educação Básica — escolas por etapa
    "escolas de educação infantil": "escolas_educacao_infantil",
    "escolas educação infantil": "escolas_educacao_infantil",
    "total de escolas de educação infantil": "escolas_educacao_infantil",
    "quantas escolas de educação infantil": "escolas_educacao_infantil",
    "escolas de ensino fundamental": "escolas_ensino_fundamental",
    "escolas ensino fundamental": "escolas_ensino_fundamental",
    "quantas escolas de ensino fundamental": "escolas_ensino_fundamental",
    "escolas de ensino médio": "escolas_ensino_medio",
    "escolas ensino médio": "escolas_ensino_medio",
    "quantas escolas de ensino médio": "escolas_ensino_medio",
    "escolas eja": "escolas_eja",
    "escolas de eja": "escolas_eja",
    "escolas de educação especial": "escolas_educacao_especial",
    "escolas de educação especial": "escolas_educacao_especial",
    "escolas técnico": "escolas_ensino_tecnico",
    "escolas técnica": "escolas_ensino_tecnico",
    "escolas de ensino técnico": "escolas_ensino_tecnico",
    # Infraestrutura Básica — instalações
    "biblioteca": "escolas_com_biblioteca",
    "escolas com biblioteca": "escolas_com_biblioteca",
    "laboratório de ciências": "escolas_com_laboratorio_ciencias",
    "laboratorio de ciencias": "escolas_com_laboratorio_ciencias",
    "laboratório de informática": "escolas_com_laboratorio_informatica",
    "laboratorio de informatica": "escolas_com_laboratorio_informatica",
    "cozinha": "escolas_com_cozinha",
    "escolas com cozinha": "escolas_com_cozinha",
    "refeitório": "escolas_com_refeitorio",
    "refeitorio": "escolas_com_refeitorio",
    "quadra esportiva": "escolas_com_quadra_esportes",
    "quadra": "escolas_com_quadra_esportes",
    "internet": "escolas_com_acesso_internet",
    "acesso à internet": "escolas_com_acesso_internet",
    "acessibilidade": "escolas_com_acessibilidade_rampas",
    "acesso para deficientes": "escolas_com_acessibilidade_rampas",
    # Infraestrutura Básica — profissionais de apoio
    "formação pedagógica": "profissionais_com_formacao_pedagogia",
    "formacao pedagogica": "profissionais_com_formacao_pedagogia",
    "coordenadores pedagógicos": "profissionais_coordenadores",
    "coordenadores pedagogicos": "profissionais_coordenadores",
    "monitores": "profissionais_monitores",
    # Educação Técnica
    "quantos cursos técnicos": "qt_curso_tec",
    "quais cursos técnicos": "qt_curso_tec",
    "total cursos técnicos": "qt_curso_tec",
    "cursos técnicos": "qt_curso_tec",
    "qt cursos técnicos": "qt_curso_tec",
    "matrículas cursos técnicos": "qt_mat_curso_tec",
    "matriculas cursos técnicos": "qt_mat_curso_tec",
    "matriculas em cursos técnicos": "qt_mat_curso_tec",
    "cursos integrados": "cursos_integrados_ct",
    "integrados": "cursos_integrados_ct",
    "matrículas integrados": "matriculas_integrados_ct",
    "matriculas integrados": "matriculas_integrados_ct",
    "cursos concomitantes": "cursos_concomitantes",
    "concomitantes": "cursos_concomitantes",
    "matrículas concomitantes": "matriculas_concomitantes",
    "matriculas concomitantes": "matriculas_concomitantes",
    "cursos subsequentes": "cursos_subsequentes",
    "subsequentes": "cursos_subsequentes",
    "matrículas subsequentes": "matriculas_subsequentes",
    "matriculas subsequentes": "matriculas_subsequentes",
    "cursos eja técnicos": "cursos_eja",
    "eja técnicos": "cursos_eja",
    "matrículas eja técnicos": "matriculas_eja",
    "matriculas eja técnicos": "matriculas_eja",
    "ano do censo técnico": "ano_censo",
    "ano do censo": "ano_censo",
    "censo técnico": "ano_censo",
    "total de matrículas em cursos técnicos": "qt_mat_curso_tec",
}

# — monta lista de regex para cada tema a partir das HEURISTICAS —
THEME_KEYWORDS: Dict[str, List[str]] = {
    "populacao": [
        rf"\b{re.escape(term)}\b"
        for term, col in HEURISTICAS.items()
        if col in ("populacao_total", "ano_populacao")
    ],
    "economia": [
        rf"\b{re.escape(term)}\b"
        for term, col in HEURISTICAS.items()
        if col in ("pib_per_capita", "ano_pib")
    ],
    "educacao": [
        rf"\b{re.escape(term)}\b"
        for term, col in HEURISTICAS.items()
        if col.startswith(
            (
                "matriculas_",
                "turmas_",
                "docentes_",
                "escolas_",
                "escolas_com_",
                "profissionais_",
            )
        )
    ],
    "tecnica": [
        rf"\b{re.escape(term)}\b"
        for term, col in HEURISTICAS.items()
        if col.startswith(
            (
                "qt_curso_tec",
                "qt_mat_curso_tec",
                "cursos_integrados_ct",
                "matriculas_integrados_ct",
                "cursos_nivel_medio_nm",
                "matriculas_nivel_medio_nm",
                "cursos_concomitantes",
                "matriculas_concomitantes",
                "cursos_subsequentes",
                "matriculas_subsequentes",
                "cursos_eja",
                "matriculas_eja",
                "ano_censo",
            )
        )
    ],
    "comparative": COMPARATIVE_PATTERNS.copy(),
}

# lista final de temas válidos
TEMAS_VALIDOS = ["populacao", "economia", "educacao", "tecnica", "comparative"]

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

# TEMPLATE para 1 única cidade (single-city agent)
TEMPLATE_SINGLE_CITY: str = """
Você é um analista de dados especialista em políticas públicas municipais.

Responda com **clareza e naturalidade** em apenas **um parágrafo curto**, contendo:

- O número principal solicitado
- A cidade correspondente
- O ano dos dados
- Uma breve frase interpretativa do dado (não apenas o número seco)

**Importante:**
- Sempre mencione o número explicitamente.
- Não adicione contexto geral, histórico ou fatores externos.
- Não escreva mais de 3 linhas.

---

📌 Pergunta: {pergunta}

📊 Dados disponíveis:
{dados_formatados}

📚 Tema: {tema}
📁 Fontes: {fontes}
"""

# TEMPLATE para 2+ cidades (comparative agent)
TEMPLATE_COMPARATIVE: str = """
## Análise Comparativa Entre Cidades

**Pergunta:** {pergunta}

📁 Fontes: {fontes}

📊 Dados disponíveis:
{dados_formatados}

---

1. **Contexto Geral:** Breve visão do que os dados mostram para cada cidade.
{contextos}

2. **Comparação Direta:**
{comparacoes}

3. **Conclusão Objetiva:** Síntese do que se infere comparando os números.
"""

# ————— TEMPLATE PARA INSTITUCIONAL —————
TEMPLATE_INSTITUCIONAL: str = """
Você é um pesquisador de políticas públicas com acesso a documentos institucionais.

Pergunta do usuário:
{pergunta}

Contexto extraído (trechos de documentos):
{dados_formatados}

⚠️ Instruções:
- Resuma os pontos-chave relacionados à pergunta.
- Cite a fonte entre parênteses quando mencionar algo.
- Seja direto e evite floreios.

Resposta:
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

NOMES_AGENTES: Dict[str, str] = {
    "EducacaoAgent": "Educação Básica",
    "TecnicaAgent": "Educação Técnica",
    "PopulacaoAgent": "População",
    "EconomiaAgent": "Economia",
    "InstitucionalAgent": "Institucional",
    "ComparativeAgent": "Comparativo",
    "LLM": "LLM (Fallback)",
}
