import { motion } from 'framer-motion'
import { Calendar, MapPin, Clock, CheckCircle, Sparkles } from 'lucide-react'
import { cn } from '@/utils/cn'
import Card from './ui/Card'
import Button from './ui/Button'
import { formatDate } from '@/utils/formatters'

const SchedulingDecisionCard = ({ decision, onConfirm, onReject, className }) => {
  const {
    workshop_id,
    workshop_name,
    workshop_location,
    slot_date,
    slot_time,
    confidence_score,
    reasoning,
    estimated_duration,
    priority,
  } = decision

  return (
    <Card className={cn('hover:border-aurora-accent-cyan/50 transition-all', className)}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-aurora-accent-cyan to-aurora-accent-blue flex items-center justify-center shadow-glow-cyan">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-aurora-text-primary">AI Recommendation</h3>
            <p className="text-sm text-aurora-accent-cyan">Optimal scheduling found</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-aurora-status-healthy animate-pulse" />
          <span className="text-xs text-aurora-text-muted">
            {(confidence_score * 100).toFixed(0)}% confidence
          </span>
        </div>
      </div>

      {/* Workshop Details */}
      <div className="space-y-3 mb-4">
        <div className="flex items-center gap-3 p-3 bg-aurora-bg-tertiary rounded-lg">
          <MapPin className="w-5 h-5 text-aurora-accent-purple" />
          <div className="flex-1">
            <p className="text-sm font-medium text-aurora-text-primary">{workshop_name}</p>
            <p className="text-xs text-aurora-text-muted">{workshop_location}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="flex items-center gap-2 p-3 bg-aurora-bg-tertiary rounded-lg">
            <Calendar className="w-4 h-4 text-aurora-accent-cyan" />
            <div>
              <p className="text-xs text-aurora-text-muted">Date</p>
              <p className="text-sm font-medium text-aurora-text-primary">
                {formatDate(slot_date)}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 p-3 bg-aurora-bg-tertiary rounded-lg">
            <Clock className="w-4 h-4 text-aurora-accent-cyan" />
            <div>
              <p className="text-xs text-aurora-text-muted">Time</p>
              <p className="text-sm font-medium text-aurora-text-primary">{slot_time}</p>
            </div>
          </div>
        </div>

        {estimated_duration && (
          <div className="flex items-center gap-2 p-2 bg-aurora-accent-blue/10 border border-aurora-accent-blue/30 rounded-lg">
            <Clock className="w-4 h-4 text-aurora-accent-cyan" />
            <span className="text-sm text-aurora-text-secondary">
              Estimated duration: {estimated_duration}
            </span>
          </div>
        )}
      </div>

      {/* Reasoning */}
      {reasoning && (
        <div className="p-3 bg-aurora-bg-secondary rounded-lg mb-4">
          <p className="text-xs text-aurora-accent-cyan font-medium mb-1">Why this slot?</p>
          <p className="text-sm text-aurora-text-secondary">{reasoning}</p>
        </div>
      )}

      {/* Priority Badge */}
      {priority && (
        <div className="flex items-center gap-2 mb-4">
          <span className={cn(
            'px-3 py-1 rounded-full text-xs font-medium',
            priority === 'urgent' && 'bg-aurora-status-critical/20 text-aurora-status-critical',
            priority === 'high' && 'bg-aurora-status-warning/20 text-aurora-status-warning',
            priority === 'normal' && 'bg-aurora-accent-blue/20 text-aurora-accent-cyan'
          )}>
            {priority.toUpperCase()} PRIORITY
          </span>
        </div>
      )}

      {/* Actions */}
      {(onConfirm || onReject) && (
        <div className="flex gap-3">
          {onConfirm && (
            <Button
              onClick={onConfirm}
              className="flex-1 bg-aurora-accent-cyan hover:bg-aurora-accent-cyan/80"
            >
              <CheckCircle className="w-4 h-4 mr-2" />
              Confirm Booking
            </Button>
          )}
          {onReject && (
            <Button
              onClick={onReject}
              variant="outline"
              className="flex-1"
            >
              Find Alternative
            </Button>
          )}
        </div>
      )}
    </Card>
  )
}

export default SchedulingDecisionCard
