# frontend/Dockerfile
FROM node:20-slim

WORKDIR /app

# Copia pacotes e instala dependências do projeto
COPY package*.json ./
RUN npm install

# Copia o restante do app (src, public, vite.config.ts, etc)
COPY . .

# Instala ferramentas essenciais e o ngrok globalmente
RUN apt-get update && apt-get install -y curl jq bash && rm -rf /var/lib/apt/lists/*
RUN npm install -g ngrok

# Torna o script de entrada executável
RUN chmod +x ./ngrok/entrypoint.sh

# Expondo a porta do Vite (frontend)
EXPOSE 8080

# Comando principal
CMD ["./ngrok/entrypoint.sh"]
