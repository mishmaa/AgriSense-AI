import { CalendarDays, CheckCircle2, Clock, Sprout } from 'lucide-react';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import SearchFilterBar from '../components/ui/SearchFilterBar.jsx';
import { calendarEvents } from '../data/mockData.js';

export default function CropCalendar() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Season planner" title="Crop calendar" description="Plan sowing, irrigation, fertilization, spraying, inspection, and harvesting tasks." />
      <SearchFilterBar placeholder="Search crop tasks" filters={['Today', 'This week', 'Overdue']} />
      <div className="grid gap-4 lg:grid-cols-[0.72fr_1.28fr]">
        <GlassPanel className="p-5">
          <CalendarDays className="h-6 w-6 text-agri-500" />
          <p className="mt-5 text-4xl font-semibold">May 2026</p>
          <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Four priority activities are scheduled this week across tomato, maize, lettuce, and citrus zones.</p>
          <div className="mt-6 grid gap-3">
            {[
              ['Planting readiness', 74],
              ['Harvest tracking', 86],
              ['Reminder coverage', 92]
            ].map(([label, value]) => (
              <div key={label}>
                <div className="flex justify-between text-sm">
                  <span>{label}</span>
                  <span>{value}%</span>
                </div>
                <div className="mt-2 h-2 rounded-full bg-slate-200 dark:bg-white/10">
                  <div className="h-full rounded-full bg-gradient-to-r from-agri-400 to-cyan-300" style={{ width: `${value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
        <div className="space-y-3">
          {calendarEvents.map((event) => (
            <GlassPanel key={event.title} className="p-4">
              <div className="flex items-center gap-4">
                <div className="grid h-14 w-16 place-items-center rounded-lg bg-agri-500/12 text-center text-sm font-semibold text-agri-700 dark:text-agri-200">{event.date}</div>
                <div className="min-w-0 flex-1">
                  <p className="font-semibold">{event.title}</p>
                  <p className="mt-1 flex flex-wrap items-center gap-3 text-sm text-slate-500 dark:text-slate-400">
                    <span className="inline-flex items-center gap-1"><Sprout className="h-4 w-4" /> {event.crop}</span>
                    <span className="inline-flex items-center gap-1"><Clock className="h-4 w-4" /> {event.type}</span>
                  </p>
                  <div className="mt-3 h-1.5 rounded-full bg-slate-200 dark:bg-white/10">
                    <div className="h-full rounded-full bg-agri-500" style={{ width: `${event.progress}%` }} />
                  </div>
                </div>
                <span className="inline-flex items-center gap-1 rounded-full bg-white/60 px-3 py-1 text-xs font-semibold text-slate-600 dark:bg-white/10 dark:text-slate-300">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  {event.status}
                </span>
              </div>
            </GlassPanel>
          ))}
        </div>
      </div>
    </div>
  );
}
