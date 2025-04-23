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

# === 3. Aguarda backend ficar disponível ===
BACKEND_IP=$(getent hosts backend | awk '{ print $1 }')
URL="http://$BACKEND_IP:8000/health"

echo "⏳ Aguardando backend responder em $URL..."
sleep 20
for i in {1..3}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "000")
  echo "📡 Resposta do backend: $STATUS"
  if [ "$STATUS" = "200" ]; then
    echo "✅ Backend disponível."
    break
  fi
  sleep 5
done

if [ "$STATUS" != "200" ]; then
  echo "❌ Backend não respondeu após 30s. Encerrando."
  exit 1
fi

# === 4. Captura e salva URL pública ===
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[] | select(.proto=="https") | .public_url')
echo "🌐 Salvando domínio $NGROK_URL no .env.runtime..."
echo "NGROK_URL=$NGROK_URL" > /app/ngrok/.env.runtime

# === 5. Inicia Vite ===
echo "🚀 Iniciando frontend com Vite..."
exec npx vite --host 0.0.0.0 --port 8080
