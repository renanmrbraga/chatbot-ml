#!/bin/bash

echo "⏳ Aguardando ngrok subir..."
until curl -s http://chatbot_ngrok:4040/api/tunnels | grep -q 'public_url'; do
  sleep 1
done

NGROK_URL=$(curl -s http://chatbot_ngrok:4040/api/tunnels | jq -r '.tunnels[0].public_url')

echo "🔗 ngrok URL detectada: $NGROK_URL"
echo "VITE_API_URL=$NGROK_URL" > .env

echo "🚀 Iniciando frontend com Vite apontando para $NGROK_URL"
npm run dev -- --host
