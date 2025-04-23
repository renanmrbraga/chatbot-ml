![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-00C7B7?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-2023-%2361DAFB?style=for-the-badge&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

# Chatbot LLM para Parcerias Público-Privadas (Educação)

Sistema completo com **backend em FastAPI** e **frontend em React** para responder perguntas sobre dados públicos de cidades brasileiras (educação, economia, população, etc.), com foco em apoiar **Parcerias Público-Privadas (PPPs)**.

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
- Fallback com **Pinecone + embeddings Cohere**
- Logs completos em MongoDB (mensagens, cidades, agentes, dashboards gerados)
- Backend FastAPI + API REST estruturada
- Frontend futurista (React + Vite + Tailwind)
- Integração com APIs do IBGE e dados educacionais do INEP
- Pipeline de scraping e ETL com PostgreSQL

---

## 📊 Fontes de Dados

- **IBGE / SIDRA** – População e PIB
- **INEP / Censo Escolar 2023** – Matrículas, escolas, docentes, infraestrutura escolar
- **QEdu** e outras fontes públicas (em expansão)
- **Dados tratados e integrados por `codigo_ibge`**

---

## ⚙️ Arquitetura

```
📁 backend/
│   ├── core/                           # Agentes semânticos, roteadores, prompts e engine LLM
│   ├── data/                           # Dados baixados e embeddings locais gerados
│   ├── database/                       # Conexões e funções auxiliares para PostgreSQL e MongoDB
│   ├── nginx/                          # NGINX + Certbot para TLS (HTTPS) no backend FastAPI
│   ├── startup/                        # Inicialização automática de embeddings e serviços
│   ├── tests/                          # Testes automatizados do backend
│   ├── uploads-temp/                   # Diretório temporário para uploads do usuário
│   ├── utils/                          # Funções utilitárias (logs, embedder, retriever, etc.)
│   ├── .dockerignore                   # Arquivos ignorados no build da imagem Docker do backend
│   ├── .env                            # Variáveis de ambiente reais (não versionadas)
│   ├── .env.example                    # Modelo de variáveis para ambiente backend
│   ├── Dockerfile                      # Dockerfile com build do backend em FastAPI
│   ├── main.py                         # Entrypoint principal da API FastAPI
│   └── requirements.txt                # Dependências Python do backend
│
📁 docs/
│   ├── Explicação.md                   # Documento de Business Understanding do projeto
│   └── Perguntas.md                    # Exemplos prontos de perguntas ao chatbot
│
📁 frontend/
│   ├── ngrok/                          # Variáveis do ngrok e script para expor endereço no terminal
│   ├── public/                         # Assets públicos servidos pelo Vite (favicon, index, etc.)
│   ├── src/                            # Interface do chatbot (React + TypeScript)
│   ├── .dockerignore                   # Arquivos ignorados no build da imagem Docker do frontend
│   ├── .env                            # Variáveis de ambiente reais do frontend
│   ├── .env.example                    # Modelo de variáveis para frontend
│   ├── components.json                 # Configurações opcionais de componentes dinâmicos
│   ├── Dockerfile                      # Dockerfile do frontend com suporte ao ngrok
│   ├── eslint.config.js                # Configuração do ESLint (análise estática do código)
│   ├── index.html                      # HTML base usado pelo Vite para montar o app
│   ├── package.json                    # Lista de dependências, scripts e metadados do frontend
│   ├── package-lock.json               # Lockfile gerado pelo NPM com versões exatas
│   ├── postcss.config.js               # Plugins de pós-processamento CSS (ex: autoprefixer)
│   ├── tailwind.config.ts              # Configurações visuais customizadas do Tailwind
│   ├── tsconfig.app.json               # Configuração TypeScript para a aplicação React
│   ├── tsconfig.json                   # Configuração global do TypeScript
│   ├── tsconfig.node.json              # Configuração para scripts/utilitários Node.js
│   └── vite.config.ts                  # Configuração do Vite (server, proxy, plugins)
│
📁 mongo/
│   └── mongod.conf                     # Arquivo de configuração do MongoDB (log, path, porta)
│
📁 postgres/
│   ├── init.sql                        # Script de inicialização do banco PostgreSQL (tabelas, dados)
│   ├── pg_hba.conf                     # Configuração de acesso do PostgreSQL (host-based authentication)
│   └── postgresql.conf                 # Configuração geral do PostgreSQL (port, logging, etc.)
│
📁 scraper/
│   ├── config/                         # Arquivos de configuração e parâmetros de scraping
│   ├── core/                           # Scrapers principais (SIDRA, INEP, QEdu, Portal da Transparência)
│   ├── data/                           # Dados brutos, limpos e tratados pelo pipeline ETL
│   ├── utils/                          # Funções auxiliares de scraping e transformação
│   ├── requirements.txt                # Dependências Python do scraper
│   └── scraper.py                      # Pipeline central do scraping (orquestração dos módulos)
│
├── .gitignore                          # Arquivos e pastas ignoradas pelo Git (ex: .env, __pycache__)
├── docker-compose.yml                  # Orquestração de todos os serviços com Docker Compose
├── LICENSE                             # Licença MIT do projeto
├── NOTICE.md                           # Avisos sobre uso de dados públicos e fontes oficiais
└── README.md                           # Documentação principal do projeto
```

---

## 🧰 Tecnologias

| Camada             | Tecnologias                                                                   |
|--------------------|-------------------------------------------------------------------------------|
| **Backend**        | Python + FastAPI + LangChain + Groq (`gemma-2-9b-it`)                         |
| **Frontend**       | TypeScript + React + Tailwind CSS + Vite                                      |
| **Dados**          | PostgreSQL + Pandas + INEP/SIDRA Scrapers                                     |
| **RAG**            | Cohere Embeddings + Pinecone + fallback local HuggingFace                     |
| **Orquestração**   | Agents semânticos + roteamento inteligente                                    |
| **Dashboards**     | Exportação como imagem base64                                                 |
| **Infraestrutura** | Docker + logging estruturado + inicialização automática                       |

---

## 💬 Documentos

- Para o Business Understanding, veja [Explicação](docs/Explicação.md).
- Para exemplos de pergunas, veja [Perguntas](docs/Perguntas.md).

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
cp frontend/ngrok/.env.example ngrok/.env
```

### 4. Configure as variáveis de ambiente (exemplo)

#### Backend
```dotenv
# === DATABASE ===
DATABASE_URL=postgresql+psycopg://postgres:devmode123@chatbot_postgres:5432/chatbot

# === MONGODB (logs) - opcional se usar logs em NoSQL
MONGO_URL=mongodb://chatbot_mongo:27017/

# === LLM (Groq - Gemma 2B) ===
GROQ_API_KEY=sua-chave-groq

# === PINECONE (Embeddings Vetoriais) ===
PINECONE_API_KEY=sua-chave-pinecone
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX=chatbot-llm

# === COHERE (Fallback Semântico) ===
COHERE_API_KEY=sua-chave-cohere
EMBEDDING_PROVIDER=cohere
EMBEDDING_MODEL=embed-english-v3.0

# === PERFORMANCE ===
PERFORMANCE_LEVEL=auto  # auto | turbo | minimal
```

#### Frontend
```dotenv
VITE_API_URL=http://localhost:8000
```

#### Ngrok
```dotenv
NGROK_AUTHTOKEN=sua-chave-ngrok
```

### 5. Suba o sistema com Docker Compose

```bash
docker-compose up --build
```

Acesse:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Ngrok (link online): gerado dinamicamente no terminal

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](./LICENSE).

---

## 📢 Notice

Este sistema usa dados públicos de fontes oficiais (IBGE, INEP, QEdu, etc.).
Os dados podem conter limitações, defasagens ou mudanças futuras.
Este sistema é apenas para fins analíticos e educacionais.
Para informações oficiais, consulte os portais originais – veja o [NOTICE.md](./NOTICE.md).
