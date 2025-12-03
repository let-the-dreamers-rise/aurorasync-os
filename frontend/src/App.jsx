import { Routes, Route } from 'react-router-dom'
import MainLayout from './components/layout/MainLayout'
import Dashboard from './pages/Dashboard'
import Vehicles from './pages/Vehicles'
import Predictions from './pages/Predictions'
import Scheduling from './pages/Scheduling'
import VoiceAI from './pages/VoiceAI'
import Workshops from './pages/Workshops'
import Insights from './pages/Insights'
import SystemHealth from './pages/SystemHealth'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="vehicles" element={<Vehicles />} />
        <Route path="predictions" element={<Predictions />} />
        <Route path="scheduling" element={<Scheduling />} />
        <Route path="voice" element={<VoiceAI />} />
        <Route path="workshops" element={<Workshops />} />
        <Route path="insights" element={<Insights />} />
        <Route path="system" element={<SystemHealth />} />
      </Route>
    </Routes>
  )
}

export default App
