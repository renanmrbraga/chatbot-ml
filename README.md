![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-00C7B7?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-2023-%2361DAFB?style=for-the-badge&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

# DataBot

Um **chatbot híbrido RAG** (Retrieval-Augmented Generation) de alta performance, desenvolvido para entregar respostas precisas e contextualizadas sobre dados públicos de municípios brasileiros.
O primeiro passo consiste em um **pipeline de scraping e ETL** que coleta automaticamente dados de APIs públicas (IBGE/SIDRA, INEP, QEdu, etc.) e os armazena no PostgreSQL, garantindo uma fonte de verdade atualizada.

A plataforma integra:

- **FastAPI** no backend, para um servidor leve, assíncrono e escalável.
- **React + Vite + TailwindCSS** no frontend, garantindo uma experiência de usuário fluida e responsiva.
- **LangChain** e **Groq (Gemma-2-9b-it)** para geração de linguagem natural, estritamente guiada por templates por agente.
- **HuggingFace Embeddings** + **Pinecone** para indexação semântica e recuperação dinâmica de contexto.
- **PostgreSQL** como fonte de verdade para dados tabulares (população, PIB, educação, infraestrutura) e **MongoDB** para logging estruturado de cada interação.

Com agentes especializados (População, Economia, Educação Básica, Educação Técnica e Comparativo), o Chatbot:

1. **Interpreta** sua pergunta (detecção de cidade, tema e métrica) por regras heurísticas e keywords, **podendo escalar para a própria LLM interpretar a pergunta**.
2. **Recupera** dentro do PostgreSQL ou, no caso de múltiplos municípios, faz comparativos diretos.
3. **Gera** a saída em Markdown enriquecido (análise de dados e conclusão objetiva), apoiada em prompts customizados.
4. **Registra** cada passo: entrada, agente, fontes, cidades e timestamp em MongoDB, garantindo auditabilidade e métricas de uso.

Este projeto foi concebido para atender às necessidades de:

- **Consultas inteligentes** (quantas escolas, matrículas, docentes, turmas) por município.
- **Análises comparativas** entre duas ou mais cidades, com cálculos diretos de diferença e ranking.
- **Extensibilidade** para novas fontes, métricas e agentes setoriais.

---

## 📌 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [📊 Fontes de Dados](#-fontes-de-dados)
- [⚙️ Arquitetura](#️-arquitetura)
- [🧰 Tecnologias](#-tecnologias)
- [💬 Documentos](#-exemplos-de-perguntas)
- [🚀 Setup](#-setup)
- [📄 Licença](#-licença)
- [📢 Notice](#-notice)

---

## ✨ Funcionalidades

- Consulta inteligente por município (`população`, `PIB`, `infraestrutura`, `escolas`, etc.)
- Comparativos entre cidades com gráficos interativos
- Geração de resposta interpretada por LLM (`gemma-2-9b-it` via Groq)
- Embeddings com **HuggingFace + Pinecone**
- Logs completos em MongoDB (mensagens, cidades, agentes, dashboards gerados)
- Pipeline de scraping e ETL com PostgreSQL
- Backend FastAPI + API REST estruturada
- Frontend moderno (React + Vite + Tailwind)
- Integração com APIs do IBGE e dados educacionais do INEP

---

## 📊 Fontes de Dados

- **IBGE / SIDRA** – População e PIB
- **INEP / Censo Escolar 2023** – Matrículas, escolas, docentes, infraestrutura escolar
- **QEdu** e outras fontes públicas (em expansão)
- **Dados tratados e integrados por `codigo_ibge`**

---

## ⚙️ Arquitetura

<details>
<summary><strong>📁 backend/</strong> — Backend em FastAPI</summary>

```bash
├── config/               # Configurações específicas do backend (ngrok, environment, etc.)
├── core/                 # Agentes semânticos, roteadores, prompts e engine LLM
├── data/                 # Dados baixados e embeddings locais gerados
├── database/             # Conexões e funções auxiliares para PostgreSQL e MongoDB
├── startup/              # Inicialização automática de embeddings e serviços
├── tests/                # Testes automatizados do backend
├── uploads-temp/         # Diretório temporário para uploads do usuário
├── utils/                # Funções utilitárias (logs, embedder, retriever, etc.)
├── .dockerignore         # Arquivos ignorados no build da imagem Docker do backend
├── .env                  # Variáveis de ambiente reais (não versionadas)
├── .env.example          # Modelo de variáveis para ambiente backend
├── Dockerfile            # Dockerfile com build do backend em FastAPI
├── main.py               # Entrypoint principal da API FastAPI
└── requirements.txt      # Dependências Python do backend
```

</details>

<details>
<summary><strong>📁 docs/</strong> — Documentação complementar</summary>

```bash
├── Explicação.md         # Documento de Business Understanding do projeto
└── Perguntas.md          # Exemplos prontos de perguntas ao chatbot
```

</details>

<details>
<summary><strong>📁 frontend/</strong> — Interface do Chatbot (React + Vite + TypeScript)</summary>

```bash
├── ngrok/                # Variáveis do ngrok e script para expor endereço no terminal
├── public/               # Assets públicos servidos pelo Vite (favicon, index, etc.)
├── src/                  # Interface do chatbot (React + TypeScript)
├── .dockerignore         # Arquivos ignorados no build da imagem Docker do frontend
├── .env                  # Variáveis de ambiente reais do frontend
├── .env.example          # Modelo de variáveis para frontend
├── components.json       # Configurações opcionais de componentes dinâmicos
├── Dockerfile            # Dockerfile do frontend com suporte ao ngrok
├── eslint.config.js      # Configuração do ESLint (análise estática do código)
├── index.html            # HTML base usado pelo Vite para montar o app
├── package.json          # Lista de dependências, scripts e metadados do frontend
├── postcss.config.js     # Plugins de pós-processamento CSS (ex: autoprefixer)
├── tailwind.config.ts    # Configurações visuais customizadas do Tailwind
├── tsconfig.app.json     # Configuração TypeScript para a aplicação React
├── tsconfig.json         # Configuração global do TypeScript
├── tsconfig.node.json    # Configuração para scripts/utilitários Node.js
├── vite.config.ts        # Configuração do Vite (server, proxy, plugins)
└── yarn.lock             # Snapshot das dependências instaladas (Gerenciador Yarn)
```

</details>

<details>
<summary><strong>📁 mongo/</strong> — Configurações do MongoDB</summary>

```bash
└── mongod.conf           # Arquivo de configuração do MongoDB (log, path, porta)
```

</details>

<details>
<summary><strong>📁 postgres/</strong> — Configurações do PostgreSQL</summary>

```bash
├── init.sql              # Script de inicialização do banco PostgreSQL (tabelas, dados)
├── pg_hba.conf           # Configuração de acesso do PostgreSQL (host-based authentication)
└── postgresql.conf       # Configuração geral do PostgreSQL (port, logging, etc.)
```

</details>

<details>
<summary><strong>📁 scraper/</strong> — Pipelines de scraping e ETL</summary>

```bash
├── config/               # Arquivos de configuração e parâmetros de scraping
├── core/                 # Scrapers principais (SIDRA, INEP, QEdu, Portal da Transparência)
├── data/                 # Dados brutos, limpos e tratados pelo pipeline ETL
├── utils/                # Funções auxiliares de scraping e transformação
├── requirements.txt      # Dependências Python do scraper
└── scrap.py              # Pipeline central do scraping (orquestração dos módulos)
```

</details>

<details>
<summary><strong>📁 raiz/</strong> — Configurações globais e arquivos principais</summary>

```bash
├── .gitignore                   # Arquivos e pastas ignoradas pelo Git (ex: .env, __pycache__)
├── .pre-commit-config.yaml      # Configuração dos hooks automatizados de pré-commit
├── .prettierrc                  # Regras de formatação automática para o frontend
├── docker-compose.yml           # Orquestração de todos os serviços com Docker Compose
├── LICENSE                      # Licença MIT do projeto
├── mypy.ini                     # Regras de tipagem estática para o Python com mypy
├── pyrightconfig.json           # Regras de tipagem estática do TypeScript com Pyright
└── README.md                    # Documentação principal do projeto
```

</details>

---

## 🧰 Tecnologias

| Camada             | Tecnologias                                             |
| ------------------ | ------------------------------------------------------- |
| **Backend**        | Python + FastAPI + LangChain + Groq (`gemma-2-9b-it`)   |
| **Frontend**       | TypeScript + React + Tailwind CSS + Vite                |
| **Dados**          | PostgreSQL + Pandas + INEP/SIDRA Scrapers               |
| **RAG**            | HuggingFace + Pinecone Embeddings                       |
| **Orquestração**   | Agents semânticos + roteamento inteligente              |
| **Dashboards**     | Exportação como ECharts                                 |
| **Infraestrutura** | Docker + logging estruturado + inicialização automática |

---

## 💬 Documentos

- Para exemplos de perguntas, veja [Perguntas](docs/Perguntas.md).

---

## 🚀 Setup

### 1. Instale o Docker Desktop (Windows/macOS) ou Docker Engine (Linux)

- [Instalar no Windows/macOS](https://www.docker.com/products/docker-desktop/)
- [Instalar no Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Instalar no Arch](https://wiki.archlinux.org/title/Docker)

### 2. Clone o repositório

```bash
git clone https://github.com/renanmrbraga/chatbot-llm.git
cd chatbot-llm
```

### 3. Configure os arquivos `.env`

Copie os exemplos:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 4. Configure as variáveis de ambiente (exemplo)

#### Backend

```dotenv
# === POSTGRES ===
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=chatbot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=devmode123
DATABASE_URL=postgresql+psycopg://postgres:devmode123@postgres:5432/chatbot

# === MONGODB ===
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=chatbot_logs
MONGO_USER=admin
MONGO_PASSWORD=devmode123
MONGO_URL=mongodb://admin:devmode123@mongo:27017/?authSource=admin

# === LLM (Groq - Gemma 2B) ===
GROQ_API_KEY=sua-chave-groq

# === PINECONE (Embeddings Vetoriais) ===
PINECONE_API_KEY=sua-chave-pinecone
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX=sua-index-pinecone

# === EMBEDDING CONFIGURATION ===
EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# === PERFOMANCE (auto | turbo | safe) ===
PERFORMANCE_LEVEL=auto
```

#### Frontend

```dotenv
NGROK_AUTHTOKEN=sua-chave-ngrok
```

### 4. Suba o sistema com Docker Compose

```bash
docker-compose up --build
```

Acesse:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8080`
- Ngrok (link online): gerado dinamicamente no terminal

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](./LICENSE).

---

## 📢 NOTICE – Uso de Dados Públicos

Este projeto utiliza dados públicos obtidos de fontes oficiais do governo brasileiro, de acordo com os princípios da Lei de Acesso à Informação (Lei nº 12.527/2011) e demais normas de dados abertos.

## 🗂️ Fontes de Dados Utilizadas

- **IBGE (Instituto Brasileiro de Geografia e Estatística)**

  - SIDRA API, Downloads em CSV e GeoJSON
  - [https://sidra.ibge.gov.br](https://sidra.ibge.gov.br)

- **INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira)**

  - Censo Escolar, Microdados e Suplementos Técnicos
  - [https://www.gov.br/inep](https://www.gov.br/inep)

- **FNDE (Fundo Nacional de Desenvolvimento da Educação)** `em breve`

  - Programas educacionais e orçamentários
  - [https://www.gov.br/fnde](https://www.gov.br/fnde)

- **Portal da Transparência** `em breve`
  - Gastos públicos federais, estaduais e municipais
  - [https://www.portaltransparencia.gov.br](https://www.portaltransparencia.gov.br)

## ⚠️ Sobre a Interpretação dos Dados

As respostas geradas por este sistema são **interpretadas por um modelo de linguagem (LLM)** com base em dados públicos estruturados. Isso significa que podem haver variações na apresentação e análise dos dados. Sempre consulte os dados brutos nas fontes oficiais para tomada de decisão crítica.

## 📅 Última atualização dos dados

- Dados IBGE: Abril de 2025
- Dados INEP: Censo Escolar 2023
- Dados FNDE: Orçamento 2024 `em breve`
- Portal da Transparência: Atualizações em tempo real `em breve`

---

## 📬 Contato

Para dúvidas ou solicitações formais sobre os dados utilizados, me envie um [e-mail](mailto:renanmrbraga@gmail.com) ou acesse meu [LinkedIn](https://www.linkedin.com/in/renanmrbraga).
