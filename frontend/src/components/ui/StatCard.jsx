import { motion, useMotionValue, useReducedMotion, useSpring } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';
import { useEffect, useState } from 'react';
import { cn } from '../../utils/formatters.js';

const toneClass = {
  emerald: 'from-agri-400/20 to-agri-600/10 text-agri-600 dark:text-agri-300',
  cyan: 'from-cyan-400/20 to-blue-500/10 text-cyan-600 dark:text-cyan-300',
  blue: 'from-blue-400/20 to-indigo-500/10 text-blue-600 dark:text-blue-300',
  amber: 'from-amber-300/20 to-orange-500/10 text-amber-600 dark:text-amber-300'
};

export default function StatCard({ label, value, trend, icon: Icon, tone = 'emerald', delay = 0 }) {
  const reduceMotion = useReducedMotion();
  const numeric = Number.parseFloat(String(value).replace(/[^0-9.]/g, ''));
  const suffix = String(value).replace(/[0-9.]/g, '');
  const motionValue = useMotionValue(0);
  const springValue = useSpring(motionValue, { stiffness: 80, damping: 18 });
  const [displayValue, setDisplayValue] = useState(value);

  useEffect(() => {
    if (!Number.isFinite(numeric) || reduceMotion) {
      setDisplayValue(value);
      return undefined;
    }
    motionValue.set(numeric);
    const unsubscribe = springValue.on('change', (latest) => {
      setDisplayValue(`${latest.toFixed(numeric % 1 ? 1 : 0)}${suffix}`);
    });
    return unsubscribe;
  }, [motionValue, numeric, reduceMotion, springValue, suffix, value]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={reduceMotion ? undefined : { y: -7, rotateX: 1.4, rotateY: -1.2 }}
      transition={{ duration: 0.42, delay, ease: [0.16, 1, 0.3, 1] }}
      className="glass premium-surface relative rounded-lg p-5"
    >
      <div className="flex items-start justify-between gap-3">
        <div className={cn('rounded-lg bg-gradient-to-br p-3', toneClass[tone])}>
          <Icon className="h-5 w-5" />
        </div>
        <span className="inline-flex items-center gap-1 rounded-full bg-white/60 px-2.5 py-1 text-xs font-medium text-agri-700 dark:bg-white/10 dark:text-agri-200">
          {trend}
          <ArrowUpRight className="h-3.5 w-3.5" />
        </span>
      </div>
      <p className="mt-5 text-sm text-slate-500 dark:text-slate-400">{label}</p>
      <p className="mt-1 text-3xl font-semibold text-graphite-900 dark:text-white">{displayValue}</p>
    </motion.div>
  );
}
