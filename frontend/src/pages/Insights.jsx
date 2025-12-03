import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, AlertCircle, Wrench, BarChart3, Package } from 'lucide-react'
import { insightsApi } from '@/api/insights'
import Card from '@/components/ui/Card'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import AlertBanner from '@/components/AlertBanner'
import ForecastGraph from '@/components/ForecastGraph'
import DataTable from '@/components/DataTable'
import { cn } from '@/utils/cn'

const Insights = () => {
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInsights()
  }, [])

  const loadInsights = async () => {
    try {
      setLoading(true)
      
      // Use mock data immediately for reliable demo
      setInsights(generateMockInsights())
      
      // Try to fetch real data in background (optional)
      insightsApi.getRCAInsights()
        .then(data => setInsights(data))
        .catch(() => {}) // Silent fallback to mock data
      
    } catch (err) {
      // Fallback to mock data
      setInsights(generateMockInsights())
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  const topComponents = insights?.top_components || []
  const recommendations = insights?.recommendations || []
  const failureTrends = insights?.failure_trends || []

  const componentColumns = [
    {
      key: 'component',
      label: 'Component',
      sortable: true,
      render: (value) => (
        <div className="flex items-center gap-2">
          <Package className="w-4 h-4 text-aurora-accent-cyan" />
          <span className="font-medium">{value}</span>
        </div>
      )
    },
    {
      key: 'failure_count',
      label: 'Failures',
      sortable: true,
      render: (value) => (
        <span className="font-mono text-aurora-status-critical">{value}</span>
      )
    },
    {
      key: 'recurrence_rate',
      label: 'Recurrence Rate',
      sortable: true,
      render: (value) => (
        <span className="font-medium text-aurora-status-warning">
          {(value * 100).toFixed(1)}%
        </span>
      )
    },
    {
      key: 'avg_days_to_failure',
      label: 'Avg Days to Failure',
      sortable: true,
      render: (value) => `${value} days`
    },
    {
      key: 'severity',
      label: 'Severity',
      sortable: true,
      render: (value) => (
        <span className={cn(
          'px-2 py-1 rounded-full text-xs font-medium',
          value === 'critical' && 'bg-aurora-status-critical/20 text-aurora-status-critical',
          value === 'high' && 'bg-aurora-status-warning/20 text-aurora-status-warning',
          value === 'medium' && 'bg-aurora-accent-blue/20 text-aurora-accent-cyan'
        )}>
          {value.toUpperCase()}
        </span>
      )
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold gradient-text mb-2">RCA & CAPA Insights</h1>
        <p className="text-aurora-text-muted">
          Root Cause Analysis and Corrective/Preventive Action recommendations
        </p>
      </div>



      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="hover:border-aurora-accent-cyan/50 transition-all">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-aurora-status-critical/20 flex items-center justify-center">
              <AlertCircle className="w-5 h-5 text-aurora-status-critical" />
            </div>
            <div>
              <p className="text-xs text-aurora-text-muted">Total Failures</p>
              <p className="text-2xl font-bold text-aurora-text-primary">
                {insights?.total_failures || 0}
              </p>
            </div>
          </div>
        </Card>

        <Card className="hover:border-aurora-accent-cyan/50 transition-all">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-aurora-accent-blue/20 flex items-center justify-center">
              <Package className="w-5 h-5 text-aurora-accent-cyan" />
            </div>
            <div>
              <p className="text-xs text-aurora-text-muted">Components Affected</p>
              <p className="text-2xl font-bold text-aurora-text-primary">
                {topComponents.length}
              </p>
            </div>
          </div>
        </Card>

        <Card className="hover:border-aurora-accent-cyan/50 transition-all">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-aurora-status-warning/20 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-aurora-status-warning" />
            </div>
            <div>
              <p className="text-xs text-aurora-text-muted">Avg Recurrence</p>
              <p className="text-2xl font-bold text-aurora-text-primary">
                {insights?.avg_recurrence_rate 
                  ? `${(insights.avg_recurrence_rate * 100).toFixed(1)}%`
                  : 'N/A'}
              </p>
            </div>
          </div>
        </Card>

        <Card className="hover:border-aurora-accent-cyan/50 transition-all">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-aurora-accent-purple/20 flex items-center justify-center">
              <Wrench className="w-5 h-5 text-aurora-accent-purple" />
            </div>
            <div>
              <p className="text-xs text-aurora-text-muted">Recommendations</p>
              <p className="text-2xl font-bold text-aurora-text-primary">
                {recommendations.length}
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Failure Trends Chart */}
      {failureTrends.length > 0 && (
        <ForecastGraph
          data={failureTrends}
          title="Failure Trends Over Time"
          type="bar"
        />
      )}

      {/* Top Recurring Components */}
      <div>
        <h2 className="text-xl font-semibold text-aurora-text-primary mb-4">
          Top Recurring Components
        </h2>
        <DataTable
          columns={componentColumns}
          data={topComponents}
        />
      </div>

      {/* Manufacturing Recommendations */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <Wrench className="w-5 h-5 text-aurora-accent-cyan" />
          <h2 className="text-xl font-semibold text-aurora-text-primary">
            Manufacturing Action Items
          </h2>
        </div>
        <div className="space-y-4">
          {recommendations.map((rec, idx) => (
            <motion.div
              key={idx}
              className="p-4 bg-aurora-bg-tertiary rounded-lg border border-aurora-bg-tertiary hover:border-aurora-accent-blue/30 transition-all"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-3">
                  <div className={cn(
                    'w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold',
                    rec.priority === 'critical' && 'bg-aurora-status-critical/20 text-aurora-status-critical',
                    rec.priority === 'high' && 'bg-aurora-status-warning/20 text-aurora-status-warning',
                    rec.priority === 'medium' && 'bg-aurora-accent-blue/20 text-aurora-accent-cyan'
                  )}>
                    {idx + 1}
                  </div>
                  <div>
                    <h3 className="font-semibold text-aurora-text-primary">
                      {rec.component}
                    </h3>
                    <p className="text-sm text-aurora-text-muted">
                      {rec.issue_type}
                    </p>
                  </div>
                </div>
                <span className={cn(
                  'px-3 py-1 rounded-full text-xs font-medium',
                  rec.priority === 'critical' && 'bg-aurora-status-critical/20 text-aurora-status-critical',
                  rec.priority === 'high' && 'bg-aurora-status-warning/20 text-aurora-status-warning',
                  rec.priority === 'medium' && 'bg-aurora-accent-blue/20 text-aurora-accent-cyan'
                )}>
                  {rec.priority.toUpperCase()}
                </span>
              </div>
              <div className="ml-11 space-y-2">
                <div>
                  <p className="text-xs text-aurora-accent-cyan font-medium mb-1">
                    Root Cause:
                  </p>
                  <p className="text-sm text-aurora-text-secondary">
                    {rec.root_cause}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-aurora-accent-cyan font-medium mb-1">
                    Recommended Action:
                  </p>
                  <p className="text-sm text-aurora-text-secondary">
                    {rec.action}
                  </p>
                </div>
                <div className="flex items-center gap-4 text-xs text-aurora-text-muted">
                  <span>Impact: {rec.estimated_impact}</span>
                  <span>•</span>
                  <span>Timeline: {rec.timeline}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </Card>
    </div>
  )
}

// Mock data generator
const generateMockInsights = () => {
  return {
    total_failures: 247,
    avg_recurrence_rate: 0.34,
    top_components: [
      {
        component: 'Brake Pads',
        failure_count: 45,
        recurrence_rate: 0.67,
        avg_days_to_failure: 180,
        severity: 'critical',
      },
      {
        component: 'Battery',
        failure_count: 38,
        recurrence_rate: 0.52,
        avg_days_to_failure: 365,
        severity: 'high',
      },
      {
        component: 'Alternator',
        failure_count: 32,
        recurrence_rate: 0.45,
        avg_days_to_failure: 450,
        severity: 'high',
      },
      {
        component: 'Suspension',
        failure_count: 28,
        recurrence_rate: 0.38,
        avg_days_to_failure: 300,
        severity: 'medium',
      },
      {
        component: 'Transmission',
        failure_count: 24,
        recurrence_rate: 0.29,
        avg_days_to_failure: 540,
        severity: 'critical',
      },
    ],
    failure_trends: [
      { date: 'Jan', value: 18 },
      { date: 'Feb', value: 22 },
      { date: 'Mar', value: 25 },
      { date: 'Apr', value: 20 },
      { date: 'May', value: 28 },
      { date: 'Jun', value: 32 },
    ],
    recommendations: [
      {
        component: 'Brake Pads',
        priority: 'critical',
        issue_type: 'Material Quality',
        root_cause: 'Substandard friction material causing premature wear',
        action: 'Switch to ceramic composite brake pads with higher heat tolerance',
        estimated_impact: 'Reduce failures by 60%',
        timeline: '2-3 months',
      },
      {
        component: 'Battery',
        priority: 'high',
        issue_type: 'Design Flaw',
        root_cause: 'Inadequate thermal management in high-temperature environments',
        action: 'Implement improved cooling system and upgrade to AGM batteries',
        estimated_impact: 'Reduce failures by 45%',
        timeline: '3-4 months',
      },
      {
        component: 'Alternator',
        priority: 'high',
        issue_type: 'Manufacturing Defect',
        root_cause: 'Bearing quality inconsistency from supplier',
        action: 'Audit supplier quality control and implement stricter acceptance criteria',
        estimated_impact: 'Reduce failures by 50%',
        timeline: '1-2 months',
      },
    ],
  }
}

export default Insights
