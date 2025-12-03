import { format, formatDistanceToNow } from 'date-fns'

export const formatDate = (date) => {
  if (!date) return 'N/A'
  return format(new Date(date), 'MMM dd, yyyy HH:mm')
}

export const formatRelativeTime = (date) => {
  if (!date) return 'N/A'
  return formatDistanceToNow(new Date(date), { addSuffix: true })
}

export const formatNumber = (num, decimals = 2) => {
  if (num === null || num === undefined) return 'N/A'
  return Number(num).toFixed(decimals)
}

export const formatPercentage = (value, decimals = 1) => {
  if (value === null || value === undefined) return 'N/A'
  return `${(value * 100).toFixed(decimals)}%`
}

export const formatRiskLevel = (level) => {
  const levels = {
    low: { label: 'Low Risk', color: 'text-aurora-status-healthy' },
    medium: { label: 'Medium Risk', color: 'text-aurora-status-warning' },
    high: { label: 'High Risk', color: 'text-aurora-status-critical' },
  }
  return levels[level?.toLowerCase()] || { label: level, color: 'text-aurora-text-secondary' }
}

export const formatComponent = (component) => {
  const components = {
    brake_system: 'Brake System',
    engine: 'Engine',
    battery: 'Battery',
    transmission: 'Transmission',
    suspension: 'Suspension',
    electrical: 'Electrical System',
  }
  return components[component] || component
}

export const getRiskColor = (probability) => {
  if (probability >= 0.7) return 'text-aurora-status-critical'
  if (probability >= 0.4) return 'text-aurora-status-warning'
  return 'text-aurora-status-healthy'
}

export const getStatusColor = (status) => {
  const colors = {
    healthy: 'text-aurora-status-healthy',
    warning: 'text-aurora-status-warning',
    critical: 'text-aurora-status-critical',
    offline: 'text-aurora-status-offline',
    ok: 'text-aurora-status-healthy',
    error: 'text-aurora-status-critical',
  }
  return colors[status?.toLowerCase()] || 'text-aurora-text-secondary'
}
