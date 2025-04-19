# backend/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copia apenas arquivos necessários (a pasta scraping já está ignorada via .dockerignore)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
