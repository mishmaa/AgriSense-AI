import { NavLink } from 'react-router-dom';
import { Leaf } from 'lucide-react';
import { navItems } from '../../data/mockData.js';
import { useLanguage } from '../../context/LanguageContext.jsx';
import { cn } from '../../utils/formatters.js';

export default function Sidebar({ onNavigate }) {
  const { t } = useLanguage();

  return (
    <aside className="flex h-full w-72 flex-col border-r border-slate-200/70 bg-white/80 p-4 backdrop-blur-2xl dark:border-white/10 dark:bg-graphite-950/80">
      <NavLink to="/" onClick={onNavigate} className="flex items-center gap-3 px-2 py-3">
        <span className="grid h-11 w-11 place-items-center rounded-lg bg-agri-500 text-white shadow-glow">
          <Leaf className="h-6 w-6" />
        </span>
        <span>
          <span className="block text-lg font-semibold text-graphite-900 dark:text-white">{t('app.name')}</span>
          <span className="block text-xs text-slate-500 dark:text-slate-400">{t('app.subtitle')}</span>
        </span>
      </NavLink>

      <nav className="mt-5 flex-1 space-y-1 overflow-y-auto pr-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            onClick={onNavigate}
            className={({ isActive }) =>
              cn(
                'flex h-11 items-center gap-3 rounded-lg px-3 text-sm font-medium transition',
                isActive
                  ? 'bg-agri-500 text-white shadow-glow'
                  : 'text-slate-600 hover:bg-agri-500/10 hover:text-agri-700 dark:text-slate-300 dark:hover:text-agri-200'
              )
            }
          >
            <item.icon className="h-4.5 w-4.5" />
            {t(`nav.${item.key}`)}
          </NavLink>
        ))}
      </nav>

      <div className="mt-4 rounded-lg border border-agri-500/20 bg-agri-500/10 p-4">
        <p className="text-sm font-semibold text-graphite-900 dark:text-white">{t('app.liveSync')}</p>
        <p className="mt-1 text-xs leading-5 text-slate-600 dark:text-slate-300">{t('app.liveSyncBody')}</p>
      </div>
    </aside>
  );
}
