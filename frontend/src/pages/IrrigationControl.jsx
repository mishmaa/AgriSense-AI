import { Power, RotateCw, TimerReset } from 'lucide-react';
import toast from 'react-hot-toast';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import { liveSensorSeries, zoneRows } from '../data/mockData.js';
import { aiApi } from '../services/api.js';

export default function IrrigationControl() {
  const predict = async () => {
    const data = await aiApi.irrigationPrediction({
      soil_moisture: 34,
      temperature: 31,
      humidity: 62,
      rainfall_forecast_mm: 4,
      water_tank_level: 70,
      crop_stage: 'vegetative',
      soil_type: 'loam',
      hour_of_day: 15
    });
    toast.success(`AI recommends: ${data.result.irrigation_action.replace('_', ' ')}`);
  };

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Water automation" title="Irrigation control" description="Manual and AI-assisted irrigation controls with tank analytics and zone automation." />
      <div className="grid gap-4 lg:grid-cols-[0.75fr_1.25fr]">
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Water reserve</h2>
          <div className="mt-6 flex justify-center">
            <ProgressRing value={70} label="Tank" />
          </div>
          <div className="mt-8 grid gap-3">
            <button onClick={() => toast.success('Irrigation cycle started')} className="inline-flex h-12 items-center justify-center gap-2 rounded-lg bg-agri-500 text-sm font-semibold text-white shadow-glow">
              <Power className="h-4 w-4" />
              Start irrigation
            </button>
            <button onClick={predict} className="inline-flex h-12 items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white/70 text-sm font-semibold dark:border-white/10 dark:bg-white/8">
              <RotateCw className="h-4 w-4" />
              Recalibrate AI mode
            </button>
          </div>
        </GlassPanel>
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Water usage forecast</h2>
          <RealtimeChart data={liveSensorSeries} dataKey="tank" type="bar" height={330} />
        </GlassPanel>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {zoneRows.map((zone) => (
          <GlassPanel key={zone.zone} className="p-5">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">{zone.zone}</h3>
              <TimerReset className="h-4 w-4 text-agri-500" />
            </div>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">{zone.crop}</p>
            <div className="mt-5 h-2 rounded-full bg-slate-200 dark:bg-white/10">
              <div className="h-full rounded-full bg-agri-500" style={{ width: zone.moisture }} />
            </div>
            <p className="mt-3 text-sm font-medium">{zone.moisture} moisture</p>
          </GlassPanel>
        ))}
      </div>
    </div>
  );
}
