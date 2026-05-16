import { MapPin, Phone, UserCircle } from 'lucide-react';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';

export default function FarmerProfile() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Farmer identity" title="Profile management" description="Manage farmer details, farm portfolio, language preference, and notification channels." />
      <div className="grid gap-4 xl:grid-cols-[0.75fr_1.25fr]">
        <GlassPanel className="p-5">
          <div className="flex flex-col items-center text-center">
            <div className="grid h-24 w-24 place-items-center rounded-full bg-agri-500/12 text-agri-600 dark:text-agri-300">
              <UserCircle className="h-14 w-14" />
            </div>
            <h2 className="mt-4 text-2xl font-semibold">Mira Chen</h2>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Owner, Green Valley Farm</p>
            <div className="mt-6">
              <ProgressRing value={94} label="Profile" />
            </div>
          </div>
        </GlassPanel>
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Profile details</h2>
          <div className="mt-5 grid gap-4 sm:grid-cols-2">
            {[
              ['Full name', 'Mira Chen'],
              ['Email', 'mira@agrisense.demo'],
              ['Phone', '+852 5555 0128'],
              ['Language', 'English'],
              ['Primary crop', 'Tomato, Maize'],
              ['Farm area', '42.8 hectares']
            ].map(([label, value]) => (
              <label key={label} className="space-y-2">
                <span className="text-sm text-slate-500 dark:text-slate-400">{label}</span>
                <input defaultValue={value} className="h-11 w-full rounded-lg border border-slate-200 bg-white/75 px-3 text-sm dark:border-white/10 dark:bg-white/8" />
              </label>
            ))}
          </div>
          <div className="mt-5 flex flex-wrap gap-3 text-sm text-slate-600 dark:text-slate-300">
            <span className="inline-flex items-center gap-2"><MapPin className="h-4 w-4 text-agri-500" /> Yuen Long, Hong Kong</span>
            <span className="inline-flex items-center gap-2"><Phone className="h-4 w-4 text-agri-500" /> SMS alerts enabled</span>
          </div>
        </GlassPanel>
      </div>
    </div>
  );
}
