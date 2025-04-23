const BASE_URL = '/api';

export interface ChatResponse {
  resposta: string;
  agente: string;
  fontes?: string[];
  comparative_base64?: string;
}

export async function enviarPergunta(pergunta: string, sessionId: string): Promise<ChatResponse> {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ pergunta, session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error('Erro ao buscar resposta do backend');
  }

  return await response.json();
}
