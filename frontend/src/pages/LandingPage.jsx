import { motion } from 'framer-motion';
import { ArrowRight, Bot, Droplets, Leaf, RadioTower, Satellite } from 'lucide-react';
import { Link } from 'react-router-dom';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import ParticleField from '../components/ui/ParticleField.jsx';
import RealtimeChart from '../components/ui/RealtimeChart.jsx';
import ScrollReveal from '../components/ui/ScrollReveal.jsx';
import { useLanguage } from '../context/LanguageContext.jsx';
import { liveSensorSeries } from '../data/mockData.js';

export default function LandingPage() {
  const { language, setLanguage, t } = useLanguage();

  return (
    <div className="min-h-screen bg-graphite-950 text-white">
      <ParticleField />
      <section className="relative min-h-[86vh] overflow-hidden bg-farm-hero bg-cover bg-center">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-5 lg:px-6">
          <Link to="/" className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-lg bg-agri-500 shadow-glow">
              <Leaf className="h-5 w-5" />
            </span>
            <span className="text-lg font-semibold">AgriSense AI</span>
          </Link>
          <div className="flex items-center gap-2">
            <select
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
              className="h-10 rounded-lg border border-white/20 bg-white/10 px-2 text-sm text-white outline-none backdrop-blur"
              aria-label="Language"
            >
              <option value="zh">中文</option>
              <option value="ur">اردو</option>
              <option value="en">EN</option>
            </select>
            <Link to="/login" className="rounded-lg px-4 py-2 text-sm font-medium text-white/85 transition hover:bg-white/10">
              {t('landing.signin')}
            </Link>
            <Link to="/app/dashboard" className="inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-semibold text-graphite-950 transition hover:bg-agri-100">
              {t('landing.launch')}
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </nav>

        <div className="mx-auto grid min-h-[calc(86vh-88px)] max-w-7xl content-center gap-10 px-4 pb-14 lg:px-6">
          <motion.div initial={{ opacity: 0, y: 22 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }} className="max-w-3xl">
            <p className="text-sm font-semibold uppercase text-agri-200">{t('landing.eyebrow')}</p>
            <h1 className="mt-4 max-w-4xl text-5xl font-semibold leading-tight text-balance md:text-7xl">{t('landing.title')}</h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-white/78 md:text-lg">
              {t('landing.description')}
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/app/dashboard" className="inline-flex h-12 items-center gap-2 rounded-lg bg-agri-500 px-5 text-sm font-semibold text-white shadow-glow transition hover:bg-agri-600">
                {t('landing.open')}
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/login" className="inline-flex h-12 items-center rounded-lg border border-white/20 bg-white/10 px-5 text-sm font-semibold text-white backdrop-blur transition hover:bg-white/16">
                {t('landing.access')}
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="-mt-14 pb-16">
        <div className="mx-auto grid max-w-7xl gap-4 px-4 lg:grid-cols-[1.1fr_0.9fr] lg:px-6">
          <ScrollReveal>
          <GlassPanel className="p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-agri-200">{t('landing.telemetry')}</p>
                <h2 className="mt-1 text-2xl font-semibold">{t('landing.farm')}</h2>
              </div>
              <span className="rounded-full bg-agri-400/20 px-3 py-1 text-xs font-semibold text-agri-100">{t('landing.streaming')}</span>
            </div>
            <RealtimeChart data={liveSensorSeries} dataKey="moisture" secondaryKey="temperature" type="line" height={270} />
          </GlassPanel>
          </ScrollReveal>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
            {[
              { icon: RadioTower, title: t('landing.cards.sensors'), body: t('landing.cards.sensorsBody') },
              { icon: Bot, title: t('landing.cards.ai'), body: t('landing.cards.aiBody') },
              { icon: Satellite, title: t('landing.cards.satellite'), body: t('landing.cards.satelliteBody') },
              { icon: Droplets, title: t('landing.cards.irrigation'), body: t('landing.cards.irrigationBody') }
            ].map((item, index) => (
              <ScrollReveal key={item.title} delay={index * 0.06}>
              <GlassPanel key={item.title} className="p-5">
                <item.icon className="h-6 w-6 text-agri-300" />
                <h3 className="mt-4 font-semibold">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-white/68">{item.body}</p>
              </GlassPanel>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
