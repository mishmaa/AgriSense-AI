import { Bell, Menu, Moon, Search, Sun, UserCircle } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext.jsx';
import { useTheme } from '../../context/ThemeContext.jsx';

export default function Topbar({ onMenu }) {
  const { isDark, toggleTheme } = useTheme();
  const { language, setLanguage, t } = useLanguage();

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200/70 bg-[#f6fbf7]/80 px-4 py-3 backdrop-blur-2xl dark:border-white/10 dark:bg-graphite-950/80 lg:px-6">
      <div className="flex items-center gap-3">
        <button onClick={onMenu} className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-white/10 lg:hidden" aria-label="Open navigation">
          <Menu className="h-5 w-5" />
        </button>

        <label className="relative hidden min-w-0 flex-1 md:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            className="h-11 w-full rounded-lg border border-slate-200 bg-white/75 pl-10 pr-4 text-sm outline-none transition focus:border-agri-400 dark:border-white/10 dark:bg-white/8"
            placeholder={t('topbar.search')}
          />
        </label>

        <div className="ml-auto flex items-center gap-2">
          <select
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
            className="h-10 rounded-lg border border-slate-200 bg-white/70 px-2 text-sm text-slate-700 outline-none transition hover:border-agri-400 dark:border-white/10 dark:bg-white/8 dark:text-slate-200"
            aria-label={t('topbar.language')}
          >
            <option value="zh">中文</option>
            <option value="ur">اردو</option>
            <option value="en">EN</option>
          </select>
          <button onClick={toggleTheme} className="grid h-10 w-10 place-items-center rounded-lg border border-slate-200 bg-white/70 text-slate-700 transition hover:border-agri-400 dark:border-white/10 dark:bg-white/8 dark:text-slate-200" aria-label={t('topbar.theme')}>
            {isDark ? <Sun className="h-4.5 w-4.5" /> : <Moon className="h-4.5 w-4.5" />}
          </button>
          <button className="relative grid h-10 w-10 place-items-center rounded-lg border border-slate-200 bg-white/70 text-slate-700 transition hover:border-agri-400 dark:border-white/10 dark:bg-white/8 dark:text-slate-200" aria-label={t('topbar.notifications')}>
            <Bell className="h-4.5 w-4.5" />
            <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-rose-500" />
          </button>
          <button className="flex h-10 items-center gap-2 rounded-lg border border-slate-200 bg-white/70 px-3 text-sm text-slate-700 transition hover:border-agri-400 dark:border-white/10 dark:bg-white/8 dark:text-slate-200">
            <UserCircle className="h-4.5 w-4.5" />
            <span className="hidden sm:inline">{t('topbar.user')}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
