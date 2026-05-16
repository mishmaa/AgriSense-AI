import { RadioTower } from 'lucide-react';
import DataTable from '../components/ui/DataTable.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import SearchFilterBar from '../components/ui/SearchFilterBar.jsx';
import SensorWidget from '../components/ui/SensorWidget.jsx';
import { liveSensorSeries, sensorWidgets, zoneRows } from '../data/mockData.js';
import { useLiveTelemetry } from '../hooks/useLiveTelemetry.js';

export default function SensorAnalytics() {
  const { history, socketStatus } = useLiveTelemetry();

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="IoT monitoring" title="Sensor analytics" description="Inspect live signals, device health, telemetry trends, and zone-level anomalies." />
      <SearchFilterBar placeholder="Search sensors or zones" filters={['Online', 'Zone', 'Anomaly']} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {sensorWidgets.map((widget) => (
          <SensorWidget key={widget.label} {...widget} />
        ))}
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <GlassPanel className="p-5">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Moisture trend</h2>
            <span className="text-xs text-slate-500 dark:text-slate-400">{socketStatus}</span>
          </div>
          <RealtimeChart data={history} dataKey="moisture" height={300} />
        </GlassPanel>
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Temperature vs humidity</h2>
          <RealtimeChart data={history.length ? history : liveSensorSeries} type="line" dataKey="temperature" secondaryKey="humidity" height={300} />
        </GlassPanel>
      </div>
      <GlassPanel className="p-5">
        <div className="mb-4 flex items-center gap-2">
          <RadioTower className="h-5 w-5 text-agri-500" />
          <h2 className="text-lg font-semibold">Sensor fleet</h2>
        </div>
        <DataTable
          columns={[
            { key: 'zone', label: 'Zone' },
            { key: 'crop', label: 'Crop' },
            { key: 'moisture', label: 'Latest' },
            { key: 'status', label: 'Health' },
            { key: 'irrigation', label: 'Mode' }
          ]}
          rows={zoneRows}
        />
      </GlassPanel>
    </div>
  );
}
