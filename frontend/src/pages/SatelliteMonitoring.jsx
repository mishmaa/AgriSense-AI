import { Layers, Satellite, ScanLine, ThermometerSun } from 'lucide-react';
import DataTable from '../components/ui/DataTable.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import { satelliteZones } from '../data/mockData.js';

export default function SatelliteMonitoring() {
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Orbital farm intelligence"
        title="Satellite farm monitoring"
        description="Simulated satellite imagery with health heatmaps, crop condition indicators, and interactive map overlays."
      />

      <div className="grid gap-4 xl:grid-cols-[1.35fr_0.65fr]">
        <GlassPanel className="relative min-h-[560px] overflow-hidden bg-graphite-950 p-5 text-white">
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80')] bg-cover bg-center opacity-45" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_25%,rgba(52,217,135,0.35),transparent_24%),radial-gradient(circle_at_68%_38%,rgba(251,191,36,0.28),transparent_18%),radial-gradient(circle_at_54%_72%,rgba(56,189,248,0.24),transparent_22%)]" />
          <div className="absolute inset-0 [background-image:linear-gradient(rgba(255,255,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.1)_1px,transparent_1px)] [background-size:58px_58px]" />
          <div className="relative z-10 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">Green Valley orbital layer</h2>
              <p className="mt-1 text-sm text-white/70">NDVI, water stress, canopy density, and heat overlay simulation</p>
            </div>
            <span className="inline-flex items-center gap-2 rounded-full bg-white/12 px-3 py-1 text-xs font-semibold">
              <Satellite className="h-4 w-4" />
              Sentinel pass 14:30
            </span>
          </div>

          {satelliteZones.map((zone, index) => (
            <button
              key={zone.zone}
              className={`absolute rounded-lg border p-3 text-left text-xs text-white backdrop-blur transition hover:scale-[1.03] ${zone.color} ${
                ['left-[9%] top-[22%] h-[24%] w-[31%]', 'right-[12%] top-[26%] h-[27%] w-[28%]', 'left-[28%] bottom-[16%] h-[24%] w-[36%]', 'right-[18%] bottom-[10%] h-[18%] w-[24%]'][index]
              }`}
            >
              <span className="font-semibold">{zone.zone}</span>
              <span className="mt-1 block">Health {zone.health}%</span>
              <span className="block">NDVI {zone.ndvi}</span>
            </button>
          ))}
        </GlassPanel>

        <div className="space-y-4">
          <GlassPanel className="p-5">
            <Layers className="h-6 w-6 text-agri-500" />
            <h2 className="mt-4 text-lg font-semibold">Overlay controls</h2>
            <div className="mt-4 grid gap-2">
              {['Crop health', 'Water stress', 'Heat risk', 'Drone routes'].map((item) => (
                <label key={item} className="flex items-center justify-between rounded-lg bg-white/55 px-3 py-2 text-sm dark:bg-white/8">
                  {item}
                  <input type="checkbox" defaultChecked className="h-4 w-4 accent-agri-500" />
                </label>
              ))}
            </div>
          </GlassPanel>
          <GlassPanel className="p-5">
            <div className="flex justify-center">
              <ProgressRing value={87} label="Farm health" />
            </div>
          </GlassPanel>
          <GlassPanel className="p-5">
            <h2 className="flex items-center gap-2 font-semibold"><ScanLine className="h-5 w-5 text-agri-500" /> AI scan</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">Zone B shows early water stress. Compare with soil moisture sensors before next irrigation run.</p>
          </GlassPanel>
        </div>
      </div>

      <GlassPanel className="p-5">
        <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold"><ThermometerSun className="h-5 w-5 text-agri-500" /> Crop condition indicators</h2>
        <DataTable
          columns={[
            { key: 'zone', label: 'Zone' },
            { key: 'health', label: 'Health' },
            { key: 'ndvi', label: 'NDVI' },
            { key: 'moisture', label: 'Moisture' },
            { key: 'condition', label: 'Condition' }
          ]}
          rows={satelliteZones}
        />
      </GlassPanel>
    </div>
  );
}
