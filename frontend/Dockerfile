# frontend/Dockerfile
FROM node:20-slim

WORKDIR /app

# Habilita Corepack (node>=16) para usar Yarn sem instalar global
RUN corepack enable

# Copia apenas package.json + yarn.lock e instala com yarn
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copia o restante do código
COPY . .

# Instala ngrok (se ainda precisar)
RUN apt-get update && apt-get install -y curl jq bash \
    && rm -rf /var/lib/apt/lists/* \
    && yarn global add ngrok \
    && chmod +x ./ngrok/entrypoint.sh

EXPOSE 8080

CMD ["./ngrok/entrypoint.sh"]
