
import React from "react";
import { motion } from "framer-motion";

interface DashboardImageProps {
  imageBase64?: string | null;
}

const DashboardImage: React.FC<DashboardImageProps> = ({ imageBase64 }) => {
  if (!imageBase64) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.2 }}
      className="mt-6 border rounded-2xl p-4 bg-black/40 border-chatbot-border shadow-lg backdrop-blur-sm"
    >
      <h3 className="text-xl font-semibold text-white mb-3 flex items-center gap-2">
        <span className="text-chatbot-light">📊</span> Dashboard Comparativo
      </h3>
      <motion.img
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        src={`data:image/png;base64,${imageBase64}`}
        alt="Dashboard Comparativo"
        className="w-full rounded-xl border border-chatbot-border/30 shadow-xl"
        onError={(e) => {
          const target = e.target as HTMLImageElement;
          target.onerror = null;
          target.src = "";
          console.warn("⚠️ Erro ao carregar imagem base64");
        }}
      />
    </motion.div>
  );
};

export default DashboardImage;
