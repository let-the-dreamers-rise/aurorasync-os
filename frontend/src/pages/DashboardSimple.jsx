import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Car, AlertTriangle, Calendar, Mic, Activity, Brain } from 'lucide-react'
import Card from './ui/Card'
import StatusBadge from './ui/StatusBadge'
import LoadingSpinner from './ui/LoadingSpinner'

const Dashboard = () => {
  const [loading, setLoading] = useState(false)

  // Mock data
  const stats = [
    { label: 'Total Vehicles', value: '15', icon: Car, trend: '+2 this month' },
    { label: 'Active Predictions', value: '12', icon: AlertTriangle, trend: '3 high risk' },
    { label: 'Scheduled Services', value: '28', icon: Calendar, trend: '5 this week' },
    { label: 'Voice Interactions', value: '45', icon: Mic, trend: '85% acceptance' },
  ]

  const agents = [
    { name: 'Master Agent', status: 'ok', role: 'Orchestrator' },
    { name: 'Data Analysis', status: 'ok', role: 'Feature Extraction' },
    { name: 'Diagnosis', status: 'ok', role: 'ML Prediction' },
    { name: 'Customer Engagement', status: 'ok', role: 'Voice AI' },
    { name: 'Scheduling', status: 'ok', role: 'Booking' },
    { name: 'Feedback', status: 'ok', role: 'Validation' },
    { name: 'Manufacturing Insights', status: 'ok', role: 'RCA/CAPA' },
    { name: 'UEBA', status: 'ok', role: 'Security' },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <LoadingSpinner size="xl" />
      </div>
    )
  }

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

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card hover glow glowColor="blue">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-aurora-text-muted text-sm mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold mb-2">{stat.value}</p>
                  <p className="text-xs text-aurora-text-muted">{stat.trend}</p>
                </div>
                <div className="p-3 rounded-lg bg-aurora-accent-blue/20">
                  <stat.icon className="w-6 h-6 text-aurora-accent-cyan" />
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Agent Status */}
      <Card>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Activity className="w-5 h-5 text-aurora-accent-cyan" />
            Agent Status
          </h2>
          <StatusBadge status="healthy" label="All Systems Operational" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((agent, index) => (
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
        <h2 className="text-xl font-bold mb-6">Recent Activity</h2>
        <div className="space-y-4">
          {[
            { type: 'prediction', message: 'High risk brake failure detected', vehicle: 'VEH003', time: '2 minutes ago', status: 'critical' },
            { type: 'booking', message: 'Service scheduled successfully', vehicle: 'VEH001', time: '15 minutes ago', status: 'healthy' },
            { type: 'voice', message: 'Customer engagement completed', vehicle: 'VEH002', time: '1 hour ago', status: 'healthy' },
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
  )
}

export default Dashboard
