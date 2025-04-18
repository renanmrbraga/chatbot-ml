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
- [💬 Exemplos de Perguntas](#-exemplos-de-perguntas)
- [🚀 Setup](#-setup)
- [📄 Licença](#-licença)
- [📢 Notice](#-notice)

---

## ✨ Funcionalidades

- Consulta inteligente por município (`população`, `PIB`, `infraestrutura`, `escolas`, etc.)
- Comparações com gráficos interativos entre cidades
- Respostas interpretadas por LLM (`gemma-2-9b-it` via Groq)
- Fallback com **Pinecone + embeddings Cohere**
- Logs completos no PostgreSQL (mensagens, agentes, cidades, fonte de dados, dashboards)
- Backend em FastAPI pronto para conexão com seu frontend preferido
- Painel de frontend futurista e leve com React + Tailwind + Vite
- Integração modular com API pública do IBGE e dados educacionais do INEP
- Pipeline robusto de scraping e ETL com integração PostgreSQL

---

## 📊 Fontes de Dados

- **IBGE / SIDRA** – População e PIB
- **INEP / Censo Escolar 2023** – Matrículas, escolas, docentes, infraestrutura
- **QEdu** e outras fontes públicas (em expansão)
- **Dados tratados e integrados por `codigo_ibge`**

---

## ⚙️ Arquitetura

```
📁 backend/
│   ├── core/               # Agentes, roteadores, LLMs, prompts
│   ├── data/               # Dados brutos, processados e embeddings gerados
│   ├── database/           # Conexão com PostgreSQL
│   ├── logs/               # Arquivos de logs
│   ├── scraping/           # Scrapers e ETL
│   ├── startup/            # Inicialização automática de embeddings
│   ├── tests/              # Arquivos de testes
│   ├── uploads-temp/       # Upload de arquivos
│   ├── utils/              # Funções auxiliares (logs, embeddings, etc)
│   ├── main.py             # Entrypoint FastAPI
│   ├── .env                # Configurações do backend
│   ├── .env.example        # Modelo de variáveis para backend
│   └── requirements.txt    # Dependências
│
📁 frontend/
│   ├── public/             # Assets públicos
│   ├── src/                # Interface do chat
│   ├── .env                # Configurações do frontend
│   └── .env.example        # Modelo de variáveis para frontend
│
📁 scripts/
│   └── gerar_embeddings_cidades.py  # (Opcional) Geração manual de embeddings
│
├── .gitignore
├── LICENSE
├── NOTICE.md
└── README.md
```

---

## 🧰 Tecnologias

| Camada             | Tecnologias                                                                   |
|--------------------|-------------------------------------------------------------------------------|
| **Backend**        | Python + FastAPI + LangChain + Groq (`gemma-2-9b-it`)                         |
| **Frontend**       | TypeScript + React + Tailwind CSS + Vite                                      |
| **Dados**          | PostgreSQL + Pandas + INEP/SIDRA Scrapers                                     |
| **RAG**            | Cohere Embeddings + Pinecone + fallback local HuggingFace                     |
| **Orquestração**   | Agents semânticos + roteamento inteligente + prompts temáticos                |
| **Dashboards**     | Exportação como imagem base64                                                 |
| **Infraestrutura** | Docker + logging estruturado + inicialização automática                       |

---

## 💬 Exemplos de Perguntas

- "Quantas escolas de ensino médio existem em Curitiba?"
- "Compare escolas técnicas entre Porto Alegre e Curitiba"
- "Quem tem mais professores: Recife ou Fortaleza?"
- "Qual o PIB de Santa Catarina?"

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

### 4. .env.example

#### Backend
```dotenv
DATABASE_URL=postgresql://usuario:senha@localhost:5432/seubanco
GROQ_API_KEY=sua-chave-aqui
PINECONE_API_KEY=sua-chave-aqui
PINECONE_ENVIRONMENT=seu-environment-aqui
PINECONE_INDEX=seu-index-aqui
COLLECTION_NAME=seu-index-aqui
COHERE_API_KEY=sua-chave-aqui
EMBEDDING_PROVIDER=cohere
EMBEDDING_MODEL=embed-english-v3.0
```

#### Frontend
```dotenv
VITE_API_URL=http://localhost:8000
```

### 5. Suba o sistema com Docker Compose

```bash
docker-compose up --build
```

Acesse:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](./LICENSE).

---

## 📢 Notice

Este sistema usa dados públicos de fontes oficiais (IBGE, INEP, QEdu, etc.).  
Os dados podem conter limitações, defasagens ou mudanças futuras.  
Este sistema é apenas para fins analíticos e educacionais.  
Para informações oficiais, consulte os portais originais – veja o [NOTICE.md](./NOTICE.md).
