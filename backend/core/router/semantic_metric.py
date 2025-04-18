# backend/core/router/semantic_metric.py
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from utils.config import GROQ_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=512
)

# Mapeamento validado das colunas reais do banco com labels explicativos
METRICAS_VALIDAS = {
    "populacao": "População Total",
    "pib_per_capita": "PIB per Capita",
    "matriculas_infantil": "Matrículas - Educação Infantil",
    "matriculas_fundamental": "Matrículas - Ensino Fundamental",
    "matriculas_medio": "Matrículas - Ensino Médio",
    "matriculas_eja": "Matrículas - EJA",
    "matriculas_especial": "Matrículas - Educação Especial",
    "matriculas_tecnico": "Matrículas - Curso Técnico",
    "turmas_infantil": "Turmas - Educação Infantil",
    "turmas_fundamental": "Turmas - Ensino Fundamental",
    "turmas_medio": "Turmas - Ensino Médio",
    "turmas_eja": "Turmas - EJA",
    "turmas_especial": "Turmas - Educação Especial",
    "turmas_tecnico": "Turmas - Curso Técnico",
    "docentes_infantil": "Docentes - Educação Infantil",
    "docentes_fundamental": "Docentes - Ensino Fundamental",
    "docentes_medio": "Docentes - Ensino Médio",
    "docentes_eja": "Docentes - EJA",
    "docentes_especial": "Docentes - Educação Especial",
    "docentes_tecnico": "Docentes - Curso Técnico",
    "escolas_infantil": "Escolas - Educação Infantil",
    "escolas_fundamental": "Escolas - Ensino Fundamental",
    "escolas_medio": "Escolas - Ensino Médio",
    "escolas_eja": "Escolas - EJA",
    "escolas_especial": "Escolas - Educação Especial",
    "escolas_tecnico": "Escolas - Curso Técnico",
    "infra_basica_biblioteca": "Infraestrutura - Bibliotecas (Educação Básica)",
    "infra_basica_lab_ciencias": "Infraestrutura - Lab. Ciências (Educação Básica)",
    "infra_basica_lab_informatica": "Infraestrutura - Lab. Informática (Educação Básica)",
    "infra_basica_cozinha": "Infraestrutura - Cozinhas (Educação Básica)",
    "infra_basica_refeitorio": "Infraestrutura - Refeitórios (Educação Básica)",
    "infra_basica_quadra_esportes": "Infraestrutura - Quadras (Educação Básica)",
    "infra_basica_internet": "Infraestrutura - Internet (Educação Básica)",
    "infra_basica_acessibilidade_rampas": "Infraestrutura - Acessibilidade (Educação Básica)",
    "prof_basica_professores_pedagogia": "Professores com Formação Pedagógica",
    "prof_basica_coordenadores": "Coordenadores Pedagógicos",
    "prof_basica_monitores": "Monitores Educacionais",
    "cursos_tecnicos_ofertados": "Cursos Técnicos Ofertados"
}

# Heurística simples baseada em palavras-chave
HEURISTICAS = {
    "população": "populacao",
    "habitantes": "populacao",
    "pib": "pib_per_capita",
    "renda": "pib_per_capita",
    "matrículas": "matriculas_fundamental",
    "ensino médio": "matriculas_medio",
    "educação infantil": "matriculas_infantil",
    "escolas": "escolas_fundamental",
    "biblioteca": "infra_basica_biblioteca",
    "quadra": "infra_basica_quadra_esportes",
    "cozinha": "infra_basica_cozinha",
    "internet": "infra_basica_internet",
    "laboratório": "infra_basica_lab_informatica",
    "curso técnico": "cursos_tecnicos_ofertados",
    "técnico": "cursos_tecnicos_ofertados",
}

TEMPLATE = f"""
Você é um classificador de métricas para dashboards comparativos entre cidades brasileiras.

Com base na pergunta do usuário, identifique a melhor coluna da tabela `dados_municipios` para gerar o gráfico comparativo entre cidades.

⚠️ Importante:
- A infraestrutura escolar refere-se **apenas às escolas de Educação Infantil, Ensino Fundamental e Médio**.
- **Não inclui escolas técnicas ou cursos técnicos**.

Use apenas uma das seguintes colunas:
{json.dumps(METRICAS_VALIDAS, indent=2, ensure_ascii=False)}

Retorne apenas um JSON válido no formato:
{{ "coluna": "matriculas_fundamental", "label": "Matrículas - Ensino Fundamental" }}

Pergunta: "{{{{pergunta}}}}"
"""

def aplicar_heuristica(pergunta: str) -> tuple[str, str] | None:
    pergunta_lower = pergunta.lower()
    for termo, coluna in HEURISTICAS.items():
        if termo in pergunta_lower:
            label = METRICAS_VALIDAS.get(coluna, coluna)
            logger.info(f"⚙️ Métrica classificada via heurística: {coluna} ({label})")
            return coluna, label
    return None

def classificar_metrica(pergunta: str) -> tuple[str, str]:
    # 1. Tentativa por heurística direta
    heuristica = aplicar_heuristica(pergunta)
    if heuristica:
        return heuristica

    # 2. Fallback: usar LLM para classificar
    try:
        prompt = ChatPromptTemplate.from_template(TEMPLATE).format_messages(pergunta=pergunta)
        resposta = llm.invoke(prompt)
        content = resposta.content.strip().replace("```json", "").replace("```", "").strip()
        logger.debug(f"📨 Resposta bruta da LLM para métrica:\n{content}")

        # Parsing seguro com fallback via regex
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r'"coluna"\s*:\s*"(?P<coluna>[\w_]+)".*?"label"\s*:\s*"(?P<label>[^"]+)"', content, re.DOTALL)
            if match:
                parsed = {
                    "coluna": match.group("coluna"),
                    "label": match.group("label")
                }
                logger.warning(f"⚠️ JSON inválido, mas métrica extraída via regex: {parsed}")
            else:
                raise

        coluna = parsed.get("coluna", "").strip()
        label = parsed.get("label", "").strip()

        if not coluna or coluna not in METRICAS_VALIDAS:
            logger.warning(f"⚠️ Coluna inválida ou não reconhecida: '{coluna}'")
            return "", "Comparação geral entre cidades"

        return coluna, label or METRICAS_VALIDAS.get(coluna)

    except Exception as e:
        logger.warning(f"⚠️ Falha ao classificar métrica: {e}")
        return "", "Comparação geral entre cidades (default)"
