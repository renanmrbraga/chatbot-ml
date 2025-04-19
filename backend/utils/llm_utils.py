# utils/llm_utils.py
import json

from utils.metricas import METRICAS_VALIDAS

TEMPLATE = """
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

TEMPLATE_METRICA = f"""
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

TEMPLATE_TEMA = """
Você é um classificador semântico para um chatbot sobre políticas públicas de cidades brasileiras.

Classifique a pergunta abaixo em **apenas um** dos seguintes temas:

- educacao
- populacao
- economia
- dashboard (se for uma pergunta que compara duas ou mais cidades)

⚠️ Se a pergunta for muito vaga ou não pertencer a nenhum desses temas, **responda com "tema": "llm"**.

Retorne **apenas o JSON**, sem explicações, neste formato:

{"tema": "educacao"}

Pergunta: "{pergunta}"
"""

def formatar_dados(dados: list[dict] | dict) -> str:
    """
    Converte os dados em um formato de tabela de texto legível para o prompt.

    Aceita tanto uma lista de dicionários (modo padrão) quanto um único dicionário com chave 'context'.
    """
    if not dados:
        return "Nenhum dado disponível."

    if isinstance(dados, dict) and "context" in dados:
        return dados["context"]

    if isinstance(dados, dict):
        dados = [dados]

    colunas = list(dados[0].keys())
    linhas = [colunas] + [[str(linha.get(col, "")) for col in colunas] for linha in dados]
    header = " | ".join(colunas)
    separador = " | ".join(["---"] * len(colunas))
    corpo = "\n".join([" | ".join(linha) for linha in linhas[1:]])

    return f"{header}\n{separador}\n{corpo}"
