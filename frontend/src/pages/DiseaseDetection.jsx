import { ImagePlus, Microscope, ShieldCheck } from 'lucide-react';
import toast from 'react-hot-toast';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import ProgressRing from '../components/ui/ProgressRing.jsx';
import { useState } from 'react';
import { aiApi } from '../services/api.js';

export default function DiseaseDetection() {
  const [result, setResult] = useState(null);
  const analyze = async () => {
    const data = await aiApi.diseaseFeatures({
      crop_name: 'tomato',
      image_url: 'demo://leaf',
      leaf_green_index: 0.48,
      spot_ratio: 0.41,
      yellowing_ratio: 0.28,
      texture_score: 0.64,
      edge_damage: 0.21
    });
    setResult(data);
    toast.success('Disease analysis complete');
  };

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Computer vision" title="Plant disease detection" description="Upload crop imagery and receive disease probability, severity, treatment, and prevention guidance." />
      <div className="grid gap-4 xl:grid-cols-[0.8fr_1.2fr]">
        <GlassPanel className="p-5">
          <h2 className="text-lg font-semibold">Leaf image upload</h2>
          <button onClick={analyze} className="mt-5 grid aspect-[4/3] w-full place-items-center rounded-lg border border-dashed border-agri-500/50 bg-agri-500/8 text-center transition hover:bg-agri-500/12">
            <span>
              <ImagePlus className="mx-auto h-10 w-10 text-agri-500" />
              <span className="mt-3 block text-sm font-semibold">Upload crop image</span>
              <span className="mt-1 block text-xs text-slate-500 dark:text-slate-400">JPG or PNG up to 8 MB</span>
            </span>
          </button>
        </GlassPanel>
        <GlassPanel className="p-5">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Diagnostic result</h2>
            <Microscope className="h-5 w-5 text-agri-500" />
          </div>
          <div className="mt-6 grid gap-6 md:grid-cols-[auto_1fr] md:items-center">
            <ProgressRing value={81} label="Confidence" />
            <div>
              <p className="text-2xl font-semibold">{result?.disease_name || 'Early blight suspected'}</p>
              <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">{result?.treatment_advice || 'Severity appears moderate. Remove infected leaves, improve airflow, and apply a copper-based fungicide if spread continues.'}</p>
              <div className="mt-5 flex flex-wrap gap-2">
                {['Moderate severity', 'Tomato', 'Action required'].map((tag) => (
                  <span key={tag} className="rounded-full bg-agri-500/12 px-3 py-1 text-xs font-semibold text-agri-700 dark:text-agri-200">{tag}</span>
                ))}
              </div>
            </div>
          </div>
        </GlassPanel>
      </div>
      <GlassPanel className="p-5">
        <div className="flex items-center gap-2">
          <ShieldCheck className="h-5 w-5 text-agri-500" />
          <h2 className="text-lg font-semibold">Prevention protocol</h2>
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {['Avoid overhead irrigation', 'Sanitize pruning tools', 'Rotate crop families'].map((item) => (
            <div key={item} className="rounded-lg border border-slate-200/70 bg-white/45 p-4 dark:border-white/10 dark:bg-white/5">
              <p className="font-semibold">{item}</p>
              <p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">Recommended for the next 14 days.</p>
            </div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
