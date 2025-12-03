import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1a1f2e',
            color: '#e8eaf0',
            border: '1px solid #3b82f6',
          },
          success: {
            iconTheme: {
              primary: '#10b981',
              secondary: '#1a1f2e',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#1a1f2e',
            },
          },
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
)
