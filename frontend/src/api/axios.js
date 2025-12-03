import axios from 'axios'
import toast from 'react-hot-toast'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Don't show toast for certain errors
    if (error.config?.skipErrorToast) {
      return Promise.reject(error)
    }
    
    // Don't show toast for 404 errors (expected when using mock data)
    if (error.response?.status === 404) {
      return Promise.reject(error)
    }
    
    // Don't show toast for 500 errors (backend issues, we have fallbacks)
    if (error.response?.status === 500) {
      return Promise.reject(error)
    }
    
    // Only show toast for unexpected errors
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    toast.error(message)
    return Promise.reject(error)
  }
)

export default axiosInstance
