import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Wrench, MapPin, Users, TrendingUp, Clock } from 'lucide-react'
import Card from '@/components/ui/Card'
import StatusBadge from '@/components/ui/StatusBadge'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import WorkshopLoadCard from '@/components/WorkshopLoadCard'
import ForecastGraph from '@/components/ForecastGraph'
import { schedulingApi } from '@/api/scheduling'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

const Workshops = () => {
  const [loading, setLoading] = useState(true)
  const [workshops, setWorkshops] = useState([])
  const [selectedWorkshop, setSelectedWorkshop] = useState(null)
  const [forecast, setForecast] = useState(null)

  useEffect(() => {
    loadWorkshops()
  }, [])

  const loadWorkshops = async () => {
    try {
      setLoading(true)
      const result = await schedulingApi.getWorkshops()
      setWorkshops(result.workshops || [])
    } catch (error) {
      console.error('Failed to load workshops:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadForecast = async (workshopId) => {
    try {
      const result = await schedulingApi.getDemandForecast(workshopId, 7)
      setForecast(result)
    } catch (error) {
      console.error('Failed to load forecast:', error)
    }
  }

  const handleWorkshopClick = (workshop) => {
    setSelectedWorkshop(workshop)
    loadForecast(workshop.id)
  }

  const getStatusFromLoad = (load) => {
    if (load >= 90) return 'critical'
    if (load >= 70) return 'warning'
    return 'healthy'
  }

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
      >
        <h1 className="text-3xl font-bold gradient-text mb-2">Workshops</h1>
        <p className="text-aurora-text-secondary">
          Workshop capacity, load balancing, and demand forecasting
        </p>
      </motion.div>

      {/* Workshops Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {workshops.map((workshop, index) => (
          <motion.div
            key={workshop.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card
              hover
              glow
              glowColor={getStatusFromLoad(workshop.current_load) === 'critical' ? 'red' : 'blue'}
              onClick={() => handleWorkshopClick(workshop)}
              className="cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold mb-1">{workshop.name}</h3>
                  <p className="text-sm text-aurora-text-muted flex items-center gap-1">
                    <MapPin className="w-3 h-3" />
                    {workshop.city}
                  </p>
                </div>
                <StatusBadge
                  status={getStatusFromLoad(workshop.current_load)}
                  label={workshop.status}
                  size="sm"
                />
              </div>

              {/* Load Bar */}
              <div className="mb-4">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-aurora-text-muted">Current Load</span>
                  <span className="font-medium">{workshop.current_load}%</span>
                </div>
                <div className="h-2 bg-aurora-bg-tertiary rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full ${
                      workshop.current_load >= 90
                        ? 'bg-aurora-status-critical'
                        : workshop.current_load >= 70
                        ? 'bg-aurora-status-warning'
                        : 'bg-aurora-status-healthy'
                    }`}
                    initial={{ width: 0 }}
                    animate={{ width: `${workshop.current_load}%` }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                  />
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-aurora-text-muted mb-1">Capacity</p>
                  <p className="text-sm font-medium flex items-center gap-1">
                    <Users className="w-3 h-3" />
                    {workshop.technician_capacity}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-aurora-text-muted mb-1">Specialties</p>
                  <p className="text-sm font-medium">{workshop.specialties?.length || 0}</p>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Selected Workshop Details */}
      {selectedWorkshop && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-6"
        >
          {/* Workshop Details */}
          <Card>
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Wrench className="w-5 h-5 text-aurora-accent-blue" />
              {selectedWorkshop.name}
            </h2>

            <div className="space-y-4">
              <div className="glass rounded-lg p-4">
                <h3 className="font-medium mb-3">Location</h3>
                <p className="text-sm text-aurora-text-secondary">
                  {selectedWorkshop.address || `${selectedWorkshop.city}, India`}
                </p>
              </div>

              <div className="glass rounded-lg p-4">
                <h3 className="font-medium mb-3">Specialties</h3>
                <div className="flex flex-wrap gap-2">
                  {(selectedWorkshop.specialties || ['General', 'Brake', 'Engine']).map((specialty) => (
                    <span
                      key={specialty}
                      className="badge badge-info"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
              </div>

              <div className="glass rounded-lg p-4">
                <h3 className="font-medium mb-3">Operating Hours</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-aurora-text-muted">Weekdays</span>
                    <span className="font-medium">9:00 AM - 6:00 PM</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-aurora-text-muted">Weekends</span>
                    <span className="font-medium">10:00 AM - 4:00 PM</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Demand Forecast */}
          <Card>
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-aurora-accent-green" />
              7-Day Demand Forecast
            </h2>

            {forecast ? (
              <div className="space-y-6">
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={forecast.load_curve || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1a1f2e" />
                    <XAxis
                      dataKey="date"
                      stroke="#9ca3af"
                      style={{ fontSize: '12px' }}
                    />
                    <YAxis
                      stroke="#9ca3af"
                      style={{ fontSize: '12px' }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#151b2b',
                        border: '1px solid #1a1f2e',
                        borderRadius: '8px',
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="load"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      dot={{ fill: '#3b82f6', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>

                <div className="glass rounded-lg p-4">
                  <h3 className="font-medium mb-3">Forecast Summary</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-aurora-text-muted">Average Load</span>
                      <span className="font-medium">
                        {forecast.forecast?.average_load || 'N/A'}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-aurora-text-muted">Peak Day</span>
                      <span className="font-medium">
                        {forecast.forecast?.peak_day || 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-aurora-text-muted">Recommendation</span>
                      <span className="font-medium">
                        {forecast.forecast?.recommendation || 'Normal operations'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-[300px]">
                <LoadingSpinner />
              </div>
            )}
          </Card>
        </motion.div>
      )}
    </div>
  )
}

export default Workshops
