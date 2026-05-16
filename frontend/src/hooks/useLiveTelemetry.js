import { useEffect, useState } from 'react';
import { liveSensorSeries } from '../data/mockData.js';

const demoFarmId = '00000000-0000-0000-0000-000000000001';

export function useLiveTelemetry(farmId = demoFarmId) {
  const [index, setIndex] = useState(0);
  const [socketStatus, setSocketStatus] = useState('demo');
  const [liveHistory, setLiveHistory] = useState([]);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setIndex((current) => (current + 1) % liveSensorSeries.length);
    }, 2600);
    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('agrisense-token');
    const wsBase = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';
    if (!token || !farmId) {
      setSocketStatus('demo');
      return undefined;
    }

    const socket = new WebSocket(`${wsBase}/ws/sensors/${farmId}?token=${encodeURIComponent(token)}`);
    socket.onopen = () => setSocketStatus('connected');
    socket.onerror = () => setSocketStatus('error');
    socket.onclose = () => setSocketStatus('closed');
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      if (payload.type !== 'sensor_reading') return;
      const reading = payload.reading;
      const point = {
        time: new Date(reading.recorded_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        moisture: Number(reading.soil_moisture ?? 0),
        temperature: Number(reading.temperature ?? 0),
        humidity: Number(reading.humidity ?? 0),
        tank: Number(reading.water_tank_level ?? 0),
        ph: Number(reading.ph_level ?? 0),
        rainfall: Number(reading.rainfall_mm ?? 0),
        light: Number(reading.light_intensity ?? 0),
        wind: Number(reading.wind_speed ?? 0),
        npk: Number(reading.nitrogen ?? 0)
      };
      setLiveHistory((current) => [...current.slice(-79), point]);
    };

    return () => socket.close();
  }, [farmId]);

  const demoHistory = liveSensorSeries.slice(0, index + 1).concat(liveSensorSeries.slice(index + 1));
  const history = liveHistory.length ? liveHistory : demoHistory;
  const current = liveHistory.length ? liveHistory[liveHistory.length - 1] : liveSensorSeries[index];

  return { current, history, socketStatus };
}
