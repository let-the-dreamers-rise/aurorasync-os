# 🚀 AuroraSync OS - Frontend

**The Self-Healing Vehicle Brain** - Production-grade React frontend for AI-powered predictive maintenance system.

## 🎨 Tech Stack

- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS with custom dark theme
- **UI Components**: Radix UI (headless) + custom components
- **Charts**: Recharts
- **Animations**: Framer Motion
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Routing**: React Router v6
- **Notifications**: React Hot Toast

## 🎯 Features

### ✅ Fully Implemented Pages

1. **Dashboard** - System overview with agent status and recent activity
2. **Predictions** - ML failure prediction with interactive form
3. **Scheduling** - Intelligent workshop scheduling with AI reasoning
4. **Voice AI** - Voice conversation simulator with TTS integration
5. **Workshops** - Workshop management with demand forecasting
6. **System Health** - Agent monitoring and UEBA security analytics

### 🎨 Design System

**Color Palette** (Futuristic Automotive Dark Theme):
- Background: Deep blacks (#0a0e1a, #111827, #1a1f2e)
- Accents: Cyan (#06b6d4), Blue (#3b82f6), Purple (#8b5cf6)
- Status: Green (healthy), Yellow (warning), Red (critical)
- Glassmorphism effects with backdrop blur

**Components**:
- StatusBadge - Animated status indicators
- Card - Glassmorphic cards with glow effects
- Button - Multiple variants with loading states
- LoadingSpinner - Smooth animated spinner

### 🔌 API Integration

All backend endpoints are integrated:
- `/api/v1/health` - Health check
- `/api/v1/predict/test` - ML predictions
- `/api/v1/scheduling/auto` - Auto scheduling
- `/api/v1/voice/engage` - Voice conversations
- `/api/v1/agents/status` - Agent monitoring
- `/api/v1/scheduling/workshops` - Workshop data

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

## 🚀 Development

```bash
# Start dev server (with HMR)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🌐 Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=AuroraSync OS
VITE_APP_VERSION=1.0.0
```

## 📁 Project Structure

```
src/
├── api/                    # API client layer
│   ├── axios.js           # Axios instance
│   ├── vehicles.js        # Vehicle endpoints
│   ├── predictions.js     # Prediction endpoints
│   ├── scheduling.js      # Scheduling endpoints
│   ├── voice.js           # Voice endpoints
│   ├── agents.js          # Agent endpoints
│   └── core.js            # Core endpoints
│
├── components/
│   ├── layout/            # Layout components
│   │   ├── MainLayout.jsx
│   │   ├── Sidebar.jsx
│   │   └── TopBar.jsx
│   │
│   └── ui/                # Reusable UI components
│       ├── Card.jsx
│       ├── Button.jsx
│       ├── StatusBadge.jsx
│       └── LoadingSpinner.jsx
│
├── pages/                 # Page components
│   ├── Dashboard.jsx
│   ├── Predictions.jsx
│   ├── Scheduling.jsx
│   ├── VoiceAI.jsx
│   ├── Workshops.jsx
│   └── SystemHealth.jsx
│
├── store/                 # State management
│   └── useStore.js        # Zustand store
│
├── styles/                # Global styles
│   └── index.css          # Tailwind + custom CSS
│
├── utils/                 # Utility functions
│   ├── cn.js              # Class name merger
│   └── formatters.js      # Data formatters
│
├── App.jsx                # Main app component
└── main.jsx               # Entry point
```

## 🎯 Key Features

### 1. Dashboard
- Real-time agent status monitoring
- System health overview
- Recent activity feed
- Workshop analytics

### 2. ML Predictions
- Interactive telematics input form
- Real-time failure probability calculation
- Risk level visualization
- Animated probability bars
- Recommendation engine

### 3. Intelligent Scheduling
- Auto-scheduling with AI reasoning
- Workshop selection logic
- Slot optimization
- Escalation handling
- Load balancing visualization

### 4. Voice AI
- Multi-turn conversation simulator
- TTS audio playback
- Quick response buttons
- Conversation history
- Multiple scenario support

### 5. Workshops
- Workshop grid with load indicators
- Demand forecasting charts
- Capacity management
- Specialty tracking
- Interactive selection

### 6. System Health
- Agent uptime monitoring
- UEBA security analytics
- System information display
- Real-time status updates

## 🎨 Design Highlights

### Animations
- Page transitions with Framer Motion
- Card hover effects with glow
- Loading states with smooth spinners
- Micro-interactions on buttons
- Animated status badges

### Responsive Design
- Mobile-first approach
- Collapsible sidebar
- Adaptive grid layouts
- Touch-friendly interactions

### Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus indicators
- Screen reader support

## 🔧 Customization

### Theme Colors
Edit `tailwind.config.js`:

```js
colors: {
  aurora: {
    accent: {
      cyan: '#06b6d4',
      blue: '#3b82f6',
      // Add your colors
    }
  }
}
```

### API Base URL
Edit `.env`:

```env
VITE_API_URL=https://your-api-url.com
```

## 📊 Performance

- **Bundle Size**: Optimized with Vite
- **Code Splitting**: Route-based lazy loading
- **Tree Shaking**: Unused code elimination
- **Image Optimization**: SVG icons (Lucide)
- **CSS**: Tailwind JIT compilation

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output in `dist/` folder.

### Deploy to Vercel

```bash
vercel deploy
```

### Deploy to Netlify

```bash
netlify deploy --prod
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in vite.config.js
server: {
  port: 3001
}
```

### API Connection Issues
- Check backend is running on port 8000
- Verify CORS settings in backend
- Check `.env` file configuration

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📝 License

MIT License - See LICENSE file for details

## 👥 Team

Built for **National Hackathon 2025** by the AuroraSync OS team.

---

**Made with ❤️ using React + Vite + TailwindCSS**
