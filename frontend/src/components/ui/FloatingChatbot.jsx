import { AnimatePresence, motion } from 'framer-motion';
import { Bot, Send, X } from 'lucide-react';
import { useState } from 'react';
import { aiApi } from '../../services/api.js';

export default function FloatingChatbot() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Ask me about irrigation, disease scouting, fertilizer, weather risk, or crop planning.' }
  ]);

  const send = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;
    const userText = message.trim();
    setMessage('');
    setMessages((current) => [...current, { role: 'user', text: userText }]);
    const data = await aiApi.chatbot(userText);
    setMessages((current) => [...current, { role: 'assistant', text: data.reply }]);
  };

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.04 }}
        whileTap={{ scale: 0.96 }}
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-30 grid h-14 w-14 place-items-center rounded-full bg-agri-500 text-white shadow-glow"
        aria-label="Open AI assistant"
      >
        <Bot className="h-6 w-6" />
      </motion.button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 18, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 12, scale: 0.96 }}
            className="glass fixed bottom-24 right-4 z-40 flex h-[520px] w-[calc(100vw-2rem)] max-w-md flex-col rounded-lg p-4"
          >
            <div className="flex items-center justify-between border-b border-slate-200/70 pb-3 dark:border-white/10">
              <div className="flex items-center gap-2">
                <span className="grid h-9 w-9 place-items-center rounded-lg bg-agri-500 text-white">
                  <Bot className="h-5 w-5" />
                </span>
                <div>
                  <p className="font-semibold">AgriSense Assistant</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">AI farming copilot</p>
                </div>
              </div>
              <button onClick={() => setOpen(false)} className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 dark:hover:bg-white/10" aria-label="Close AI assistant">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="flex-1 space-y-3 overflow-y-auto py-4">
              {messages.map((item, index) => (
                <div key={`${item.role}-${index}`} className={item.role === 'user' ? 'text-right' : 'text-left'}>
                  <span className={`inline-block max-w-[82%] rounded-lg px-3 py-2 text-sm leading-6 ${item.role === 'user' ? 'bg-agri-500 text-white' : 'bg-white/70 text-slate-700 dark:bg-white/10 dark:text-slate-200'}`}>
                    {item.text}
                  </span>
                </div>
              ))}
            </div>

            <form onSubmit={send} className="flex gap-2 border-t border-slate-200/70 pt-3 dark:border-white/10">
              <input
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                className="h-11 min-w-0 flex-1 rounded-lg border border-slate-200 bg-white/75 px-3 text-sm outline-none focus:border-agri-400 dark:border-white/10 dark:bg-white/8"
                placeholder="Ask about this farm..."
              />
              <button className="grid h-11 w-11 place-items-center rounded-lg bg-agri-500 text-white" aria-label="Send message">
                <Send className="h-4 w-4" />
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
