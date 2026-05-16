import { motion } from 'framer-motion';

export default function PageHeader({ eyebrow, title, description, action }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"
    >
      <div className="max-w-3xl">
        {eyebrow && <p className="text-xs font-semibold uppercase text-agri-600 dark:text-agri-300">{eyebrow}</p>}
        <h1 className="mt-2 text-3xl font-semibold text-graphite-900 dark:text-white md:text-4xl">{title}</h1>
        {description && <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">{description}</p>}
      </div>
      {action}
    </motion.div>
  );
}
