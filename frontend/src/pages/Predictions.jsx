import { useState } from 'react'
import { motion } from 'framer-motion'
import { Brain, AlertTriangle, TrendingUp, Info } from 'lucide-react'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import StatusBadge from '@/components/ui/StatusBadge'
import PredictionResultCard from '@/components/PredictionResultCard'
import { predictionsApi } from '@/api/predictions'
import { formatPercentage, formatComponent } from '@/utils/formatters'
import toast from 'react-hot-toast'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const Predictions = () => {
  const [loading, setLoading] = useState(false)
  const [prediction, setPrediction] = useState(null)
  const [formData, setFormData] = useState({
    engine_temp: 95.0,
    brake_pad_wear: 5.0,
    battery_voltage: 12.5,
    vibration: 0.5,
    tyre_pressure: 32.0,
    odometer: 50000,
    ambient_temp: 25.0,
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }))
  }

  const handlePredict = async () => {
    try {
      setLoading(true)
      const result = await predictionsApi.testPrediction(formData)
      setPrediction(result)
      toast.success('Prediction completed successfully')
    } catch (error) {
      console.error('Prediction failed:', error)
      toast.error('Prediction failed. Make sure backend is running on http://localhost:8000')
      
      // Show mock prediction for demo purposes
      const mockProbability = (
        (formData.engine_temp > 100 ? 0.3 : 0) +
        (formData.brake_pad_wear < 5 ? 0.3 : 0) +
        (formData.battery_voltage < 12 ? 0.2 : 0) +
        (formData.vibration > 1 ? 0.2 : 0)
      )
      
      setPrediction({
        status: 'mock',
        input: formData,
        prediction: {
          failure_risk: mockProbability > 0.5 ? 'HIGH' : mockProbability > 0.2 ? 'MEDIUM' : 'LOW',
          probability: mockProbability,
          thresholds: { low: 0.2, medium: 0.5 },
          model_type: 'MockPredictor (Backend Offline)'
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFormData({
      engine_temp: 95.0,
      brake_pad_wear: 5.0,
      battery_voltage: 12.5,
      vibration: 0.5,
      tyre_pressure: 32.0,
      odometer: 50000,
      ambient_temp: 25.0,
    })
    setPrediction(null)
  }

  const getRiskStatus = (risk) => {
    if (risk === 'HIGH') return 'critical'
    if (risk === 'MEDIUM') return 'warning'
    return 'healthy'
  }

  const formFields = [
    { name: 'engine_temp', label: 'Engine Temperature (°C)', min: 0, max: 150, step: 0.1 },
    { name: 'brake_pad_wear', label: 'Brake Pad Wear (mm)', min: 0, max: 15, step: 0.1 },
    { name: 'battery_voltage', label: 'Battery Voltage (V)', min: 10, max: 15, step: 0.1 },
    { name: 'vibration', label: 'Vibration Level (0-2)', min: 0, max: 2, step: 0.1 },
    { name: 'tyre_pressure', label: 'Tyre Pressure (PSI)', min: 15, max: 50, step: 0.5 },
    { name: 'odometer', label: 'Odometer (km)', min: 0, max: 500000, step: 100 },
    { name: 'ambient_temp', label: 'Ambient Temperature (°C)', min: -20, max: 60, step: 0.5 },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold gradient-text mb-2">ML Predictions</h1>
        <p className="text-aurora-text-secondary">
          Test the failure prediction model with custom telematics data
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Brain className="w-5 h-5 text-aurora-accent-blue" />
            Telematics Input
          </h2>

          <div className="space-y-4">
            {formFields.map((field) => (
              <div key={field.name}>
                <label className="block text-sm font-medium mb-2">
                  {field.label}
                </label>
                <input
                  type="number"
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleInputChange}
                  min={field.min}
                  max={field.max}
                  step={field.step}
                  className="input"
                />
              </div>
            ))}
          </div>

          <div className="flex gap-3 mt-6">
            <Button
              variant="primary"
              className="flex-1"
              onClick={handlePredict}
              loading={loading}
              icon={<Brain className="w-4 h-4" />}
            >
              Predict Failure
            </Button>
            <Button
              variant="secondary"
              onClick={handleReset}
            >
              Reset
            </Button>
          </div>
        </Card>

        {/* Prediction Result */}
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-aurora-accent-green" />
            Prediction Result
          </h2>

          {!prediction ? (
            <div className="flex flex-col items-center justify-center h-[400px] text-center">
              <AlertTriangle className="w-16 h-16 text-aurora-text-muted mb-4" />
              <p className="text-aurora-text-muted">
                Enter telematics data and click "Predict Failure" to see results
              </p>
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="space-y-6"
            >
              {/* Risk Level */}
              <div className="text-center p-6 glass rounded-lg">
                <p className="text-sm text-aurora-text-muted mb-2">Failure Risk</p>
                <StatusBadge
                  status={getRiskStatus(prediction.prediction.failure_risk)}
                  label={prediction.prediction.failure_risk}
                  size="lg"
                />
                <p className="text-4xl font-bold mt-4">
                  {formatPercentage(prediction.prediction.probability, 2)}
                </p>
                <p className="text-sm text-aurora-text-muted mt-2">
                  Failure Probability
                </p>
              </div>

              {/* Thresholds */}
              <div className="glass rounded-lg p-4">
                <h3 className="font-medium mb-3 flex items-center gap-2">
                  <Info className="w-4 h-4" />
                  Risk Thresholds
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-aurora-text-muted">Low Risk</span>
                    <span className="text-sm font-medium">
                      &lt; {formatPercentage(prediction.prediction.thresholds.low)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-aurora-text-muted">Medium Risk</span>
                    <span className="text-sm font-medium">
                      {formatPercentage(prediction.prediction.thresholds.low)} - {formatPercentage(prediction.prediction.thresholds.medium)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-aurora-text-muted">High Risk</span>
                    <span className="text-sm font-medium">
                      ≥ {formatPercentage(prediction.prediction.thresholds.medium)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Probability Bar */}
              <div className="glass rounded-lg p-4">
                <h3 className="font-medium mb-3">Probability Distribution</h3>
                <div className="relative h-8 bg-aurora-bg-tertiary rounded-full overflow-hidden">
                  <motion.div
                    className={`absolute left-0 top-0 h-full rounded-full ${
                      prediction.prediction.failure_risk === 'HIGH'
                        ? 'bg-aurora-status-critical'
                        : prediction.prediction.failure_risk === 'MEDIUM'
                        ? 'bg-aurora-status-warning'
                        : 'bg-aurora-status-healthy'
                    }`}
                    initial={{ width: 0 }}
                    animate={{ width: `${prediction.prediction.probability * 100}%` }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-sm font-bold text-white mix-blend-difference">
                      {formatPercentage(prediction.prediction.probability, 1)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Recommendation */}
              <div className={`glass rounded-lg p-4 border-l-4 ${
                prediction.prediction.failure_risk === 'HIGH'
                  ? 'border-aurora-status-critical'
                  : prediction.prediction.failure_risk === 'MEDIUM'
                  ? 'border-aurora-status-warning'
                  : 'border-aurora-status-healthy'
              }`}>
                <h3 className="font-medium mb-2">Recommendation</h3>
                <p className="text-sm text-aurora-text-secondary">
                  {prediction.prediction.failure_risk === 'HIGH'
                    ? 'Immediate service required. Schedule appointment as soon as possible.'
                    : prediction.prediction.failure_risk === 'MEDIUM'
                    ? 'Monitor closely. Consider scheduling preventive maintenance.'
                    : 'Vehicle is in good condition. Continue regular monitoring.'}
                </p>
              </div>
            </motion.div>
          )}
        </Card>
      </div>
    </div>
  )
}

export default Predictions
