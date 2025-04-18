
import React from "react";
import { motion } from "framer-motion";

interface MessageProps {
  role: "user" | "system" | string;
  text: string;
  agent?: string | null;
  fontes?: string[] | null;
  dashboardImage?: string | null;
}

const Message: React.FC<MessageProps> = ({ role, text, agent, fontes, dashboardImage }) => {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
      className={`my-4 flex ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div 
        className={`
          max-w-[85%] rounded-2xl px-5 py-4 shadow-lg transition-all duration-300
          ${isUser 
            ? "bg-gradient-to-br from-chatbot-user to-chatbot-user/80 text-white" 
            : "glass-panel text-gray-100"
          }
        `}
      >
        {!isUser && agent && (
          <div className="text-xs text-chatbot-light mb-2 font-mono flex flex-wrap gap-2 items-center">
            <span className="inline-flex items-center gap-1">
              🤖 Agente: <span className="text-white font-medium">{agent || "LLM"}</span>
            </span>
            
            {fontes && fontes.length > 0 && (
              <span className="inline-flex items-center gap-1">
                • 🗂️ Fonte: <span className="text-white font-medium">{fontes.join(", ")}</span>
              </span>
            )}
          </div>
        )}
        
        <div className="whitespace-pre-line leading-relaxed font-light text-sm md:text-base tracking-wide">
          {text}
        </div>
        
        {dashboardImage && (
          <motion.img
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            src={`data:image/png;base64,${dashboardImage}`}
            alt="Dashboard gerado"
            className="mt-4 rounded-xl border border-chatbot-border/30 max-w-full shadow-md"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.onerror = null;
              target.src = "";
              console.warn("⚠️ Erro ao carregar imagem base64");
            }}
          />
        )}
      </div>
    </motion.div>
  );
};

export default Message;
