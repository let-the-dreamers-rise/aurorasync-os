import axios from './axios'

export const agentsApi = {
  // Test agent routing
  testRoute: async (eventData) => {
    const response = await axios.post('/api/v1/agents/test-route', eventData)
    return response.data
  },

  // Get agent status
  getStatus: async () => {
    const response = await axios.get('/api/v1/agents/status')
    return response.data
  },

  // Get UEBA statistics
  getUEBAStats: async () => {
    const response = await axios.get('/api/v1/agents/ueba/stats')
    return response.data
  },

  // Get available event types
  getEventTypes: async () => {
    const response = await axios.get('/api/v1/agents/event-types')
    return response.data
  },
}
