import axios from './axios'

export const vehiclesApi = {
  // Get all vehicles
  getAll: async () => {
    const response = await axios.get('/api/v1/vehicles')
    return response.data
  },

  // Get vehicle by ID
  getById: async (id) => {
    const response = await axios.get(`/api/v1/vehicles/${id}`)
    return response.data
  },

  // Get vehicle telematics
  getTelematics: async (id) => {
    const response = await axios.get(`/api/v1/vehicles/${id}/telematics`)
    return response.data
  },

  // Get vehicle history
  getHistory: async (id) => {
    const response = await axios.get(`/api/v1/vehicles/${id}/history`)
    return response.data
  },

  // Simulate failure
  simulateFailure: async (id, data) => {
    const response = await axios.post(`/api/v1/vehicles/${id}/simulate`, data)
    return response.data
  },
}
