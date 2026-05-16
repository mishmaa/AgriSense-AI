import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';

export default function FloatingActionButton({ onClick }) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.96 }}
      onClick={onClick}
      className="fixed bottom-24 right-5 z-30 grid h-14 w-14 place-items-center rounded-full bg-agri-500 text-white shadow-glow"
      aria-label="Create new item"
    >
      <Plus className="h-6 w-6" />
    </motion.button>
  );
}
