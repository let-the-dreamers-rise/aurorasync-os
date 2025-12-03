import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, Info, CheckCircle, XCircle, X } from 'lucide-react'
import { cn } from '@/utils/cn'

const AlertBanner = ({ type = 'info', message, onClose, className }) => {
  const icons = {
    info: Info,
    success: CheckCircle,
    warning: AlertTriangle,
    error: XCircle,
  }

  const colors = {
    info: 'bg-aurora-accent-blue/20 border-aurora-accent-blue/30 text-aurora-accent-cyan',
    success: 'bg-aurora-status-healthy/20 border-aurora-status-healthy/30 text-aurora-status-healthy',
    warning: 'bg-aurora-status-warning/20 border-aurora-status-warning/30 text-aurora-status-warning',
    error: 'bg-aurora-status-critical/20 border-aurora-status-critical/30 text-aurora-status-critical',
  }

  const Icon = icons[type]

  return (
    <AnimatePresence>
      <motion.div
        className={cn(
          'flex items-center gap-3 p-4 rounded-lg border',
          colors[type],
          className
        )}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.3 }}
      >
        <Icon className="w-5 h-5 flex-shrink-0" />
        <p className="flex-1 text-sm font-medium">{message}</p>
        {onClose && (
          <button
            onClick={onClose}
            className="p-1 hover:bg-aurora-bg-hover rounded transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </motion.div>
    </AnimatePresence>
  )
}

export default AlertBanner
