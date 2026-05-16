import { Leaf } from 'lucide-react';

export default function PageLoader() {
  return (
    <div className="grid min-h-[60vh] place-items-center px-4">
      <div className="glass rounded-lg p-6 text-center">
        <div className="mx-auto grid h-14 w-14 place-items-center rounded-lg bg-agri-500 text-white shadow-glow">
          <Leaf className="h-7 w-7 animate-pulse" />
        </div>
        <p className="mt-4 text-sm font-semibold text-graphite-900 dark:text-white">Loading AgriSense AI</p>
        <div className="skeleton-shimmer mt-4 h-2 w-56 rounded-full bg-slate-200 dark:bg-white/10" />
      </div>
    </div>
  );
}
