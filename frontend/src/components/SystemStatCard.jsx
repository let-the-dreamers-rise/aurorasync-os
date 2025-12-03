import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { cn } from '@/utils/cn'
import Card from './ui/Card'

const SystemStatCard = ({ stat, className }) => {
  const { label, value, unit, change, trend, icon: Icon, status } = stat

  const getTrendIcon = () => {
    if (trend === 'up') return TrendingUp
    if (trend === 'down') return TrendingDown
    return Minus
  }

  const getTrendColor = () => {
    if (status === 'critical') return 'text-aurora-status-critical'
    if (status === 'warning') return 'text-aurora-status-warning'
    if (trend === 'up') return 'text-aurora-status-healthy'
    if (trend === 'down') return 'text-aurora-status-critical'
    return 'text-aurora-text-muted'
  }

  const getStatusColor = () => {
    if (status === 'critical') return 'bg-aurora-status-critical/20 border-aurora-status-critical/30'
    if (status === 'warning') return 'bg-aurora-status-warning/20 border-aurora-status-warning/30'
    if (status === 'healthy') return 'bg-aurora-status-healthy/20 border-aurora-status-healthy/30'
    return 'bg-aurora-bg-tertiary border-aurora-bg-tertiary'
  }

  const TrendIcon = getTrendIcon()

  return (
    <Card className={cn('hover:border-aurora-accent-blue/50 transition-all', className)}>
      <div className="flex items-start justify-between mb-3">
        <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center border', getStatusColor())}>
          {Icon && <Icon className="w-5 h-5 text-aurora-accent-cyan" />}
        </div>
        {change !== undefined && (
          <div className={cn('flex items-center gap-1 text-xs font-medium', getTrendColor())}>
            <TrendIcon className="w-3 h-3" />
            <span>{Math.abs(change)}%</span>
          </div>
        )}
      </div>

      <div className="space-y-1">
        <p className="text-sm text-aurora-text-muted">{label}</p>
        <div className="flex items-baseline gap-1">
          <motion.span
            className="text-3xl font-bold text-aurora-text-primary"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            {value}
          </motion.span>
          {unit && (
            <span className="text-sm text-aurora-text-muted">{unit}</span>
          )}
        </div>
      </div>

      {/* Status Indicator */}
      {status && (
        <div className="mt-3 pt-3 border-t border-aurora-bg-tertiary">
          <div className="flex items-center gap-2">
            <div className={cn(
              'w-2 h-2 rounded-full',
              status === 'healthy' && 'bg-aurora-status-healthy animate-pulse',
              status === 'warning' && 'bg-aurora-status-warning animate-pulse',
              status === 'critical' && 'bg-aurora-status-critical animate-pulse'
            )} />
            <span className="text-xs text-aurora-text-muted capitalize">{status}</span>
          </div>
        </div>
      )}
    </Card>
  )
}

export default SystemStatCard
