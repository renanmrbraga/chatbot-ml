FROM python:3.13-slim

# === 1. Diretório de trabalho ===
WORKDIR /app

# === 2. Variáveis de ambiente ===
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# === 3. Instala dependências Python ===
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === 4. Copia a aplicação ===
COPY . .

# === 5. Expõe a porta do FastAPI ===
EXPOSE 8000

# === 6. Comando padrão ===
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
