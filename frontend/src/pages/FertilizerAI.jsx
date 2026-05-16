import { FlaskConical, Sparkles } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import { fertilizerPlans } from '../data/mockData.js';
import { aiApi } from '../services/api.js';

export default function FertilizerAI() {
  const [plan, setPlan] = useState('potassium_fruit_support');

  const generate = async () => {
    try {
      const data = await aiApi.fertilizerRecommendation?.({
        crop_name: 'tomato',
        growth_stage: 'flowering',
        soil_type: 'loam',
        nitrogen: 42,
        phosphorus: 56,
        potassium: 39,
        ph_level: 6.2
      });
      setPlan(data?.result?.fertilizer_plan || 'potassium_fruit_support');
    } catch {
      setPlan('potassium_fruit_support');
    }
    toast.success('Fertilizer AI plan generated');
  };

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Nutrient intelligence"
        title="Fertilizer recommendation AI"
        description="Analyze nutrient deficiencies, soil chemistry, growth stage, and schedule fertilizer applications."
        action={
          <button onClick={generate} className="inline-flex h-11 items-center gap-2 rounded-lg bg-agri-500 px-4 text-sm font-semibold text-white shadow-glow">
            <Sparkles className="h-4 w-4" />
            Generate plan
          </button>
        }
      />

      <div className="grid gap-4 xl:grid-cols-[0.8fr_1.2fr]">
        <GlassPanel className="p-5">
          <FlaskConical className="h-6 w-6 text-agri-500" />
          <h2 className="mt-4 text-xl font-semibold">Recommended plan</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{plan.replaceAll('_', ' ')}</p>
          <div className="mt-6 flex justify-center">
            <ProgressRing value={84} label="Confidence" />
          </div>
        </GlassPanel>
        <div className="grid gap-4 md:grid-cols-2">
          {fertilizerPlans.map((item) => (
            <GlassPanel key={item.nutrient} className="p-5">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold">{item.nutrient}</h3>
                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{item.status}</p>
                </div>
                <span className="rounded-full bg-agri-500/12 px-3 py-1 text-xs font-semibold text-agri-700 dark:text-agri-200">
                  {item.current}/{item.target}
                </span>
              </div>
              <div className="mt-5 h-2 rounded-full bg-slate-200 dark:bg-white/10">
                <div className="h-full rounded-full bg-gradient-to-r from-agri-400 to-cyan-300" style={{ width: `${Math.min(100, (item.current / item.target) * 100)}%` }} />
              </div>
              <p className="mt-4 text-sm leading-6 text-slate-600 dark:text-slate-300">{item.plan}</p>
            </GlassPanel>
          ))}
        </div>
      </div>
    </div>
  );
}
