# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Builda o frontend (React + Vite)
RUN npm run build

# Usa um servidor leve para servir os arquivos (alternativa: nginx)
RUN npm install -g serve

EXPOSE 3000
CMD ["serve", "-s", "dist"]
