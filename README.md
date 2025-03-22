# ChatBot LLM

Este projeto é um **Chat Bot baseado em Machine Learning**. Ele utiliza modelos de linguagem da Anthropic integrados com a biblioteca **LangChain** para realizar tarefas como sumarização de textos e outras operações de NLP (Processamento de Linguagem Natural).

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuições](#contribuições)
- [Licença](#licença)

## Visão Geral

O ChatBot ML tem como objetivo oferecer uma interface inteligente para processar e resumir textos, além de outras funcionalidades que podem ser integradas futuramente. Este projeto foi desenvolvido para atender as necessidades da empresa, utilizando a API da Anthropic e uma abordagem modular com LangChain.

## Funcionalidades

- **Sumarização de textos:** Divide textos longos em partes menores e gera um resumo claro e objetivo em português.
- **Integração com API da Anthropic:** Utiliza o modelo `claude-3-opus-20240229` para gerar respostas e resumos.
- **Carregamento de variáveis de ambiente:** Configuração facilitada através de arquivo `.env`.

## Tecnologias Utilizadas

- **Python 3.11**
- **LangChain e LangChain Anthropic**
- **Anthropic API**
- **python-dotenv**
- **Requests**

## Pré-requisitos

- Ter o **Python 3.11** instalado.
- Ter o **Git** instalado para controle de versão.
- Conta válida e chave de API para acessar os serviços da Anthropic.
- Ambiente virtual configurado (recomendado para isolar as dependências).

## Instalação e Configuração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/renanmrbraga/chatbot-ml.git
   cd chatbot-ml
   ```

2. **Crie e ative o ambiente virtual:**

   Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   ```

   Linux/Mac:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto e adicione a seguinte linha, substituindo `seu_codigo` pela sua chave de API da Anthropic:

   ```plaintext
   ANTHROPIC_API_KEY=seu_codigo
   ```

## Uso

Após seguir os passos de instalação e configuração, você pode executar o projeto:

```bash
python src/app.py
```

O script fará o seguinte:
- Carregar a chave de API a partir do arquivo `.env`.
- Criar um modelo de linguagem utilizando o **ChatAnthropic**.
- Dividir um texto em partes menores e criar documentos a partir dele.
- Executar uma cadeia de sumarização para gerar um resumo em português.
- Exibir o resumo gerado no console.

## Estrutura de Diretórios e Arquivos

```plaintext
├── analysis/
├── data/
├── docs/
├── log/
├── src/
│   └── app.py  # Script principal do chatbot
├── tests/
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md   # Este arquivo de documentação
└── requirements.txt
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar o projeto.

1. Faça um fork do repositório.
2. Crie uma branch com a sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m 'Adiciona nova feature'
   ```
4. Envie para a branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob os termos da **MIT License**.  
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes ou acesse:  
[Licença MIT](https://opensource.org/licenses/MIT)
