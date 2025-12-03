import axios from './axios'

export const schedulingApi = {
  // Auto schedule appointment
  autoSchedule: async (scheduleData) => {
    const response = await axios.post('/api/v1/scheduling/auto', scheduleData)
    return response.data
  },

  // Get all workshops
  getWorkshops: async () => {
    const response = await axios.get('/api/v1/scheduling/workshops')
    return response.data
  },

  // Get workshop by ID
  getWorkshop: async (workshopId) => {
    const response = await axios.get(`/api/v1/scheduling/workshops/${workshopId}`)
    return response.data
  },

  // Get demand forecast
  getDemandForecast: async (workshopId, days = 7) => {
    const response = await axios.get(`/api/v1/scheduling/forecast/${workshopId}`, {
      params: { days }
    })
    return response.data
  },

  // Get available slots
  getAvailableSlots: async (workshopId, days = 7) => {
    const response = await axios.get(`/api/v1/scheduling/slots/${workshopId}`, {
      params: { days }
    })
    return response.data
  },

  // Generate RCA report
  generateRCAReport: async (component = null, days = 30) => {
    const response = await axios.post('/api/v1/scheduling/insights/rca', null, {
      params: { component, days }
    })
    return response.data
  },

  // Get scheduling analytics
  getAnalytics: async () => {
    const response = await axios.get('/api/v1/scheduling/analytics/overview')
    return response.data
  },
}
