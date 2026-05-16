import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 12000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('agrisense-token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const demoFarmId = '00000000-0000-0000-0000-000000000001';

async function postOrDemo(path, payload, demoFactory) {
  try {
    const { data } = await api.post(path, payload);
    return data;
  } catch (error) {
    return demoFactory(error);
  }
}

export const aiApi = {
  cropRecommendation(payload) {
    return postOrDemo('/ai/crop-recommendation', { farm_id: demoFarmId, ...payload }, () => ({
      result: {
        recommended_crop: 'soybean',
        confidence_score: 0.82,
        explanation: 'Soybean fits the current NPK balance, pH, rainfall, and loam soil profile.',
        actions: ['Validate local market demand.', 'Run a soil test before planting.']
      }
    }));
  },
  irrigationPrediction(payload) {
    return postOrDemo('/ai/irrigation-prediction', { farm_id: demoFarmId, ...payload }, () => ({
      result: {
        irrigation_action: 'standard_cycle',
        confidence_score: 0.84,
        explanation: 'Moisture is below target and rainfall is low.',
        actions: ['Run irrigation for 15-22 minutes.', 'Recheck moisture after 30 minutes.']
      }
    }));
  },
  fertilizerRecommendation(payload) {
    return postOrDemo('/ai/fertilizer-recommendation', { farm_id: demoFarmId, ...payload }, () => ({
      result: {
        fertilizer_plan: 'potassium_fruit_support',
        confidence_score: 0.84,
        explanation: 'Potassium is low for the current crop and growth stage.',
        actions: ['Apply potassium support before flowering.', 'Split doses and avoid heavy rain windows.']
      }
    }));
  },
  weatherSuggestion(payload) {
    return postOrDemo('/ai/weather-suggestion', { farm_id: demoFarmId, ...payload }, () => ({
      result: {
        suggestion_type: 'heat_protection',
        confidence_score: 0.78,
        explanation: 'Heat stress is likely. Irrigate early and inspect canopy stress.',
        actions: ['Irrigate before peak heat.', 'Shade sensitive seedlings.']
      }
    }));
  },
  diseaseFeatures(payload) {
    return postOrDemo('/disease-detection/features', { farm_id: demoFarmId, ...payload }, () => ({
      disease_name: 'early blight',
      confidence_score: 0.81,
      treatment_advice: 'Remove infected leaves and improve airflow.',
      prevention_advice: 'Avoid overhead irrigation and capture follow-up images.'
    }));
  },
  chatbot(message) {
    return postOrDemo('/chatbot/message', { message, language: 'en' }, () => ({
      reply: 'Check soil moisture and rainfall forecast. If moisture is below 35%, run targeted irrigation for the affected zone.'
    }));
  }
};
