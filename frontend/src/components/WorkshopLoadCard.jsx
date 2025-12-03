import { motion } from 'framer-motion'
import { Wrench, TrendingUp, AlertTriangle } from 'lucide-react'
import { cn } from '@/utils/cn'
import Card from './ui/Card'

const WorkshopLoadCard = ({ workshop, className }) => {
  const { id, name, location, current_load, capacity, forecast_load, status } = workshop

  // Handle location - could be string or object {lat, lon}
  const locationText = typeof location === 'string' 
    ? location 
    : location?.city || location?.address || 'Location not specified'

  const loadPercentage = capacity > 0 ? (current_load / capacity) * 100 : 0
  const forecastPercentage = capacity > 0 ? (forecast_load / capacity) * 100 : 0

  const getStatusColor = () => {
    if (loadPercentage >= 90) return 'text-aurora-status-critical'
    if (loadPercentage >= 70) return 'text-aurora-status-warning'
    return 'text-aurora-status-healthy'
  }

  const getLoadBarColor = () => {
    if (loadPercentage >= 90) return 'bg-aurora-status-critical'
    if (loadPercentage >= 70) return 'bg-aurora-status-warning'
    return 'bg-aurora-accent-cyan'
  }

  return (
    <Card className={cn('hover:border-aurora-accent-blue/50 transition-all', className)}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-aurora-bg-tertiary flex items-center justify-center">
            <Wrench className="w-5 h-5 text-aurora-accent-cyan" />
          </div>
          <div>
            <h3 className="font-semibold text-aurora-text-primary">{name}</h3>
            <p className="text-sm text-aurora-text-muted">{locationText}</p>
          </div>
        </div>
        <span className={cn('text-sm font-medium', getStatusColor())}>
          {status || 'Active'}
        </span>
      </div>

      {/* Current Load */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-aurora-text-secondary">Current Load</span>
          <span className="font-medium text-aurora-text-primary">
            {current_load} / {capacity}
          </span>
        </div>
        <div className="h-2 bg-aurora-bg-tertiary rounded-full overflow-hidden">
          <motion.div
            className={cn('h-full rounded-full', getLoadBarColor())}
            initial={{ width: 0 }}
            animate={{ width: `${loadPercentage}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>
        <div className="flex justify-end">
          <span className={cn('text-xs font-medium', getStatusColor())}>
            {loadPercentage.toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Forecast */}
      {forecast_load !== undefined && (
        <div className="flex items-center gap-2 p-3 bg-aurora-bg-tertiary rounded-lg">
          <TrendingUp className="w-4 h-4 text-aurora-accent-purple" />
          <div className="flex-1">
            <p className="text-xs text-aurora-text-muted">Forecast (Next 7 Days)</p>
            <p className="text-sm font-medium text-aurora-text-primary">
              {forecast_load} bookings ({forecastPercentage.toFixed(0)}%)
            </p>
          </div>
          {forecastPercentage > 85 && (
            <AlertTriangle className="w-4 h-4 text-aurora-status-warning" />
          )}
        </div>
      )}
    </Card>
  )
}

export default WorkshopLoadCard
