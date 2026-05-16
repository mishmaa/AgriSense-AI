import { CloudSun, Umbrella, Wind } from 'lucide-react';
import DataTable from '../components/ui/DataTable.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import StatCard from '../components/ui/StatCard.jsx';
import { liveSensorSeries, weatherRows } from '../data/mockData.js';
import { aiApi } from '../services/api.js';
import { useState } from 'react';

export default function WeatherIntelligence() {
  const [advice, setAdvice] = useState('Delay fertilizer application if Sunday rainfall remains above 60%.');

  const generateAdvice = async () => {
    const data = await aiApi.weatherSuggestion({
      crop_name: 'tomato',
      condition: 'hot',
      temperature: 34,
      humidity: 68,
      rainfall_mm: 8,
      wind_speed: 14
    });
    setAdvice(data.result.explanation);
  };

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Climate intelligence" title="Weather intelligence" description="Forecast risks, rainfall probabilities, heat stress, and irrigation adjustments." />
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Heat Stress" value="Medium" trend="+8%" icon={CloudSun} tone="amber" />
        <StatCard label="Rain Probability" value="62%" trend="+19%" icon={Umbrella} tone="cyan" />
        <StatCard label="Wind Speed" value="14km/h" trend="-2%" icon={Wind} tone="blue" />
      </div>
      <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Temperature outlook</h2>
          <RealtimeChart data={liveSensorSeries} type="line" dataKey="temperature" secondaryKey="humidity" height={320} />
        </GlassPanel>
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">AI weather advice</h2>
          <div className="mt-5 space-y-4 text-sm leading-6 text-slate-600 dark:text-slate-300">
            <p>{advice}</p>
            <p>Increase irrigation only for Zone B. Other zones should wait for expected precipitation.</p>
            <p>Inspect tomato canopy tomorrow after 15:00 for heat stress indicators.</p>
          </div>
          <button onClick={generateAdvice} className="mt-5 h-11 rounded-lg bg-agri-500 px-4 text-sm font-semibold text-white shadow-glow">Refresh AI advice</button>
        </GlassPanel>
      </div>
      <GlassPanel className="p-5">
        <h2 className="mb-4 text-lg font-semibold">Four-day forecast</h2>
        <DataTable columns={[{ key: 'day', label: 'Day' }, { key: 'condition', label: 'Condition' }, { key: 'temp', label: 'Temp' }, { key: 'rain', label: 'Rain' }, { key: 'risk', label: 'Risk' }]} rows={weatherRows} />
      </GlassPanel>
    </div>
  );
}
