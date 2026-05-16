import { lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import AppShell from './components/layout/AppShell.jsx';
import ErrorBoundary from './components/ui/ErrorBoundary.jsx';
import PageLoader from './components/ui/PageLoader.jsx';

const AdminDashboard = lazy(() => import('./pages/AdminDashboard.jsx'));
const AICropRecommendation = lazy(() => import('./pages/AICropRecommendation.jsx'));
const CropCalendar = lazy(() => import('./pages/CropCalendar.jsx'));
const Dashboard = lazy(() => import('./pages/Dashboard.jsx'));
const DiseaseDetection = lazy(() => import('./pages/DiseaseDetection.jsx'));
const DroneMonitoring = lazy(() => import('./pages/DroneMonitoring.jsx'));
const FarmerProfile = lazy(() => import('./pages/FarmerProfile.jsx'));
const FertilizerAI = lazy(() => import('./pages/FertilizerAI.jsx'));
const IrrigationControl = lazy(() => import('./pages/IrrigationControl.jsx'));
const LandingPage = lazy(() => import('./pages/LandingPage.jsx'));
const LoginRegister = lazy(() => import('./pages/LoginRegister.jsx'));
const Marketplace = lazy(() => import('./pages/Marketplace.jsx'));
const Notifications = lazy(() => import('./pages/Notifications.jsx'));
const SensorAnalytics = lazy(() => import('./pages/SensorAnalytics.jsx'));
const Settings = lazy(() => import('./pages/Settings.jsx'));
const SatelliteMonitoring = lazy(() => import('./pages/SatelliteMonitoring.jsx'));
const WeatherIntelligence = lazy(() => import('./pages/WeatherIntelligence.jsx'));

export default function App() {
  return (
    <ErrorBoundary>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginRegister />} />
          <Route path="/app" element={<AppShell />}>
            <Route index element={<Navigate to="/app/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="sensors" element={<SensorAnalytics />} />
            <Route path="irrigation" element={<IrrigationControl />} />
            <Route path="weather" element={<WeatherIntelligence />} />
            <Route path="ai-crop" element={<AICropRecommendation />} />
            <Route path="fertilizer" element={<FertilizerAI />} />
            <Route path="disease" element={<DiseaseDetection />} />
            <Route path="satellite" element={<SatelliteMonitoring />} />
            <Route path="marketplace" element={<Marketplace />} />
            <Route path="calendar" element={<CropCalendar />} />
            <Route path="drone" element={<DroneMonitoring />} />
            <Route path="notifications" element={<Notifications />} />
            <Route path="profile" element={<FarmerProfile />} />
            <Route path="admin" element={<AdminDashboard />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}
