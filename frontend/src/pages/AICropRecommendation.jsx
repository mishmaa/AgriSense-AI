import { Bot, Sparkles } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import AIInsightCard from '../components/ui/AIInsightCard.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import { aiInsights, cropOptions } from '../data/mockData.js';
import { aiApi } from '../services/api.js';

export default function AICropRecommendation() {
  const [crop, setCrop] = useState('Maize');
  const [result, setResult] = useState(null);

  const generate = async () => {
    const data = await aiApi.cropRecommendation({
      zone_id: null,
      nitrogen: 82,
      phosphorus: 46,
      potassium: 71,
      temperature: 29,
      humidity: 66,
      ph_level: 6.7,
      rainfall_mm: 126,
      soil_type: 'loam'
    });
    setResult(data.result);
    toast.success('AI recommendation generated');
  };

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="AI agronomy" title="AI crop recommendation" description="Recommend crops using NPK balance, pH, temperature, humidity, rainfall, and soil context." />
      <div className="grid gap-4 xl:grid-cols-[0.82fr_1.18fr]">
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Recommendation inputs</h2>
          <div className="mt-5 grid gap-4">
            <label className="space-y-2">
              <span className="text-sm text-slate-500 dark:text-slate-400">Current crop</span>
              <select value={crop} onChange={(event) => setCrop(event.target.value)} className="h-11 w-full rounded-lg border border-slate-200 bg-white/75 px-3 text-sm dark:border-white/10 dark:bg-white/8">
                {cropOptions.map((option) => <option key={option}>{option}</option>)}
              </select>
            </label>
            {['Nitrogen', 'Phosphorus', 'Potassium', 'pH level', 'Rainfall'].map((label, index) => (
              <label key={label} className="space-y-2">
                <span className="text-sm text-slate-500 dark:text-slate-400">{label}</span>
                <input defaultValue={[82, 46, 71, 6.7, 126][index]} className="h-11 w-full rounded-lg border border-slate-200 bg-white/75 px-3 text-sm dark:border-white/10 dark:bg-white/8" />
              </label>
            ))}
            <button onClick={generate} className="inline-flex h-12 items-center justify-center gap-2 rounded-lg bg-agri-500 text-sm font-semibold text-white shadow-glow">
              <Sparkles className="h-4 w-4" />
              Generate recommendation
            </button>
          </div>
        </GlassPanel>
        <GlassPanel className="p-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">Recommended rotation</h2>
              <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
                {result?.explanation || `Based on current field readings, soybean is the strongest rotation after ${crop.toLowerCase()} for nitrogen recovery and market yield.`}
              </p>
            </div>
            <Bot className="h-6 w-6 text-agri-500" />
          </div>
          <div className="mt-8 flex justify-center">
            <ProgressRing value={Math.round((result?.confidence_score || 0.82) * 100)} label="Confidence" />
          </div>
          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            {[result?.recommended_crop || 'Soybean', 'Tomato', 'Rice'].map((item, index) => (
              <div key={item} className="rounded-lg border border-slate-200/70 bg-white/45 p-4 dark:border-white/10 dark:bg-white/5">
                <p className="font-semibold">{item}</p>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{[82, 76, 71][index]}% match</p>
              </div>
            ))}
          </div>
        </GlassPanel>
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        {aiInsights.map((insight) => <AIInsightCard key={insight.title} {...insight} />)}
      </div>
    </div>
  );
}
