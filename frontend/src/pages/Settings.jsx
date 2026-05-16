import { BellRing, Globe2, Languages, Lock, Mail, MessageSquare, SlidersHorizontal } from 'lucide-react';
import toast from 'react-hot-toast';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import { useTheme } from '../context/ThemeContext.jsx';

export default function Settings() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="System preferences" title="Settings" description="Configure appearance, language, security, alert channels, and automation behavior." />
      <div className="grid gap-4 lg:grid-cols-2">
        <GlassPanel className="p-5">
          <div className="flex items-center gap-2">
            <SlidersHorizontal className="h-5 w-5 text-agri-500" />
            <h2 className="text-lg font-semibold">Appearance</h2>
          </div>
          <div className="mt-5 grid grid-cols-2 gap-3">
            {['dark', 'light'].map((item) => (
              <button key={item} onClick={() => setTheme(item)} className={`h-12 rounded-lg border text-sm font-semibold capitalize transition ${theme === item ? 'border-agri-500 bg-agri-500 text-white' : 'border-slate-200 bg-white/60 dark:border-white/10 dark:bg-white/8'}`}>
                {item}
              </button>
            ))}
          </div>
        </GlassPanel>
        <GlassPanel className="p-5">
          <div className="flex items-center gap-2">
            <Languages className="h-5 w-5 text-agri-500" />
            <h2 className="text-lg font-semibold">Language</h2>
          </div>
          <select className="mt-5 h-12 w-full rounded-lg border border-slate-200 bg-white/75 px-3 text-sm dark:border-white/10 dark:bg-white/8">
            <option>English</option>
            <option>Chinese</option>
            <option>Hindi</option>
            <option>Malay</option>
          </select>
        </GlassPanel>
        <SettingsSwitch icon={Globe2} title="Weather intelligence sync" body="Use farm geolocation to fetch weather risk data." />
        <SettingsSwitch icon={Lock} title="Security alerts" body="Notify farmers when unusual access or device activity is detected." />
        <SettingsSwitch icon={MessageSquare} title="SMS irrigation alerts" body="Send SMS when soil moisture drops, tank level is low, or irrigation automation changes state." />
        <SettingsSwitch icon={Mail} title="Email disease warnings" body="Send email summaries for disease detection, weather risk, and weekly farm analytics." />
      </div>
      <GlassPanel className="p-5">
        <div className="flex items-center gap-2">
          <BellRing className="h-5 w-5 text-agri-500" />
          <h2 className="text-lg font-semibold">Notification preferences</h2>
        </div>
        <div className="mt-5 grid gap-3 md:grid-cols-3">
          {['Irrigation alerts', 'Weather alerts', 'Disease warnings'].map((item) => (
            <div key={item} className="rounded-lg border border-slate-200/70 bg-white/45 p-4 dark:border-white/10 dark:bg-white/5">
              <p className="font-semibold">{item}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {['In-app', 'SMS', 'Email'].map((channel) => (
                  <span key={channel} className="rounded-full bg-agri-500/12 px-3 py-1 text-xs font-semibold text-agri-700 dark:text-agri-200">{channel}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </GlassPanel>
      <button onClick={() => toast.success('Settings saved')} className="inline-flex h-12 items-center rounded-lg bg-agri-500 px-5 text-sm font-semibold text-white shadow-glow">
        Save preferences
      </button>
    </div>
  );
}

function SettingsSwitch({ icon: Icon, title, body }) {
  return (
    <GlassPanel className="p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="flex gap-3">
          <Icon className="mt-0.5 h-5 w-5 text-agri-500" />
          <div>
            <h2 className="font-semibold">{title}</h2>
            <p className="mt-1 text-sm leading-6 text-slate-600 dark:text-slate-300">{body}</p>
          </div>
        </div>
        <button className="relative h-7 w-12 rounded-full bg-agri-500">
          <span className="absolute right-1 top-1 h-5 w-5 rounded-full bg-white" />
        </button>
      </div>
    </GlassPanel>
  );
}
