import { AnimatePresence, motion } from 'framer-motion';
import { Mic, MicOff, Volume2, X } from 'lucide-react';
import { useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import { useLanguage } from '../../context/LanguageContext.jsx';
import { aiApi } from '../../services/api.js';

export default function VoiceAssistant() {
  const { language } = useLanguage();
  const [open, setOpen] = useState(false);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [reply, setReply] = useState('Press the microphone and ask about irrigation, weather, fertilizer, or disease risk.');
  const speechLanguage = useMemo(() => ({ zh: 'zh-CN', ur: 'ur-PK', en: 'en-US' })[language] || 'en-US', [language]);

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      toast.error('Speech recognition is not supported in this browser');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = speechLanguage;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    setListening(true);
    recognition.onresult = async (event) => {
      const text = event.results[0][0].transcript;
      setTranscript(text);
      const data = await aiApi.chatbot(text);
      setReply(data.reply);
      speak(data.reply);
    };
    recognition.onerror = () => {
      setListening(false);
      toast.error('Voice command failed');
    };
    recognition.onend = () => setListening(false);
    recognition.start();
  };

  const speak = (text) => {
    if (!window.speechSynthesis) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = speechLanguage;
    utterance.rate = 0.95;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.96 }}
        onClick={() => setOpen(true)}
        className="fixed bottom-40 right-5 z-30 grid h-14 w-14 place-items-center rounded-full border border-white/20 bg-cyan-500 text-white shadow-glow"
        aria-label="Open voice assistant"
      >
        <Mic className="h-6 w-6" />
      </motion.button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 18, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 12, scale: 0.96 }}
            className="glass fixed bottom-56 right-4 z-40 w-[calc(100vw-2rem)] max-w-sm rounded-lg p-5"
          >
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-semibold">AI Voice Assistant</h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">Speech-to-text farming help</p>
              </div>
              <button onClick={() => setOpen(false)} className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 dark:hover:bg-white/10" aria-label="Close voice assistant">
                <X className="h-5 w-5" />
              </button>
            </div>

            <button
              onClick={startListening}
              className={`mt-5 grid h-24 w-full place-items-center rounded-lg border text-sm font-semibold transition ${
                listening ? 'border-rose-400 bg-rose-500/14 text-rose-500' : 'border-cyan-300/40 bg-cyan-400/12 text-cyan-500'
              }`}
            >
              {listening ? <MicOff className="h-8 w-8" /> : <Mic className="h-8 w-8" />}
              {listening ? 'Listening...' : 'Start voice command'}
            </button>

            <div className="mt-4 space-y-3">
              <div className="rounded-lg bg-white/60 p-3 text-sm dark:bg-white/8">
                <p className="text-xs text-slate-500 dark:text-slate-400">Command</p>
                <p className="mt-1">{transcript || 'No command yet'}</p>
              </div>
              <div className="rounded-lg bg-agri-500/12 p-3 text-sm">
                <p className="flex items-center gap-2 text-xs text-agri-700 dark:text-agri-200"><Volume2 className="h-4 w-4" /> Response</p>
                <p className="mt-1 leading-6">{reply}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
