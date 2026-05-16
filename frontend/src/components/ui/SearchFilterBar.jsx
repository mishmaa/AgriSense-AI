import { Filter, Search } from 'lucide-react';

export default function SearchFilterBar({ placeholder = 'Search', filters = [] }) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      <label className="relative min-w-0 flex-1">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          className="h-11 w-full rounded-lg border border-slate-200 bg-white/75 pl-10 pr-4 text-sm outline-none transition focus:border-agri-400 dark:border-white/10 dark:bg-white/8"
          placeholder={placeholder}
        />
      </label>
      <div className="flex flex-wrap gap-2">
        {filters.map((filter) => (
          <button
            key={filter}
            className="inline-flex h-11 items-center gap-2 rounded-lg border border-slate-200 bg-white/70 px-3 text-sm text-slate-700 transition hover:border-agri-400 dark:border-white/10 dark:bg-white/8 dark:text-slate-200"
          >
            <Filter className="h-4 w-4" />
            {filter}
          </button>
        ))}
      </div>
    </div>
  );
}
