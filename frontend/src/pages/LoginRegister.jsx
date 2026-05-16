import { motion } from 'framer-motion';
import { ArrowRight, Leaf, Lock, Mail, User } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext.jsx';

export default function LoginRegister() {
  const [mode, setMode] = useState('login');
  const { t } = useLanguage();

  const submit = (event) => {
    event.preventDefault();
    toast.success(`${mode === 'login' ? 'Signed in' : 'Account created'} for demo mode`);
  };

  return (
    <div className="grid min-h-screen bg-[#f6fbf7] text-graphite-900 dark:bg-graphite-950 dark:text-white lg:grid-cols-[0.95fr_1.05fr]">
      <section className="relative hidden overflow-hidden bg-farm-hero bg-cover bg-center lg:block">
        <div className="absolute inset-0 bg-graphite-950/25" />
        <div className="relative flex h-full flex-col justify-between p-10">
          <Link to="/" className="flex items-center gap-3">
            <span className="grid h-11 w-11 place-items-center rounded-lg bg-agri-500 text-white shadow-glow">
              <Leaf className="h-6 w-6" />
            </span>
            <span className="text-xl font-semibold text-white">AgriSense AI</span>
          </Link>
          <div className="max-w-xl">
            <p className="text-sm font-semibold uppercase text-agri-200">AgriSense AI</p>
            <h1 className="mt-4 text-5xl font-semibold leading-tight text-white">{t('auth.sideTitle')}</h1>
            <p className="mt-5 text-base leading-7 text-white/75">{t('auth.sideBody')}</p>
          </div>
        </div>
      </section>

      <section className="grid place-items-center px-4 py-10">
        <motion.form initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6">
          <div className="flex items-center gap-3 lg:hidden">
            <span className="grid h-10 w-10 place-items-center rounded-lg bg-agri-500 text-white">
              <Leaf className="h-5 w-5" />
            </span>
            <span className="font-semibold">AgriSense AI</span>
          </div>
          <h2 className="mt-6 text-3xl font-semibold">{mode === 'login' ? t('auth.titleLogin') : t('auth.titleRegister')}</h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{t('auth.subtitle')}</p>

          <div className="mt-6 grid grid-cols-2 rounded-lg bg-slate-100 p-1 dark:bg-white/8">
            {['login', 'register'].map((item) => (
              <button key={item} type="button" onClick={() => setMode(item)} className={`h-10 rounded-md text-sm font-medium capitalize transition ${mode === item ? 'bg-white text-agri-700 shadow-sm dark:bg-white/14 dark:text-agri-200' : 'text-slate-500'}`}>
                {t(`auth.${item}`)}
              </button>
            ))}
          </div>

          <div className="mt-6 space-y-4">
            {mode === 'register' && <Field icon={User} placeholder={t('auth.name')} />}
            <Field icon={Mail} placeholder={t('auth.email')} type="email" />
            <Field icon={Lock} placeholder={t('auth.password')} type="password" />
          </div>

          <button className="mt-6 inline-flex h-12 w-full items-center justify-center gap-2 rounded-lg bg-agri-500 text-sm font-semibold text-white shadow-glow transition hover:bg-agri-600">
            {t('auth.continue')}
            <ArrowRight className="h-4 w-4" />
          </button>
          <Link to="/app/dashboard" className="mt-4 block text-center text-sm font-medium text-agri-600 dark:text-agri-300">
            {t('auth.demo')}
          </Link>
        </motion.form>
      </section>
    </div>
  );
}

function Field({ icon: Icon, ...props }) {
  return (
    <label className="relative block">
      <Icon className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
      <input className="h-12 w-full rounded-lg border border-slate-200 bg-white/75 pl-10 pr-4 text-sm outline-none transition focus:border-agri-400 dark:border-white/10 dark:bg-white/8" {...props} />
    </label>
  );
}
