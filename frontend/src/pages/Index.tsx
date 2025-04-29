import Chat from '@/components/Chat';

const Index = () => {
  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden">
      {/* HEADER GERAL – visível sempre no topo */}
      <header className="w-full bg-background/90 backdrop-blur-sm z-10 py-6 px-4 sm:px-6 flex flex-col items-center">
        <h1 className="text-3xl md:text-4xl font-bold text-foreground">🤖 Houer DataBot</h1>
        <p className="text-gray-300 mt-1 text-center max-w-xl">
          Faça perguntas sobre cidades e obtenha insights com análises detalhadas e dados
          comparativos
        </p>
      </header>

      {/* MAIN – container do chat */}
      <main className="flex-1 bg-background p-4 sm:p-6 overflow-hidden">
        <Chat />
      </main>

      {/* FOOTER */}
      <footer className="w-full bg-background/90 backdrop-blur-sm py-4 text-center text-xs text-gray-400">
        © 2025 Houer DataBot • Todos os direitos reservados
      </footer>
    </div>
  );
};

export default Index;
