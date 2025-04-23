import React from 'react';
import Chat from '@/components/Chat';

const Index = () => {
  return (
    <div className="min-h-screen chat-gradient py-10 px-4 sm:px-6">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-3 text-chatbot-light text-glow tracking-tight">
            🤖 Chatbot PPPs Insight
          </h1>
          <p className="text-gray-300 max-w-lg mx-auto">
            Faça perguntas sobre PPPs e obtenha insights com análises detalhadas e dados
            comparativos
          </p>
        </header>

        <main>
          <Chat />
        </main>

        <footer className="mt-8 text-center text-xs text-gray-500">
          <p>© 2025 Chatbot PPPs Insight • Todos os direitos reservados</p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
