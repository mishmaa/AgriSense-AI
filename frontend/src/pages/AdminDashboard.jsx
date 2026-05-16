import { ShieldCheck, Users } from 'lucide-react';
import DataTable from '../components/ui/DataTable.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import StatCard from '../components/ui/StatCard.jsx';
import { adminRows, liveSensorSeries } from '../data/mockData.js';

export default function AdminDashboard() {
  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Platform command" title="Admin dashboard" description="Monitor users, farms, sensor health, alert throughput, API uptime, and operational growth." />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Active farms" value="128" trend="+9%" icon={Users} tone="emerald" />
        <StatCard label="Online sensors" value="1,842" trend="+14%" icon={ShieldCheck} tone="cyan" />
        <StatCard label="Alerts resolved" value="94%" trend="+5%" icon={ShieldCheck} tone="blue" />
        <StatCard label="API uptime" value="99.96%" trend="+0.1%" icon={ShieldCheck} tone="amber" />
      </div>
      <div className="grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Platform telemetry</h2>
          <RealtimeChart data={liveSensorSeries} dataKey="npk" type="bar" height={320} />
        </GlassPanel>
        <GlassPanel className="p-5">
          <h2 className="mb-4 text-lg font-semibold">System metrics</h2>
          <DataTable columns={[{ key: 'metric', label: 'Metric' }, { key: 'value', label: 'Value' }, { key: 'change', label: 'Change' }]} rows={adminRows} />
        </GlassPanel>
      </div>
    </div>
  );
}
