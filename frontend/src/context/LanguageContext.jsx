import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { installAutoTranslator } from '../i18n/autoTranslate.js';
import { translations } from '../i18n/translations.js';

const LanguageContext = createContext(null);

function getNestedValue(source, path) {
  return path.split('.').reduce((value, key) => value?.[key], source);
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(() => localStorage.getItem('agrisense-language') || 'zh');

  useEffect(() => {
    localStorage.setItem('agrisense-language', language);
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : language;
    document.documentElement.dir = language === 'ur' ? 'rtl' : 'ltr';
    return installAutoTranslator(language);
  }, [language]);

  const value = useMemo(() => {
    const t = (key) => getNestedValue(translations[language], key) || getNestedValue(translations.en, key) || key;
    return {
      language,
      setLanguage,
      isChinese: language === 'zh',
      t
    };
  }, [language]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used inside LanguageProvider');
  }
  return context;
}
