import axios from './axios'

export const insightsApi = {
  // Get RCA insights
  getRCAInsights: async (params = {}) => {
    const response = await axios.get('/api/v1/insights/rca', { params })
    return response.data
  },

  // Get CAPA recommendations
  getCAPARecommendations: async (componentId) => {
    const response = await axios.get(`/api/v1/insights/capa/${componentId}`)
    return response.data
  },

  // Get manufacturing insights
  getManufacturingInsights: async () => {
    const response = await axios.get('/api/v1/insights/manufacturing')
    return response.data
  },

  // Get failure trends
  getFailureTrends: async (params = {}) => {
    const response = await axios.get('/api/v1/insights/trends', { params })
    return response.data
  },
}
