// src/components/Chat.tsx
import { useToast } from '@/components/ui/use-toast';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';
import React, { useEffect, useRef, useState } from 'react';
import { enviarPergunta } from '../services/api';
import ComparativeImage from './ComparativeImage'; // ← import adicionado
import Message from './Message';

interface MessageType {
  role: 'user' | 'system';
  content: string;
  fonte: string | null;
  agente: string | null;
  comparative?: string | null;
  csv_base64?: string | null;
  pdf_base64?: string | null;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const session_id = 'sessao-teste';

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: 'user', content: input, fonte: null, agente: null }]);
    setInput('');
    setLoading(true);

    try {
      const response = await enviarPergunta(input, session_id);

      setMessages((prev) => [
        ...prev,
        {
          role: 'system',
          content: response.resposta,
          agente: response.agente,
          fonte: response.fontes?.join(', ') || 'LLM',
          comparative: response.comparative_base64 || null, // ← usa comparative_base64
          csv_base64: response.csv_base64 || null,
          pdf_base64: response.pdf_base64 || null,
        },
      ]);
    } catch (err) {
      console.error('Erro ao enviar mensagem:', err);
      toast({
        title: 'Erro na comunicação',
        description: 'Não foi possível obter resposta do servidor.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-90px)] bg-opacity-70 rounded-xl overflow-hidden border border-white/10 shadow-xl glass-panel">
      {/* Header */}
      <div className="p-4 border-b border-white/10 backdrop-blur-lg bg-black/40">
        <h2 className="text-xl font-medium text-white flex items-center gap-2">
          <span className="text-chatbot-light">🤖</span> Chatbot PPPs Insight
        </h2>
      </div>

      {/* Mensagens */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-chatbot-border scrollbar-track-transparent">
        {messages.length === 0 ? (
          /* ... tela de boas-vindas ... */
          <div className="h-full flex items-center justify-center">{/* ... */}</div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="space-y-2">
              <Message
                role={msg.role}
                text={msg.content}
                agent={msg.agente}
                fontes={msg.fonte ? msg.fonte.split(', ') : []}
              />

              {/* Exibição do gráfico, se houver */}
              {msg.role === 'system' && msg.comparative && (
                <ComparativeImage imageBase64={msg.comparative} />
              )}

              {/* Botões de download */}
              {msg.role === 'system' && (msg.csv_base64 || msg.pdf_base64) && (
                <div className="flex gap-4 mt-1 text-sm">
                  {msg.csv_base64 && (
                    <a
                      href={`data:text/csv;base64,${msg.csv_base64}`}
                      download="comparacao.csv"
                      className="text-chatbot-light underline hover:opacity-80"
                    >
                      📥 Baixar CSV
                    </a>
                  )}
                  {msg.pdf_base64 && (
                    <a
                      href={`data:application/pdf;base64,${msg.pdf_base64}`}
                      download="comparacao.pdf"
                      className="text-chatbot-light underline hover:opacity-80"
                    >
                      📥 Baixar PDF
                    </a>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-white/10 bg-black/40 backdrop-blur-lg">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center w-full"
        >
          <input
            ref={inputRef}
            type="text"
            className="flex-1 w-full px-4 py-3 rounded-xl bg-black/50 text-white border border-white/10 focus:outline-none focus:border-chatbot-light focus:ring-1 focus:ring-chatbot-light transition-colors placeholder:text-sm sm:placeholder:text-base"
            placeholder="Digite sua pergunta..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            disabled={loading || !input.trim()}
            className="w-full sm:w-auto bg-chatbot-accent hover:bg-chatbot-accent/90 text-white px-5 py-3 rounded-xl transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="h-5 w-5 rounded-full border-2 border-white border-t-transparent animate-spin" />
                <span>Processando...</span>
              </>
            ) : (
              <>
                <Send size={18} />
                <span>Enviar</span>
              </>
            )}
          </motion.button>
        </form>
      </div>
    </div>
  );
};

export default Chat;
