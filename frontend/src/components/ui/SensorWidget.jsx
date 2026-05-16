import { motion } from 'framer-motion';

export default function SensorWidget({ label, value, unit, icon: Icon, status, min, max }) {
  const percentage = Math.min(100, Math.max(0, ((value - min) / (max - min)) * 100));

  return (
    <motion.div whileHover={{ y: -3 }} className="glass rounded-lg p-4">
      <div className="flex items-center justify-between">
        <div className="rounded-lg bg-agri-500/12 p-2 text-agri-600 dark:text-agri-300">
          <Icon className="h-5 w-5" />
        </div>
        <span className="text-xs text-slate-500 dark:text-slate-400">{status}</span>
      </div>
      <div className="mt-5 flex items-end gap-1">
        <span className="text-3xl font-semibold text-graphite-900 dark:text-white">{value}</span>
        <span className="mb-1 text-sm text-slate-500 dark:text-slate-400">{unit}</span>
      </div>
      <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{label}</p>
      <div className="mt-4 h-2 rounded-full bg-slate-200 dark:bg-white/10">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          className="h-full rounded-full bg-gradient-to-r from-agri-400 to-cyan-300"
        />
      </div>
    </motion.div>
  );
}
