import { Bell, Download, Zap } from 'lucide-react';
import AIInsightCard from '../components/ui/AIInsightCard.jsx';
import DataTable from '../components/ui/DataTable.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import HolographicFarmMap from '../components/ui/HolographicFarmMap.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import ScrollReveal from '../components/ui/ScrollReveal.jsx';
import SensorWidget from '../components/ui/SensorWidget.jsx';
import StatCard from '../components/ui/StatCard.jsx';
import { useLanguage } from '../context/LanguageContext.jsx';
import { aiInsights, sensorWidgets, statCards, zoneRows } from '../data/mockData.js';
import { useLiveTelemetry } from '../hooks/useLiveTelemetry.js';

export default function Dashboard() {
  const { current, history, socketStatus } = useLiveTelemetry();
  const { t } = useLanguage();
  const localizedStats = statCards.map((card, index) => ({
    ...card,
    label: [t('metrics.farmHealth'), t('metrics.soilMoisture'), t('metrics.tankReserve'), t('metrics.yieldForecast')][index]
  }));
  const localizedWidgets = sensorWidgets.map((widget, index) => ({
    ...widget,
    label: [t('metrics.soilMoisture'), t('metrics.temperature'), t('metrics.humidity'), t('metrics.waterTank')][index],
    status: index === 0 ? 'Auto-watch' : t('common.stable')
  }));

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow={t('dashboard.eyebrow')}
        title={t('dashboard.title')}
        description={t('dashboard.description')}
        action={
          <button className="inline-flex h-11 items-center gap-2 rounded-lg bg-agri-500 px-4 text-sm font-semibold text-white shadow-glow">
            <Download className="h-4 w-4" />
            {t('dashboard.export')}
          </button>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {localizedStats.map((card, index) => (
          <StatCard key={card.label} {...card} delay={index * 0.05} />
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {localizedWidgets.map((widget) => (
          <SensorWidget key={widget.label} {...widget} value={widget.label === 'Soil Moisture' ? current.moisture : widget.value} />
        ))}
      </div>

      <ScrollReveal>
        <HolographicFarmMap title={t('dashboard.holographic')} body={t('dashboard.holographicBody')} />
      </ScrollReveal>

      <div className="grid gap-4 xl:grid-cols-[1.35fr_0.65fr]">
        <GlassPanel className="p-5">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-graphite-900 dark:text-white">{t('dashboard.telemetry')}</h2>
              <p className="text-sm text-slate-500 dark:text-slate-400">{t('dashboard.telemetryBody')}</p>
            </div>
            <span className="rounded-full bg-agri-500/12 px-3 py-1 text-xs font-semibold text-agri-700 dark:text-agri-200">
              {socketStatus === 'connected' ? t('dashboard.websocketLive') : t('dashboard.demoStream')}
            </span>
          </div>
          <RealtimeChart data={history} type="line" dataKey="moisture" secondaryKey="temperature" height={320} />
        </GlassPanel>

        <GlassPanel className="p-5">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">{t('dashboard.autonomy')}</h2>
            <Zap className="h-5 w-5 text-agri-500" />
          </div>
          <div className="mt-6 flex justify-center">
            <ProgressRing value={91} label={t('dashboard.health')} />
          </div>
          <div className="mt-8 space-y-3">
            <StatusLine label={t('dashboard.irrigation')} value={t('dashboard.armed')} />
            <StatusLine label={t('dashboard.weatherRisk')} value={t('dashboard.low')} />
            <StatusLine label={t('dashboard.uptime')} value="99.4%" />
            <StatusLine label={t('dashboard.unread')} value="3" icon={Bell} />
          </div>
        </GlassPanel>
      </div>

      <div className="grid gap-4 xl:grid-cols-[0.75fr_1.25fr]">
        <div className="space-y-4">
          {aiInsights.map((insight) => (
            <AIInsightCard key={insight.title} {...insight} />
          ))}
        </div>
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">{t('dashboard.zones')}</h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{t('dashboard.zonesBody')}</p>
          <div className="mt-4">
            <DataTable
              columns={[
                { key: 'zone', label: 'Zone' },
                { key: 'crop', label: 'Crop' },
                { key: 'moisture', label: 'Moisture' },
                { key: 'status', label: 'Status' },
                { key: 'irrigation', label: 'Irrigation' }
              ]}
              rows={zoneRows}
            />
          </div>
        </GlassPanel>
      </div>
    </div>
  );
}

function StatusLine({ label, value, icon: Icon }) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-slate-200/70 bg-white/45 px-3 py-2 dark:border-white/10 dark:bg-white/5">
      <span className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">{Icon && <Icon className="h-4 w-4" />}{label}</span>
      <span className="text-sm font-semibold text-graphite-900 dark:text-white">{value}</span>
    </div>
  );
}
