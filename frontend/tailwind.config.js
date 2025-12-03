/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // AuroraSync OS Custom Theme - Futuristic Automotive
        aurora: {
          bg: {
            primary: '#0a0e1a',
            secondary: '#111827',
            tertiary: '#1a1f2e',
            card: '#151b2b',
            hover: '#1e2538',
          },
          text: {
            primary: '#e8eaf0',
            secondary: '#9ca3af',
            muted: '#6b7280',
          },
          accent: {
            cyan: '#06b6d4',
            blue: '#3b82f6',
            purple: '#8b5cf6',
            pink: '#ec4899',
            green: '#10b981',
            yellow: '#f59e0b',
            red: '#ef4444',
          },
          status: {
            healthy: '#10b981',
            warning: '#f59e0b',
            critical: '#ef4444',
            offline: '#6b7280',
          },
          glow: {
            cyan: 'rgba(6, 182, 212, 0.3)',
            blue: 'rgba(59, 130, 246, 0.3)',
            purple: 'rgba(139, 92, 246, 0.3)',
            green: 'rgba(16, 185, 129, 0.3)',
            red: 'rgba(239, 68, 68, 0.3)',
          }
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'glow-cyan': '0 0 20px rgba(6, 182, 212, 0.3)',
        'glow-blue': '0 0 20px rgba(59, 130, 246, 0.3)',
        'glow-purple': '0 0 20px rgba(139, 92, 246, 0.3)',
        'glow-green': '0 0 20px rgba(16, 185, 129, 0.3)',
        'glow-red': '0 0 20px rgba(239, 68, 68, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(6, 182, 212, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(6, 182, 212, 0.6)' },
        },
      },
    },
  },
  plugins: [],
}
