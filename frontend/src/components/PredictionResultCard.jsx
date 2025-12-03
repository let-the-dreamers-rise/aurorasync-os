import { motion } from 'framer-motion'
import { Brain, AlertTriangle, CheckCircle, Clock } from 'lucide-react'
import { cn } from '@/utils/cn'
import Card from './ui/Card'
import StatusBadge from './ui/StatusBadge'
import { formatDate } from '@/utils/formatters'

const PredictionResultCard = ({ prediction, className }) => {
  const {
    vehicle_id,
    component,
    failure_probability,
    risk_level,
    days_to_failure,
    recommended_action,
    confidence,
    created_at,
  } = prediction

  const getRiskColor = () => {
    if (risk_level === 'critical' || failure_probability > 0.8) return 'text-aurora-status-critical'
    if (risk_level === 'high' || failure_probability > 0.6) return 'text-aurora-status-warning'
    if (risk_level === 'medium' || failure_probability > 0.4) return 'text-aurora-status-info'
    return 'text-aurora-status-healthy'
  }

  const getRiskIcon = () => {
    if (failure_probability > 0.7) return AlertTriangle
    if (failure_probability > 0.4) return Clock
    return CheckCircle
  }

  const RiskIcon = getRiskIcon()

  return (
    <Card className={cn('hover:border-aurora-accent-blue/50 transition-all', className)}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center', 
            failure_probability > 0.7 ? 'bg-aurora-status-critical/20' : 'bg-aurora-bg-tertiary'
          )}>
            <Brain className={cn('w-5 h-5', getRiskColor())} />
          </div>
          <div>
            <h3 className="font-semibold text-aurora-text-primary">{component}</h3>
            <p className="text-sm text-aurora-text-muted">Vehicle: {vehicle_id}</p>
          </div>
        </div>
        <StatusBadge status={risk_level || 'unknown'} />
      </div>

      {/* Probability & Confidence */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="space-y-1">
          <p className="text-xs text-aurora-text-muted">Failure Probability</p>
          <div className="flex items-center gap-2">
            <RiskIcon className={cn('w-4 h-4', getRiskColor())} />
            <span className={cn('text-2xl font-bold', getRiskColor())}>
              {(failure_probability * 100).toFixed(1)}%
            </span>
          </div>
        </div>
        <div className="space-y-1">
          <p className="text-xs text-aurora-text-muted">Confidence</p>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-2 bg-aurora-bg-tertiary rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-aurora-accent-cyan rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${(confidence || 0.85) * 100}%` }}
                transition={{ duration: 0.6 }}
              />
            </div>
            <span className="text-sm font-medium text-aurora-text-primary">
              {((confidence || 0.85) * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </div>

      {/* Days to Failure */}
      {days_to_failure !== undefined && (
        <div className="flex items-center gap-2 p-3 bg-aurora-bg-tertiary rounded-lg mb-3">
          <Clock className="w-4 h-4 text-aurora-accent-purple" />
          <div>
            <p className="text-xs text-aurora-text-muted">Estimated Time to Failure</p>
            <p className="text-sm font-medium text-aurora-text-primary">
              {days_to_failure} days
            </p>
          </div>
        </div>
      )}

      {/* Recommended Action */}
      {recommended_action && (
        <div className="p-3 bg-aurora-accent-blue/10 border border-aurora-accent-blue/30 rounded-lg">
          <p className="text-xs text-aurora-accent-cyan font-medium mb-1">Recommended Action</p>
          <p className="text-sm text-aurora-text-secondary">{recommended_action}</p>
        </div>
      )}

      {/* Timestamp */}
      {created_at && (
        <div className="mt-3 pt-3 border-t border-aurora-bg-tertiary">
          <p className="text-xs text-aurora-text-muted">
            Predicted: {formatDate(created_at)}
          </p>
        </div>
      )}
    </Card>
  )
}

export default PredictionResultCard
