# Importa o módulo 'os' para interagir com o sistema operacional,
# permitindo acessar variáveis de ambiente e outras funções relacionadas ao sistema.
import os

# Importa as funções 'load_dotenv' e 'find_dotenv' da biblioteca 'python-dotenv'.
# Essas funções são usadas para carregar variáveis de ambiente definidas em um arquivo .env,
# facilitando a configuração de parâmetros sensíveis (como chaves de API) sem codificá-los diretamente.
from dotenv import load_dotenv, find_dotenv

# Importa o módulo 'requests', que permite fazer requisições HTTP.
# Embora não seja utilizado diretamente neste exemplo, ele pode ser útil para interagir com APIs.
import requests

# Importa a classe 'ChatAnthropic' do pacote 'langchain_anthropic'.
# Essa classe é usada para interagir com modelos de linguagem fornecidos pela Anthropic.
from langchain_anthropic import ChatAnthropic

# Importa a classe 'Document' da biblioteca LangChain.
# Ela é usada para representar textos/documentos que serão processados.
from langchain.docstore.document import Document

# Importa a classe 'CharacterTextSplitter' da LangChain.
# Essa classe é utilizada para dividir um texto longo em pedaços menores, com base em caracteres.
from langchain.text_splitter import CharacterTextSplitter

# Importa a função 'load_summarize_chain' da LangChain.
# Essa função constrói uma "cadeia" (chain) que realiza a sumarização dos textos.
from langchain.chains.summarize import load_summarize_chain

# Importa a classe 'PromptTemplate' que permite definir um template (modelo) para as instruções
# que serão enviadas para o modelo de linguagem.
from langchain.prompts import PromptTemplate  # Importante para criar o prompt personalizado

# ----------------------------------------------------------------------------- 
# Carrega as variáveis de ambiente a partir do arquivo .env.
# A função 'find_dotenv()' procura automaticamente pelo arquivo .env na estrutura de pastas.
# Em seguida, 'load_dotenv()' carrega essas variáveis para que possam ser usadas pelo código.
load_dotenv(find_dotenv())

# Recupera a variável de ambiente 'ANTHROPIC_API_KEY' que contém a chave de acesso à API da Anthropic.
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# Exibe a chave carregada no console para confirmar que a variável foi definida corretamente.
print("ANTHROPIC_API_KEY: ", ANTHROPIC_API_KEY)

# ----------------------------------------------------------------------------- 
# Cria um modelo de linguagem (LLM) utilizando a classe ChatAnthropic.
# O modelo é configurado para usar o modelo "claude-3-opus-20240229" com uma temperatura de 0,
# o que significa que as respostas serão mais determinísticas (menos aleatórias).
llm = ChatAnthropic(
    model="claude-3-opus-20240229",
    temperature=0,  # Define o nível de criatividade do modelo (0 = respostas mais previsíveis)
    anthropic_api_key=ANTHROPIC_API_KEY  # Utiliza a chave de API carregada
)

# ----------------------------------------------------------------------------- 
# Define um texto a ser processado.
# Neste exemplo, o texto fala sobre a artista Tarsila do Amaral e sua importância na arte brasileira.
text = "Tarsila do Amaral é um dos mais conhecidos e aclamados nomes da pintura nacional, sendo um ícone do modernismo brasileiro. Integrando diversos elementos típicos da cultura brasileira, a artista foi capaz de produzir uma identidade cultural própria, que assimilava as tendências da arte moderna europeia, ao mesmo tempo que lhes dava as cores nacionais. Para além do período modernista, sua obra mais famosa, O Abaporu, símbolo do Manifesto Antropófago de 1928, é também o quadro mais valioso da história da arte brasileira. Ademais, Tarsila do Amaral é uma das grandes representantes da arte latino-americana, com exposições dedicadas a ela circulando por grandes museus ao redor do mundo. Veja mais sobre 'Tarsila do Amaral' em: https://brasilescola.uol.com.br/biografia/tarsila-amaral.htm"

# ----------------------------------------------------------------------------- 
# Cria uma instância do CharacterTextSplitter para dividir o texto em pedaços menores.
# Isso é útil para facilitar o processamento de textos longos, quebrando-os em partes menores.
text_splitter = CharacterTextSplitter()

# Utiliza o método 'split_text' para dividir o texto em uma lista de pedaços.
texts = text_splitter.split_text(text)

# Exibe a lista de textos divididos no console.
print(texts)

# Cria uma lista de objetos Document a partir dos pedaços de texto.
# Cada objeto Document contém uma parte do texto original, pronto para ser processado.
docs = [Document(page_content=text) for text in texts]  # List comprehension para criar os documentos

# ----------------------------------------------------------------------------- 
# Define o template (modelo) de prompt para a sumarização.
# Esse template instrui o modelo a resumir o texto em português de forma clara e objetiva.
prompt_template = "Resuma o seguinte texto em português de forma clara e objetiva: \n\n{text}"

# Cria um objeto PromptTemplate usando o template definido e especifica que a variável 'text'
# será substituída no template.
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# ----------------------------------------------------------------------------- 
# Cria a cadeia de sumarização utilizando a função load_summarize_chain.
# Aqui, a cadeia é configurada para o tipo "stuff" (uma estratégia de sumarização)
# e o prompt personalizado é passado para instruir o modelo.
chain = load_summarize_chain(
    llm=llm,
    chain_type="stuff",
    prompt=prompt  # Passa o PromptTemplate configurado anteriormente
)

# Executa a cadeia de sumarização com os documentos criados.
# O método 'invoke' processa os documentos e retorna um resumo.
summary = chain.invoke(docs)  # Executa a cadeia de resumo dos textos

# Exibe o resumo gerado no console.
print(summary['output_text'])
