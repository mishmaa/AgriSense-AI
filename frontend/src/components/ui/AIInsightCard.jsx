import { Bot } from 'lucide-react';
import ProgressRing from './ProgressRing.jsx';

export default function AIInsightCard({ title, body, score }) {
  return (
    <div className="glass rounded-lg p-5">
      <div className="flex items-start gap-4">
        <div className="rounded-lg bg-agri-500/14 p-3 text-agri-600 dark:text-agri-300">
          <Bot className="h-5 w-5" />
        </div>
        <div className="min-w-0 flex-1">
          <h3 className="text-base font-semibold text-graphite-900 dark:text-white">{title}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{body}</p>
        </div>
        <div className="hidden sm:block">
          <ProgressRing value={score} label="Confidence" size={86} />
        </div>
      </div>
    </div>
  );
}
