import { Activity, Crosshair, Map, Plane, RadioTower, Satellite } from 'lucide-react';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import { liveSensorSeries } from '../data/mockData.js';

export default function DroneMonitoring() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Aerial intelligence" title="Drone monitoring" description="Plan missions, visualize scouting paths, and summarize crop stress observations from aerial imagery." />
      <div className="grid gap-4 xl:grid-cols-[1.25fr_0.75fr]">
        <GlassPanel className="relative min-h-[440px] overflow-hidden p-5">
          <div className="absolute inset-0 opacity-80 [background-image:linear-gradient(rgba(18,183,106,0.18)_1px,transparent_1px),linear-gradient(90deg,rgba(18,183,106,0.18)_1px,transparent_1px)] [background-size:42px_42px]" />
          <div className="absolute left-[18%] top-[22%] h-28 w-40 rounded-lg border border-agri-400/50 bg-agri-500/12" />
          <div className="absolute right-[22%] top-[34%] h-32 w-44 rounded-lg border border-cyan-300/50 bg-cyan-400/12" />
          <div className="absolute bottom-[18%] left-[38%] h-24 w-48 rounded-lg border border-amber-300/50 bg-amber-300/12" />
          <div className="relative flex items-center justify-between">
            <h2 className="text-lg font-semibold">Mission map</h2>
            <Satellite className="h-5 w-5 text-agri-500" />
          </div>
          <div className="absolute left-[20%] top-[24%] grid h-10 w-10 place-items-center rounded-full bg-agri-500 text-white shadow-glow">
            <Plane className="h-5 w-5" />
          </div>
          <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <path d="M20 30 C34 18, 52 56, 72 42 S88 66, 58 78" fill="none" stroke="rgba(113,239,173,0.9)" strokeDasharray="2 2" strokeWidth="0.7" />
          </svg>
          <div className="absolute right-[28%] top-[40%] grid h-9 w-9 place-items-center rounded-full bg-cyan-500 text-white">
            <Crosshair className="h-4 w-4" />
          </div>
        </GlassPanel>
        <div className="space-y-4">
          <GlassPanel className="p-5">
            <Map className="h-6 w-6 text-agri-500" />
            <h2 className="mt-4 text-lg font-semibold">North Field Scout</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Mission planned for 16:30 with multispectral sweep over tomato and maize zones.</p>
            <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
              <span className="rounded-lg bg-white/60 p-2 dark:bg-white/8"><RadioTower className="mx-auto mb-1 h-4 w-4 text-agri-500" /> 5G link</span>
              <span className="rounded-lg bg-white/60 p-2 dark:bg-white/8"><Activity className="mx-auto mb-1 h-4 w-4 text-agri-500" /> Live scan</span>
              <span className="rounded-lg bg-white/60 p-2 dark:bg-white/8"><Satellite className="mx-auto mb-1 h-4 w-4 text-agri-500" /> NDVI</span>
            </div>
          </GlassPanel>
          <GlassPanel className="p-5">
            <div className="flex justify-center">
              <ProgressRing value={68} label="Coverage" />
            </div>
          </GlassPanel>
          <GlassPanel className="p-5">
            <h2 className="font-semibold">AI findings</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Potential water stress cluster on the western edge. Recommend ground inspection before next irrigation run.</p>
          </GlassPanel>
        </div>
      </div>
      <GlassPanel className="p-5">
        <h2 className="text-lg font-semibold">Aerial analytics stream</h2>
        <RealtimeChart data={liveSensorSeries} dataKey="moisture" secondaryKey="temperature" type="line" height={260} />
      </GlassPanel>
    </div>
  );
}
