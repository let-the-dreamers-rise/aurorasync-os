import { useState } from 'react'
import { motion } from 'framer-motion'
import { Calendar, MapPin, Clock, AlertCircle, CheckCircle } from 'lucide-react'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import StatusBadge from '@/components/ui/StatusBadge'
import SchedulingDecisionCard from '@/components/SchedulingDecisionCard'
import { schedulingApi } from '@/api/scheduling'
import { formatDate } from '@/utils/formatters'
import toast from 'react-hot-toast'

const Scheduling = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [formData, setFormData] = useState({
    vehicle_id: 'VEH001',
    component: 'brake_system',
    risk_level: 'high',
    probability: 0.82,
    vehicle_location: 'Mumbai',
    preferred_time: 'afternoon',
    preferred_day: 'tomorrow',
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSchedule = async () => {
    try {
      setLoading(true)
      const scheduleResult = await schedulingApi.autoSchedule({
        vehicle_id: formData.vehicle_id,
        component: formData.component,
        risk_level: formData.risk_level,
        probability: parseFloat(formData.probability),
        owner_preferences: {
          preferred_time: formData.preferred_time,
          preferred_day: formData.preferred_day,
          preferred_city: formData.vehicle_location
        },
        vehicle_location: formData.vehicle_location
      })
      setResult(scheduleResult)
      toast.success('Appointment scheduled successfully!')
    } catch (error) {
      console.error('Scheduling failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold gradient-text mb-2">Intelligent Scheduling</h1>
        <p className="text-aurora-text-secondary">
          AI-powered workshop scheduling with load balancing and demand forecasting
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Scheduling Form */}
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-aurora-accent-blue" />
            Schedule Service
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Vehicle ID</label>
              <input
                type="text"
                name="vehicle_id"
                value={formData.vehicle_id}
                onChange={handleInputChange}
                className="input"
                placeholder="VEH001"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Component</label>
              <select
                name="component"
                value={formData.component}
                onChange={handleInputChange}
                className="input"
              >
                <option value="brake_system">Brake System</option>
                <option value="engine">Engine</option>
                <option value="battery">Battery</option>
                <option value="transmission">Transmission</option>
                <option value="suspension">Suspension</option>
                <option value="electrical">Electrical System</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Risk Level</label>
              <select
                name="risk_level"
                value={formData.risk_level}
                onChange={handleInputChange}
                className="input"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Failure Probability</label>
              <input
                type="number"
                name="probability"
                value={formData.probability}
                onChange={handleInputChange}
                min="0"
                max="1"
                step="0.01"
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Location</label>
              <input
                type="text"
                name="vehicle_location"
                value={formData.vehicle_location}
                onChange={handleInputChange}
                className="input"
                placeholder="Mumbai"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Preferred Time</label>
              <select
                name="preferred_time"
                value={formData.preferred_time}
                onChange={handleInputChange}
                className="input"
              >
                <option value="morning">Morning</option>
                <option value="afternoon">Afternoon</option>
                <option value="evening">Evening</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Preferred Day</label>
              <select
                name="preferred_day"
                value={formData.preferred_day}
                onChange={handleInputChange}
                className="input"
              >
                <option value="today">Today</option>
                <option value="tomorrow">Tomorrow</option>
                <option value="this_week">This Week</option>
                <option value="next_week">Next Week</option>
              </select>
            </div>
          </div>

          <Button
            variant="primary"
            className="w-full mt-6"
            onClick={handleSchedule}
            loading={loading}
            icon={<Calendar className="w-4 h-4" />}
          >
            Schedule Appointment
          </Button>
        </Card>

        {/* Scheduling Result */}
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-aurora-accent-green" />
            Scheduling Result
          </h2>

          {!result ? (
            <div className="flex flex-col items-center justify-center h-[500px] text-center">
              <Calendar className="w-16 h-16 text-aurora-text-muted mb-4" />
              <p className="text-aurora-text-muted">
                Fill in the form and click "Schedule Appointment" to see results
              </p>
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <SchedulingDecisionCard
                decision={{
                  workshop_id: result.workshop?.id || result.workshop_id,
                  workshop_name: result.workshop?.name || 'Selected Workshop',
                  workshop_location: result.workshop?.city || result.workshop?.location || formData.vehicle_location,
                  slot_date: result.slot?.date || formatDate(new Date()),
                  slot_time: result.slot?.time || formData.preferred_time,
                  confidence_score: result.confidence_score || 0.92,
                  reasoning: result.reasoning?.workshop_selection || result.reasoning?.slot_selection || 'Optimal slot selected based on availability and proximity',
                  estimated_duration: result.slot?.duration_hours ? `${result.slot.duration_hours} hours` : '2-3 hours',
                  priority: formData.risk_level,
                }}
                onConfirm={() => toast.success('Booking confirmed!')}
                onReject={() => {
                  setResult(null)
                  toast('Finding alternative slots...', { icon: 'ℹ️' })
                }}
              />

              {/* Warnings */}
              {result.warnings && result.warnings.length > 0 && (
                <div className="mt-4 glass rounded-lg p-4 border-l-4 border-aurora-status-warning">
                  <h3 className="font-medium mb-2 text-aurora-status-warning">Warnings</h3>
                  <ul className="space-y-1">
                    {result.warnings.map((warning, index) => (
                      <li key={index} className="text-sm text-aurora-text-secondary">
                        • {warning}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </motion.div>
          )}
        </Card>
      </div>
    </div>
  )
}

export default Scheduling
