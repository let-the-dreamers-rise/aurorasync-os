import axios from './axios'

export const coreApi = {
  // Health check
  healthCheck: async () => {
    const response = await axios.get('/api/v1/health', { skipErrorToast: true })
    return response.data
  },

  // System info
  getSystemInfo: async () => {
    const response = await axios.get('/api/v1/info')
    return response.data
  },

  // Database check
  dbCheck: async () => {
    const response = await axios.get('/api/v1/db-check')
    return response.data
  },
}
