import { motion } from 'framer-motion'
import { cn } from '@/utils/cn'

const StatusBadge = ({ status, label, size = 'md', animated = true }) => {
  const statusConfig = {
    healthy: {
      bg: 'bg-aurora-status-healthy/20',
      text: 'text-aurora-status-healthy',
      border: 'border-aurora-status-healthy/30',
      glow: 'shadow-glow-green',
    },
    warning: {
      bg: 'bg-aurora-status-warning/20',
      text: 'text-aurora-status-warning',
      border: 'border-aurora-status-warning/30',
      glow: 'shadow-glow-yellow',
    },
    critical: {
      bg: 'bg-aurora-status-critical/20',
      text: 'text-aurora-status-critical',
      border: 'border-aurora-status-critical/30',
      glow: 'shadow-glow-red',
    },
    offline: {
      bg: 'bg-aurora-status-offline/20',
      text: 'text-aurora-status-offline',
      border: 'border-aurora-status-offline/30',
      glow: '',
    },
    ok: {
      bg: 'bg-aurora-status-healthy/20',
      text: 'text-aurora-status-healthy',
      border: 'border-aurora-status-healthy/30',
      glow: 'shadow-glow-green',
    },
  }

  const sizeConfig = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  }

  const config = statusConfig[status?.toLowerCase()] || statusConfig.offline
  const sizeClass = sizeConfig[size]

  const Component = animated ? motion.span : 'span'

  return (
    <Component
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full font-medium border',
        config.bg,
        config.text,
        config.border,
        config.glow,
        sizeClass
      )}
      {...(animated && {
        initial: { scale: 0.9, opacity: 0 },
        animate: { scale: 1, opacity: 1 },
        transition: { duration: 0.2 }
      })}
    >
      <span className={cn('w-1.5 h-1.5 rounded-full', config.text.replace('text-', 'bg-'))} />
      {label || status}
    </Component>
  )
}

export default StatusBadge
