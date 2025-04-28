#!/usr/bin/env bash
set -euo pipefail

echo "🟣 Iniciando frontend com ngrok embutido..."

# === 0. Carrega variáveis do .env principal ===
set -a
if [ -f /app/.env ]; then
  while IFS='=' read -r key value; do
    if [[ $key != \#* ]] && [[ -n "$key" ]]; then
      export "$key"="$(echo "$value" | tr -d '"')"
    fi
  done < /app/.env
fi
set +a

# === Validação ===
if [ -z "${NGROK_AUTHTOKEN:-}" ]; then
  echo "❌ Variável NGROK_AUTHTOKEN não encontrada. Verifique o arquivo /app/.env"
  exit 1
fi

# === 1. Autentica ngrok ===
echo "🔐 Autenticando ngrok..."
ngrok config add-authtoken "$NGROK_AUTHTOKEN"

# === 2. Inicia ngrok para o frontend em segundo plano ===
ngrok http 8080 > /dev/null &
sleep 2

# === 3. Captura e salva URL pública ===
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[] | select(.proto=="https") | .public_url')

if [ -z "$NGROK_URL" ]; then
  echo "❌ Não foi possível capturar a URL pública do ngrok."
  exit 1
fi

echo "🌐 Salvando domínio $NGROK_URL no .env.runtime..."

# Garante que o arquivo existe
touch /app/ngrok/.env.runtime

# Escreve a URL no arquivo
echo "NGROK_URL=$NGROK_URL" > /app/ngrok/.env.runtime

# === 4. Inicia Vite ===
echo "🚀 Iniciando frontend com Vite..."
exec npx vite --host 0.0.0.0 --port 8080
