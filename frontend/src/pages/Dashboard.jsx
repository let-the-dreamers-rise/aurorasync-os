import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Car, AlertTriangle, Calendar, Mic, TrendingUp, Activity } from 'lucide-react'
import Card from '@/components/ui/Card'
import StatusBadge from '@/components/ui/StatusBadge'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import SystemStatCard from '@/components/SystemStatCard'
import WorkshopLoadCard from '@/components/WorkshopLoadCard'
import PredictionResultCard from '@/components/PredictionResultCard'
import AlertBanner from '@/components/AlertBanner'
import { agentsApi } from '@/api/agents'
import { schedulingApi } from '@/api/scheduling'
import { predictionsApi } from '@/api/predictions'
import { formatRelativeTime } from '@/utils/formatters'
import { useStore } from '@/store/useStore'

const Dashboard = () => {
  const [loading, setLoading] = useState(true)
  const [agentStatus, setAgentStatus] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [workshops, setWorkshops] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      // Use mock data directly for reliable demo
      setAgentStatus(generateMockAgentStatus())
      setAnalytics(generateMockAnalytics())
      setPredictions(generateMockPredictions().slice(0, 3))
      setWorkshops(generateMockWorkshops().slice(0, 3))
      
      // Try to fetch real data in background (optional)
      Promise.all([
        agentsApi.getStatus().catch(() => null),
        schedulingApi.getAnalytics().catch(() => null),
        predictionsApi.getMockPredictions().catch(() => null),
        schedulingApi.getWorkshops().catch(() => null)
      ]).then(([agents, schedulingData, recentPredictions, workshopData]) => {
        if (agents) setAgentStatus(agents)
        if (schedulingData) setAnalytics(schedulingData.analytics || schedulingData)
        if (recentPredictions?.predictions) setPredictions(recentPredictions.predictions.slice(0, 3))
        if (workshopData?.workshops) setWorkshops(workshopData.workshops.slice(0, 3))
      }).catch(err => {
        console.log('Using mock data (backend unavailable):', err.message)
      })
      
    } catch (error) {
      console.error('Failed to load dashboard:', error)
      // Use mock data as fallback
      setAgentStatus(generateMockAgentStatus())
      setAnalytics(generateMockAnalytics())
      setPredictions(generateMockPredictions().slice(0, 3))
      setWorkshops(generateMockWorkshops().slice(0, 3))
    } finally {
      setLoading(false)
    }
  }

  // Mock data generators
  const generateMockAgentStatus = () => ({
    status: 'ok',
    master_agent: { status: 'ok' },
    data_analysis: { status: 'ok' },
    diagnosis: { status: 'ok' },
    customer_engagement: { status: 'ok' },
    scheduling: { status: 'ok' },
    feedback: { status: 'ok' },
    manufacturing: { status: 'ok' },
    ueba: { status: 'ok' },
    predictions_count: 12,
    voice_interactions: 45
  })

  const generateMockAnalytics = () => ({
    total_bookings: 28,
    total_workshops: 5,
    average_load: 68,
    total_capacity: 150
  })

  const generateMockPredictions = () => [
    {
      id: 1,
      vehicle_id: 'VEH001',
      component: 'Brake Pads',
      failure_probability: 0.82,
      probability: 0.82,
      risk_level: 'high',
      confidence: 0.89,
      days_to_failure: 15,
      days_until_failure: 15,
      recommended_action: 'Schedule immediate inspection and replacement',
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      vehicle_id: 'VEH002',
      component: 'Battery',
      failure_probability: 0.65,
      probability: 0.65,
      risk_level: 'medium',
      confidence: 0.85,
      days_to_failure: 30,
      days_until_failure: 30,
      recommended_action: 'Monitor battery voltage and schedule replacement',
      created_at: new Date(Date.now() - 3600000).toISOString()
    },
    {
      id: 3,
      vehicle_id: 'VEH003',
      component: 'Alternator',
      failure_probability: 0.45,
      probability: 0.45,
      risk_level: 'low',
      confidence: 0.78,
      days_to_failure: 60,
      days_until_failure: 60,
      recommended_action: 'Include in next scheduled maintenance',
      created_at: new Date(Date.now() - 7200000).toISOString()
    }
  ]

  const generateMockWorkshops = () => [
    {
      id: 1,
      name: 'AutoCare Mumbai Central',
      location: 'Mumbai, Maharashtra',
      current_load: 45,
      capacity: 60,
      forecast_load: 52,
      status: 'active'
    },
    {
      id: 2,
      name: 'ServicePro Delhi',
      location: 'Delhi, NCR',
      current_load: 55,
      capacity: 70,
      forecast_load: 62,
      status: 'active'
    },
    {
      id: 3,
      name: 'QuickFix Bangalore',
      location: 'Bangalore, Karnataka',
      current_load: 38,
      capacity: 50,
      forecast_load: 45,
      status: 'active'
    }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <LoadingSpinner size="xl" />
      </div>
    )
  }

  const stats = [
    {
      label: 'Total Vehicles',
      value: '10',
      icon: Car,
      color: 'blue',
      trend: '+2 this month'
    },
    {
      label: 'Active Predictions',
      value: agentStatus?.predictions_count || '0',
      icon: AlertTriangle,
      color: 'red',
      trend: '3 high risk'
    },
    {
      label: 'Scheduled Services',
      value: analytics?.total_bookings || '0',
      icon: Calendar,
      color: 'green',
      trend: '5 this week'
    },
    {
      label: 'Voice Interactions',
      value: agentStatus?.voice_interactions || '0',
      icon: Mic,
      color: 'purple',
      trend: '85% acceptance'
    },
  ]

  const agentsList = [
    { name: 'Master Agent', status: agentStatus?.master_agent?.status || 'ok', role: 'Orchestrator' },
    { name: 'Data Analysis', status: agentStatus?.data_analysis?.status || 'ok', role: 'Feature Extraction' },
    { name: 'Diagnosis', status: agentStatus?.diagnosis?.status || 'ok', role: 'ML Prediction' },
    { name: 'Customer Engagement', status: agentStatus?.customer_engagement?.status || 'ok', role: 'Voice AI' },
    { name: 'Scheduling', status: agentStatus?.scheduling?.status || 'ok', role: 'Booking' },
    { name: 'Feedback', status: agentStatus?.feedback?.status || 'ok', role: 'Validation' },
    { name: 'Manufacturing Insights', status: agentStatus?.manufacturing?.status || 'ok', role: 'RCA/CAPA' },
    { name: 'UEBA', status: agentStatus?.ueba?.status || 'ok', role: 'Security' },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h1 className="text-3xl font-bold gradient-text mb-2">Dashboard</h1>
        <p className="text-aurora-text-secondary">
          Welcome to AuroraSync OS - The Self-Healing Vehicle Brain
        </p>
      </motion.div>

      {error && (
        <AlertBanner type="warning" message={error} onClose={() => setError(null)} />
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <SystemStatCard
              stat={{
                label: stat.label,
                value: stat.value,
                change: index === 0 ? 20 : index === 1 ? -15 : index === 2 ? 10 : 5,
                trend: index === 1 ? 'down' : 'up',
                icon: stat.icon,
                status: index === 1 ? 'warning' : 'healthy'
              }}
            />
          </motion.div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Status */}
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Activity className="w-5 h-5 text-aurora-accent-cyan" />
              Agent Status
            </h2>
            <StatusBadge status="healthy" label="All Systems Operational" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agentsList.map((agent, index) => (
              <motion.div
                key={agent.name}
                className="glass-hover rounded-lg p-4"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium">{agent.name}</h3>
                  <StatusBadge status={agent.status} size="sm" />
                </div>
                <p className="text-sm text-aurora-text-muted">{agent.role}</p>
              </motion.div>
            ))}
          </div>
        </Card>

        {/* Recent Activity */}
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-aurora-accent-green" />
            Recent Activity
          </h2>
          
          <div className="space-y-4">
            {[
              { type: 'prediction', message: 'High risk brake failure detected', vehicle: 'VEH003', time: '2 minutes ago', status: 'critical' },
              { type: 'booking', message: 'Service scheduled successfully', vehicle: 'VEH001', time: '15 minutes ago', status: 'healthy' },
              { type: 'voice', message: 'Customer engagement completed', vehicle: 'VEH002', time: '1 hour ago', status: 'healthy' },
              { type: 'rca', message: 'RCA report generated', vehicle: 'Fleet', time: '2 hours ago', status: 'warning' },
            ].map((activity, index) => (
              <motion.div
                key={index}
                className="glass-hover rounded-lg p-3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <div className="flex items-start gap-3">
                  <StatusBadge status={activity.status} size="sm" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{activity.message}</p>
                    <p className="text-xs text-aurora-text-muted mt-1">
                      {activity.vehicle} • {activity.time}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </Card>
      </div>

      {/* Recent Predictions & Workshops */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Predictions */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Recent Predictions</h2>
          {predictions.length > 0 ? (
            predictions.map((pred, idx) => (
              <PredictionResultCard key={idx} prediction={pred} />
            ))
          ) : (
            <Card>
              <p className="text-center text-aurora-text-muted py-8">No recent predictions</p>
            </Card>
          )}
        </div>

        {/* Workshop Load */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Workshop Status</h2>
          {workshops.length > 0 ? (
            workshops.map((workshop, idx) => (
              <WorkshopLoadCard key={idx} workshop={workshop} />
            ))
          ) : (
            <Card>
              <p className="text-center text-aurora-text-muted py-8">No workshop data available</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
