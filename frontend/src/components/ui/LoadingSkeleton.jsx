export default function LoadingSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {[0, 1, 2].map((item) => (
        <div key={item} className="glass rounded-lg p-5">
          <div className="skeleton-shimmer h-4 w-24 rounded bg-slate-200 dark:bg-white/10" />
          <div className="skeleton-shimmer mt-6 h-8 w-32 rounded bg-slate-200 dark:bg-white/10" />
          <div className="skeleton-shimmer mt-4 h-3 w-full rounded bg-slate-200 dark:bg-white/10" />
        </div>
      ))}
    </div>
  );
}
