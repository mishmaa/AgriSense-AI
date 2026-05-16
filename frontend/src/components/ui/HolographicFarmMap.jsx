import { motion } from 'framer-motion';
import { Satellite, Waves } from 'lucide-react';

const plots = [
  { name: 'A1', className: 'left-[10%] top-[18%] h-[26%] w-[34%]', tone: 'bg-agri-400/18 border-agri-300/60' },
  { name: 'B2', className: 'right-[14%] top-[26%] h-[30%] w-[28%]', tone: 'bg-cyan-400/14 border-cyan-300/60' },
  { name: 'C3', className: 'bottom-[16%] left-[27%] h-[24%] w-[46%]', tone: 'bg-amber-300/16 border-amber-200/60' }
];

export default function HolographicFarmMap({ title, body }) {
  return (
    <div className="holographic-map relative min-h-[340px] overflow-hidden rounded-lg border border-white/10 bg-graphite-950/90 p-5 text-white shadow-glass">
      <div className="absolute inset-0 holo-grid" />
      <div className="relative z-10 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>
          <p className="mt-2 max-w-xl text-sm leading-6 text-white/66">{body}</p>
        </div>
        <span className="grid h-11 w-11 place-items-center rounded-lg bg-white/10 text-agri-200">
          <Satellite className="h-5 w-5" />
        </span>
      </div>

      {plots.map((plot, index) => (
        <motion.div
          key={plot.name}
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.12 * index, duration: 0.6 }}
          className={`absolute rounded-lg border ${plot.tone} ${plot.className}`}
        >
          <span className="absolute left-3 top-3 text-xs font-semibold text-white/80">{plot.name}</span>
        </motion.div>
      ))}

      <motion.div
        animate={{ x: ['-8%', '86%', '-8%'], y: ['8%', '46%', '8%'] }}
        transition={{ duration: 13, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute left-[12%] top-[26%] z-20 grid h-12 w-12 place-items-center rounded-full border border-agri-200/50 bg-agri-500 text-white shadow-glow"
      >
        <Waves className="h-5 w-5" />
      </motion.div>

      <div className="absolute bottom-5 left-5 right-5 z-10 grid gap-3 sm:grid-cols-3">
        {['NDVI 0.82', 'Moisture 40%', 'Coverage 94%'].map((item) => (
          <div key={item} className="rounded-lg border border-white/10 bg-white/8 px-3 py-2 text-sm text-white/82 backdrop-blur">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
