import axios from './axios'

export const predictionsApi = {
  // Get mock predictions (no input required - perfect for demos!)
  getMockPredictions: async () => {
    const response = await axios.get('/api/v1/predict/mock')
    return response.data
  },

  // Test prediction
  testPrediction: async (telematicsData) => {
    const response = await axios.post('/api/v1/predict/test', telematicsData)
    return response.data
  },

  // Batch prediction
  batchPrediction: async (telematicsArray) => {
    const response = await axios.post('/api/v1/predict/batch', telematicsArray)
    return response.data
  },

  // Get model info
  getModelInfo: async () => {
    const response = await axios.get('/api/v1/predict/model-info')
    return response.data
  },

  // Get all predictions
  getAll: async () => {
    const response = await axios.get('/api/v1/predictions')
    return response.data
  },

  // Get prediction by ID
  getById: async (id) => {
    const response = await axios.get(`/api/v1/predictions/${id}`)
    return response.data
  },

  // Get predictions for vehicle
  getByVehicle: async (vehicleId) => {
    const response = await axios.get(`/api/v1/vehicles/${vehicleId}/predictions`)
    return response.data
  },
}
