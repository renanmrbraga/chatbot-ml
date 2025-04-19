# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

# Instala dependências pro script
RUN apk add --no-cache bash curl jq

COPY . .

# Permissão para o entrypoint
RUN chmod +x entrypoint.sh

EXPOSE 3000
CMD ["./entrypoint.sh"]
