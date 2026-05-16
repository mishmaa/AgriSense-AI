import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import FloatingChatbot from '../ui/FloatingChatbot.jsx';
import ParticleField from '../ui/ParticleField.jsx';
import VoiceAssistant from '../ui/VoiceAssistant.jsx';
import Sidebar from './Sidebar.jsx';
import Topbar from './Topbar.jsx';

export default function AppShell() {
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#f6fbf7] text-graphite-900 dark:bg-graphite-950 dark:text-white">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <ParticleField />
      <div className="relative flex min-h-screen">
        <div className="hidden lg:block">
          <Sidebar />
        </div>

        <AnimatePresence>
          {open && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-40 bg-graphite-950/60 backdrop-blur-sm lg:hidden">
              <motion.div initial={{ x: -320 }} animate={{ x: 0 }} exit={{ x: -320 }} transition={{ type: 'spring', damping: 28, stiffness: 260 }} className="h-full">
                <Sidebar onNavigate={() => setOpen(false)} />
                <button onClick={() => setOpen(false)} className="absolute right-4 top-4 rounded-lg bg-white/10 p-2 text-white" aria-label="Close navigation">
                  <X className="h-5 w-5" />
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        <main id="main-content" className="min-w-0 flex-1" tabIndex={-1}>
          <Topbar onMenu={() => setOpen(true)} />
          <div className="mx-auto w-full max-w-7xl px-4 py-6 lg:px-6 lg:py-8">
            <Outlet />
          </div>
          <FloatingChatbot />
          <VoiceAssistant />
        </main>
      </div>
    </div>
  );
}
