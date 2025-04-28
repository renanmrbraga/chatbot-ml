import { useToast } from '@/components/ui/use-toast';
import { motion } from 'framer-motion';
import { Plus, Send } from 'lucide-react';
import React, { useEffect, useRef, useState } from 'react';
import { enviarPergunta } from '../services/api';
import ChartRenderer, { ChartData } from './ChartRenderer';
import Message from './Message';

interface MessageType {
  role: 'user' | 'system';
  content: string;
  fonte: string | null;
  agente: string | null;
  chart_data?: ChartData | null;
  csv_base64?: string | null;
  pdf_base64?: string | null;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [hasScroll, setHasScroll] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();
  const session_id = 'sessao-teste';

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    const el = containerRef.current;
    setHasScroll(el ? el.scrollHeight > el.clientHeight : false);
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [
      ...prev,
      { role: 'user', content: input.trim(), fonte: null, agente: null },
    ]);
    setInput('');
    setLoading(true);

    try {
      const resp = await enviarPergunta(input, session_id);
      setMessages((prev) => [
        ...prev,
        {
          role: 'system',
          content: resp.resposta,
          agente: resp.agente,
          fonte: resp.fontes?.join(', ') || 'LLM',
          chart_data: resp.chart_data || null,
          csv_base64: resp.csv_base64 || null,
          pdf_base64: resp.pdf_base64 || null,
        },
      ]);
    } catch {
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
    <div className="flex flex-col h-full rounded-lg overflow-hidden">
      {/* LISTA DE MENSAGENS */}
      <div
        ref={containerRef}
        className={`flex-1 p-4 space-y-6 chat-messages${hasScroll ? ' has-scrollbar' : ''}`}
      >
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-foreground">
            Digite sua pergunta para começar...
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className="space-y-2">
              <Message
                role={msg.role}
                text={msg.content}
                agent={msg.agente}
                fontes={msg.fonte ? msg.fonte.split(', ') : []}
              />
              {msg.role === 'system' && msg.chart_data && <ChartRenderer data={msg.chart_data} />}
              {msg.role === 'system' && (msg.csv_base64 || msg.pdf_base64) && (
                <div className="flex gap-4 mt-1 text-sm">
                  {msg.csv_base64 && (
                    <a
                      href={`data:text/csv;base64,${msg.csv_base64}`}
                      download="comparacao.csv"
                      className="text-foreground underline hover:opacity-80"
                    >
                      📥 Baixar CSV
                    </a>
                  )}
                  {msg.pdf_base64 && (
                    <a
                      href={`data:application/pdf;base64,${msg.pdf_base64}`}
                      download="comparacao.pdf"
                      className="text-foreground underline hover:opacity-80"
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

      {/* ÁREA DE INPUT COM BOTÕES */}
      <div className="p-4 bg-transparent border-t border-[hsl(var(--border))]/70 flex justify-center">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2 w-1/2"
        >
          <div
            className="
              flex items-center
              bg-[hsl(var(--background))]/50
              border border-[hsl(var(--border))]/60
              rounded-full
              flex-1 px-3 py-2
            "
          >
            {/* botão de anexar */}
            <button
              type="button"
              className="p-2 text-foreground hover:bg-[hsl(var(--background))]/40 rounded-full transition"
            >
              <Plus size={20} />
            </button>

            {/* campo de texto */}
            <input
              ref={inputRef}
              type="text"
              className="
                flex-1
                bg-transparent
                mx-2
                focus:outline-none
                placeholder:text-foreground/60 placeholder:text-sm
              "
              placeholder="Digite sua pergunta..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />

            {/* botão enviar */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={loading || !input.trim()}
              className="p-2 text-foreground disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="h-5 w-5 border-2 border-foreground border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send size={20} />
              )}
            </motion.button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Chat;
