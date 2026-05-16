import { Bell, CheckCheck } from 'lucide-react';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import SearchFilterBar from '../components/ui/SearchFilterBar.jsx';
import { notifications } from '../data/mockData.js';

export default function Notifications() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Alert center" title="Notifications" description="Sensor, irrigation, weather, AI, marketplace, and system notifications." />
      <SearchFilterBar placeholder="Search notifications" filters={['Critical', 'Unread', 'Weather']} />
      <div className="space-y-3">
        {notifications.map((item) => (
          <GlassPanel key={item.title} className="p-4">
            <div className="flex items-start gap-4">
              <div className="grid h-11 w-11 place-items-center rounded-lg bg-agri-500/12 text-agri-600 dark:text-agri-300">
                <Bell className="h-5 w-5" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="font-semibold">{item.title}</p>
                  <span className="rounded-full bg-white/60 px-2 py-0.5 text-xs text-slate-500 dark:bg-white/10 dark:text-slate-400">{item.severity}</span>
                </div>
                <p className="mt-1 text-sm leading-6 text-slate-600 dark:text-slate-300">{item.message}</p>
                <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">{item.time}</p>
              </div>
              <button className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 dark:hover:bg-white/10" aria-label="Mark as read">
                <CheckCheck className="h-5 w-5" />
              </button>
            </div>
          </GlassPanel>
        ))}
      </div>
    </div>
  );
}
