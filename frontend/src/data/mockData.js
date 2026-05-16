import {
  Activity,
  Bell,
  Bot,
  CalendarDays,
  CloudSun,
  Droplets,
  FlaskConical,
  Gauge,
  Leaf,
  Map,
  Microscope,
  PanelsTopLeft,
  RadioTower,
  Settings,
  ShieldCheck,
  ShoppingBag,
  Satellite,
  Sprout,
  ThermometerSun,
  User,
  Waves
} from 'lucide-react';

export const navItems = [
  { key: 'dashboard', label: 'Dashboard', path: '/app/dashboard', icon: PanelsTopLeft },
  { key: 'sensors', label: 'Sensors', path: '/app/sensors', icon: RadioTower },
  { key: 'irrigation', label: 'Irrigation', path: '/app/irrigation', icon: Droplets },
  { key: 'weather', label: 'Weather', path: '/app/weather', icon: CloudSun },
  { key: 'aiCrop', label: 'AI Crop', path: '/app/ai-crop', icon: Sprout },
  { key: 'fertilizer', label: 'Fertilizer AI', path: '/app/fertilizer', icon: FlaskConical },
  { key: 'disease', label: 'Disease', path: '/app/disease', icon: Microscope },
  { key: 'satellite', label: 'Satellite', path: '/app/satellite', icon: Satellite },
  { key: 'marketplace', label: 'Marketplace', path: '/app/marketplace', icon: ShoppingBag },
  { key: 'calendar', label: 'Calendar', path: '/app/calendar', icon: CalendarDays },
  { key: 'drone', label: 'Drone', path: '/app/drone', icon: Map },
  { key: 'notifications', label: 'Notifications', path: '/app/notifications', icon: Bell },
  { key: 'profile', label: 'Profile', path: '/app/profile', icon: User },
  { key: 'admin', label: 'Admin', path: '/app/admin', icon: ShieldCheck },
  { key: 'settings', label: 'Settings', path: '/app/settings', icon: Settings }
];

export const liveSensorSeries = [
  { time: '06:00', moisture: 41, temperature: 23, humidity: 78, tank: 92, ph: 6.7, npk: 82 },
  { time: '07:00', moisture: 39, temperature: 24, humidity: 75, tank: 91, ph: 6.6, npk: 81 },
  { time: '08:00', moisture: 36, temperature: 26, humidity: 72, tank: 89, ph: 6.6, npk: 80 },
  { time: '09:00', moisture: 34, temperature: 28, humidity: 68, tank: 86, ph: 6.5, npk: 79 },
  { time: '10:00', moisture: 47, temperature: 29, humidity: 66, tank: 81, ph: 6.6, npk: 79 },
  { time: '11:00', moisture: 52, temperature: 30, humidity: 63, tank: 75, ph: 6.7, npk: 78 },
  { time: '12:00', moisture: 49, temperature: 32, humidity: 59, tank: 73, ph: 6.7, npk: 78 },
  { time: '13:00', moisture: 45, temperature: 33, humidity: 57, tank: 72, ph: 6.8, npk: 77 },
  { time: '14:00', moisture: 42, temperature: 32, humidity: 60, tank: 71, ph: 6.7, npk: 77 },
  { time: '15:00', moisture: 40, temperature: 31, humidity: 63, tank: 70, ph: 6.7, npk: 76 }
];

export const statCards = [
  { label: 'Farm Health', value: '91%', trend: '+4.8%', icon: Activity, tone: 'emerald' },
  { label: 'Soil Moisture', value: '40%', trend: '-2.1%', icon: Waves, tone: 'cyan' },
  { label: 'Tank Reserve', value: '70%', trend: '-6.0%', icon: Droplets, tone: 'blue' },
  { label: 'Yield Forecast', value: '7.8t', trend: '+12%', icon: Leaf, tone: 'amber' }
];

export const sensorWidgets = [
  { label: 'Soil Moisture', value: 40, unit: '%', icon: Waves, status: 'Auto-watch', min: 35, max: 70 },
  { label: 'Temperature', value: 31, unit: 'C', icon: ThermometerSun, status: 'Warm', min: 20, max: 35 },
  { label: 'Humidity', value: 63, unit: '%', icon: Gauge, status: 'Stable', min: 45, max: 85 },
  { label: 'Water Tank', value: 70, unit: '%', icon: Droplets, status: 'Enough', min: 25, max: 100 }
];

export const aiInsights = [
  {
    title: 'Irrigation window',
    score: 86,
    body: 'Zone B soil moisture is trending below target. Run a 14-minute drip cycle before 16:00.'
  },
  {
    title: 'Crop recommendation',
    score: 82,
    body: 'Current NPK and pH favor maize or soybean in the next rotation cycle.'
  },
  {
    title: 'Weather risk',
    score: 74,
    body: 'Moderate heat stress is expected tomorrow afternoon. Increase canopy inspection frequency.'
  }
];

export const zoneRows = [
  { zone: 'North Field', crop: 'Tomato', moisture: '42%', status: 'Healthy', irrigation: 'Auto' },
  { zone: 'Greenhouse A', crop: 'Lettuce', moisture: '58%', status: 'Optimal', irrigation: 'Scheduled' },
  { zone: 'Zone B', crop: 'Maize', moisture: '34%', status: 'Attention', irrigation: 'Auto' },
  { zone: 'Orchard Edge', crop: 'Citrus', moisture: '46%', status: 'Healthy', irrigation: 'Manual' }
];

export const weatherRows = [
  { day: 'Today', condition: 'Partly cloudy', temp: '31 C', rain: '12%', risk: 'Low' },
  { day: 'Tomorrow', condition: 'Hot afternoon', temp: '34 C', rain: '8%', risk: 'Medium' },
  { day: 'Sunday', condition: 'Light rain', temp: '28 C', rain: '62%', risk: 'Low' },
  { day: 'Monday', condition: 'Thunder risk', temp: '29 C', rain: '71%', risk: 'High' }
];

export const marketplaceItems = [
  { title: 'Organic NPK Blend', category: 'Fertilizer', price: '$28', stock: '240 bags', seller: 'GreenLoop Co.', rating: 4.8, reviews: 126, location: 'Yuen Long' },
  { title: 'Drip Irrigation Kit', category: 'Equipment', price: '$145', stock: '18 kits', seller: 'AquaField', rating: 4.7, reviews: 84, location: 'Shenzhen' },
  { title: 'Hybrid Maize Seeds', category: 'Seeds', price: '$34', stock: '86 packs', seller: 'SeedWorks', rating: 4.9, reviews: 211, location: 'Kowloon' },
  { title: 'Drone Crop Scan', category: 'Service', price: '$99', stock: 'On demand', seller: 'SkyFarm AI', rating: 4.6, reviews: 52, location: 'Hong Kong' }
];

export const notifications = [
  { title: 'Moisture alert', message: 'Zone B dropped below 35%. Irrigation recommended.', severity: 'Critical', time: '4 min ago' },
  { title: 'Weather intelligence', message: 'Rain probability rose to 62% for Sunday.', severity: 'Info', time: '22 min ago' },
  { title: 'Disease scan ready', message: 'Leaf image classified with 81% confidence.', severity: 'Warning', time: '1 hr ago' },
  { title: 'Marketplace order', message: 'Organic NPK Blend inquiry from Greenhouse A.', severity: 'Info', time: '2 hr ago' }
];

export const calendarEvents = [
  { date: '15 May', title: 'Apply micronutrient spray', crop: 'Tomato', status: 'Today', type: 'Fertilizing', progress: 72 },
  { date: '16 May', title: 'Inspect drip lines', crop: 'Maize', status: 'Planned', type: 'Irrigation', progress: 38 },
  { date: '18 May', title: 'Harvest batch A', crop: 'Lettuce', status: 'Planned', type: 'Harvest', progress: 86 },
  { date: '21 May', title: 'Soil pH retest', crop: 'Citrus', status: 'Planned', type: 'Inspection', progress: 51 }
];

export const satelliteZones = [
  { zone: 'North Field', health: 91, ndvi: 0.82, moisture: 42, condition: 'Healthy', color: 'bg-agri-400/30 border-agri-300/70' },
  { zone: 'Greenhouse A', health: 96, ndvi: 0.88, moisture: 58, condition: 'Optimal', color: 'bg-cyan-300/25 border-cyan-200/70' },
  { zone: 'Zone B', health: 68, ndvi: 0.59, moisture: 34, condition: 'Water stress', color: 'bg-amber-300/30 border-amber-200/70' },
  { zone: 'Orchard Edge', health: 83, ndvi: 0.74, moisture: 46, condition: 'Stable', color: 'bg-lime-300/25 border-lime-200/70' }
];

export const fertilizerPlans = [
  { nutrient: 'Nitrogen', current: 42, target: 72, status: 'Deficient', plan: 'Apply nitrogen boost in two split doses' },
  { nutrient: 'Phosphorus', current: 56, target: 48, status: 'Stable', plan: 'Maintain current root support program' },
  { nutrient: 'Potassium', current: 39, target: 68, status: 'Low', plan: 'Add potassium fruit support before flowering' },
  { nutrient: 'pH', current: 6.2, target: 6.7, status: 'Good', plan: 'No correction needed this week' }
];

export const adminRows = [
  { metric: 'Active farms', value: '128', change: '+9%' },
  { metric: 'Online sensors', value: '1,842', change: '+14%' },
  { metric: 'Alerts resolved', value: '94%', change: '+5%' },
  { metric: 'API uptime', value: '99.96%', change: '+0.1%' }
];

export const cropOptions = ['Maize', 'Rice', 'Tomato', 'Soybean', 'Lettuce', 'Citrus'];

export const iconMap = { Bot };
