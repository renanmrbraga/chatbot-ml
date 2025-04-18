# backend/Dockerfile
FROM python:3.13-slim

# Instala dependências de sistema necessárias para psycopg>=3
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas arquivos necessários (a pasta scraping já está ignorada via .dockerignore)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
