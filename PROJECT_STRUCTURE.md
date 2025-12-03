# 📁 AuroraSync OS - Complete Project Structure

## Overview
This document provides a detailed breakdown of every file and folder in the project.

---

## Root Directory

```
aurorasync-os/
├── backend/                    # Python FastAPI backend
├── frontend/                   # React frontend
├── ml_models/                  # ML models and notebooks
├── data_generators/            # Synthetic data generation
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── docker-compose.yml          # Docker orchestration
├── .env.example                # Environment variables template
├── README.md                   # Project overview
├── MASTER_PLAN.md              # Complete development plan
├── QUICK_START.md              # Quick setup guide
├── DEMO_SCRIPT.md              # Presentation script
└── PROJECT_STRUCTURE.md        # This file
```

---

## Backend Structure (`backend/`)

### Core Application (`app/`)

```
backend/app/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── config.py                   # Configuration management
└── database.py                 # Database connection setup
```

**main.py** - Key responsibilities:
- Initialize FastAPI app
- Configure CORS
- Register API routes
- Set up WebSocket endpoints
- Start background tasks (agent orchestration)
- Health check endpoint

**config.py** - Environment variables:
- DATABASE_URL
- REDIS_URL
- OPENAI_API_KEY (optional)
- TTS_API_KEY
- LOG_LEVEL

**database.py** - Database setup:
- SQLAlchemy engine
- Session management
- Connection pooling

### Agents (`app/agents/`)

```
backend/app/agents/
├── __init__.py
├── base_agent.py               # Abstract base class for all agents
├── master_agent.py             # Orchestrator agent
├── data_analysis_agent.py      # Feature extraction & preprocessing
├── diagnosis_agent.py          # ML-based failure prediction
├── customer_engagement_agent.py # Voice AI & customer interaction
├── scheduling_agent.py         # Workshop booking optimization
├── feedback_agent.py           # Post-service validation
├── manufacturing_insights_agent.py # RCA/CAPA generation
└── ueba_agent.py               # Security monitoring
```

**base_agent.py** - Base class features:
- Redis pub/sub connection
- Task processing loop
- Error handling
- Logging for UEBA
- Status reporting

**master_agent.py** - Orchestration logic:
- Task routing
- Agent health monitoring
- Priority queue management
- Workflow coordination

**data_analysis_agent.py** - Data processing:
- Feature engineering (30 features)
- Statistical analysis
- Anomaly detection (Isolation Forest)
- Data validation

**diagnosis_agent.py** - Prediction:
- Load trained ML models
- Feature transformation
- Failure probability calculation
- Component identification
- Severity classification

**customer_engagement_agent.py** - Customer interaction:
- LLM-based script generation
- TTS integration (ElevenLabs/Coqui)
- Sentiment analysis
- Response handling

**scheduling_agent.py** - Booking:
- Workshop availability query
- Constraint satisfaction
- Demand forecasting integration
- Booking confirmation

**feedback_agent.py** - Validation:
- Prediction vs. actual comparison
- Accuracy metrics calculation
- False positive/negative tracking
- Model retraining triggers

**manufacturing_insights_agent.py** - RCA/CAPA:
- Failure pattern clustering
- Root cause analysis
- CAPA report generation
- OEM alert system

**ueba_agent.py** - Security:
- Baseline establishment
- Anomaly detection
- Alert generation
- Auto-mitigation

### Machine Learning (`app/ml/`)

```
backend/app/ml/
├── __init__.py
├── failure_predictor.py        # Random Forest + XGBoost ensemble
├── anomaly_detector.py         # Isolation Forest
├── demand_forecaster.py        # Prophet time-series model
└── model_trainer.py            # Training pipeline
```

**failure_predictor.py**:
- Model loading
- Prediction interface
- Feature importance
- Confidence scoring

**anomaly_detector.py**:
- Isolation Forest implementation
- Anomaly scoring
- Threshold management

**demand_forecaster.py**:
- Prophet model wrapper
- Seasonality handling
- Forecast generation

**model_trainer.py**:
- Data loading
- Feature engineering
- Model training
- Hyperparameter tuning
- Model evaluation
- Model persistence

### Data Layer (`app/data/`)

```
backend/app/data/
├── __init__.py
├── synthetic_generator.py      # Generate vehicle data
├── telematics_stream.py        # Mock MQTT stream
└── schemas.py                  # Pydantic models
```

**synthetic_generator.py**:
- Vehicle fleet generation
- Historical data creation
- Failure scenario injection
- Normal operation patterns

**telematics_stream.py**:
- Real-time data simulation
- MQTT mock implementation
- Data streaming to Redis

**schemas.py** - Pydantic models:
- VehicleCreate, VehicleResponse
- TelemetryData
- PredictionResponse
- BookingCreate, BookingResponse
- UEBAEvent

### Services (`app/services/`)

```
backend/app/services/
├── __init__.py
├── voice_service.py            # TTS integration
├── workshop_api.py             # Mock workshop API
├── manufacturing_api.py        # Mock manufacturing API
└── websocket_manager.py        # WebSocket connections
```

**voice_service.py**:
- TTS API integration
- Audio file generation
- Voice personality configuration

**workshop_api.py**:
- Mock workshop database
- Availability checking
- Booking management

**manufacturing_api.py**:
- RCA/CAPA submission
- Alert handling

**websocket_manager.py**:
- Connection management
- Broadcast to clients
- Room-based messaging

### API Routes (`app/api/routes/`)

```
backend/app/api/routes/
├── __init__.py
├── vehicles.py                 # Vehicle CRUD
├── predictions.py              # Prediction endpoints
├── agents.py                   # Agent status & control
├── scheduling.py               # Booking endpoints
└── analytics.py                # Analytics & reports
```

Each route file contains:
- GET, POST, PUT, DELETE endpoints
- Request validation
- Response serialization
- Error handling

### Database Models (`app/models/`)

```
backend/app/models/
├── __init__.py
├── vehicle.py                  # Vehicle table
├── prediction.py               # Prediction table
├── maintenance.py              # Maintenance records
├── customer.py                 # Customer table
└── ueba_event.py               # UEBA events table
```

Each model file contains:
- SQLAlchemy ORM model
- Table schema
- Relationships
- Indexes

### Utilities (`app/utils/`)

```
backend/app/utils/
├── __init__.py
├── logger.py                   # Logging configuration
└── helpers.py                  # Helper functions
```

### Tests (`tests/`)

```
backend/tests/
├── __init__.py
├── test_agents.py              # Agent unit tests
├── test_ml.py                  # ML model tests
├── test_api.py                 # API endpoint tests
└── test_integration.py         # End-to-end tests
```

### Configuration Files

```
backend/
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image
├── .env.example                # Environment template
└── pytest.ini                  # Test configuration
```

---

## Frontend Structure (`frontend/`)

### Source Code (`src/`)

```
frontend/src/
├── components/                 # React components
├── hooks/                      # Custom React hooks
├── services/                   # API clients
├── styles/                     # CSS files
├── App.jsx                     # Main app component
└── main.jsx                    # Entry point
```

### Components (`src/components/`)

```
frontend/src/components/
├── Dashboard.jsx               # Main dashboard layout
├── VehicleGrid.jsx             # Vehicle card grid
├── VehicleCard.jsx             # Individual vehicle card
├── TelemetryChart.jsx          # Real-time line charts
├── PredictionPanel.jsx         # ML prediction display
├── AgentStatus.jsx             # Agent health indicators
├── SchedulingView.jsx          # Calendar & bookings
├── ManufacturingInsights.jsx   # RCA/CAPA reports
├── UEBAMonitor.jsx             # Security dashboard
├── VoiceCallSimulator.jsx      # TTS demo
├── Navbar.jsx                  # Top navigation
└── Sidebar.jsx                 # Side navigation
```

**Dashboard.jsx** - Main layout:
- Grid layout
- Real-time updates via WebSocket
- State management with Zustand

**VehicleGrid.jsx** - Vehicle overview:
- 3x4 grid of vehicle cards
- Color-coded status
- Click to drill down

**TelemetryChart.jsx** - Charts:
- Recharts library
- Real-time data updates
- Multiple metrics (RPM, temp, vibration)
- 30-second sliding window

**PredictionPanel.jsx** - Predictions:
- Failure probability gauge
- Component identification
- Confidence score
- Recommended action

**AgentStatus.jsx** - Agent monitoring:
- Status indicators (green/yellow/red)
- Performance metrics
- Task queue visualization

**SchedulingView.jsx** - Bookings:
- Calendar component
- Workshop capacity heatmap
- Drag-and-drop rescheduling

**ManufacturingInsights.jsx** - RCA/CAPA:
- Report list
- Failure clustering chart
- Component heatmap

**UEBAMonitor.jsx** - Security:
- Event stream
- Anomaly timeline
- Alert severity distribution
- "Simulate Attack" button

**VoiceCallSimulator.jsx** - Voice demo:
- Audio player
- Transcript display
- Customer response buttons

### Hooks (`src/hooks/`)

```
frontend/src/hooks/
├── useWebSocket.js             # WebSocket connection
└── useAgents.js                # Agent state management
```

**useWebSocket.js**:
- Establish WebSocket connection
- Handle reconnection
- Subscribe to channels
- Parse messages

**useAgents.js**:
- Fetch agent status
- Update agent state
- Trigger agent actions

### Services (`src/services/`)

```
frontend/src/services/
└── api.js                      # Axios HTTP client
```

**api.js**:
- Axios instance configuration
- Base URL setup
- Request interceptors
- Response interceptors
- Error handling

### Styles (`src/styles/`)

```
frontend/src/styles/
└── darkmode.css                # Dark mode theme
```

**darkmode.css**:
- CSS variables for colors
- Dark mode overrides
- Glassmorphism effects
- Animations

### Configuration Files

```
frontend/
├── package.json                # Dependencies
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # TailwindCSS config
├── postcss.config.js           # PostCSS config
└── index.html                  # HTML template
```

---

## ML Models (`ml_models/`)

```
ml_models/
├── trained/                    # Saved models
│   ├── failure_predictor.pkl
│   ├── anomaly_detector.pkl
│   └── demand_forecaster.pkl
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_failure_prediction.ipynb
│   ├── 03_anomaly_detection.ipynb
│   └── 04_demand_forecasting.ipynb
│
└── datasets/                   # Training data
    ├── synthetic_vehicles.csv
    ├── telematics_logs.csv
    └── rca_capa_data.csv
```

---

## Data Generators (`data_generators/`)

```
data_generators/
├── generate_vehicles.py        # Create 10 vehicles
├── generate_telematics.py      # Historical telemetry
├── generate_failures.py        # Failure scenarios
└── generate_ueba_events.py     # UEBA baseline data
```

---

## Scripts (`scripts/`)

```
scripts/
├── setup_db.py                 # Initialize database
├── train_models.py             # Train ML models
├── seed_data.py                # Load synthetic data
└── run_demo.py                 # Start demo mode
```

**setup_db.py**:
- Create tables
- Set up indexes
- Initialize Redis

**train_models.py**:
- Load training data
- Train all models
- Save to ml_models/trained/

**seed_data.py**:
- Generate 10 vehicles
- Create 6 months of history
- Inject failure patterns

**run_demo.py**:
- Start telematics stream
- Trigger failure for VEH003
- Simulate customer interaction
- Auto-schedule booking

---

## Documentation (`docs/`)

```
docs/
├── ARCHITECTURE.md             # System architecture
├── API_REFERENCE.md            # API documentation
├── AGENT_DESIGN.md             # Agent specifications
└── DEPLOYMENT.md               # Deployment guide
```

---

## Docker Configuration

```
docker-compose.yml              # Multi-container setup
backend/Dockerfile              # Backend image
frontend/Dockerfile             # Frontend image
```

---

## File Count Summary

- **Backend**: ~50 files
- **Frontend**: ~30 files
- **ML Models**: ~10 files
- **Scripts**: ~10 files
- **Documentation**: ~10 files
- **Total**: ~110 files

---

## Key Technologies by Layer

### Backend
- FastAPI (API framework)
- SQLAlchemy (ORM)
- Redis (Message bus)
- PostgreSQL (Database)
- scikit-learn (ML)
- LangChain (Agents)

### Frontend
- React 18 (UI framework)
- Vite (Build tool)
- TailwindCSS (Styling)
- Recharts (Charts)
- Axios (HTTP client)
- Zustand (State management)

### ML
- scikit-learn (Random Forest, Isolation Forest)
- XGBoost (Gradient boosting)
- Prophet (Time-series)
- pandas (Data manipulation)
- numpy (Numerical computing)

### Infrastructure
- Docker (Containerization)
- PostgreSQL (Database)
- Redis (Cache & message bus)

---

## Development Workflow

1. **Backend Development**:
   - Start with `backend/app/main.py`
   - Implement agents in `backend/app/agents/`
   - Add API routes in `backend/app/api/routes/`
   - Test with `pytest`

2. **Frontend Development**:
   - Start with `frontend/src/App.jsx`
   - Build components in `frontend/src/components/`
   - Connect to API via `frontend/src/services/api.js`
   - Test in browser

3. **ML Development**:
   - Explore data in `ml_models/notebooks/`
   - Train models with `scripts/train_models.py`
   - Integrate in `backend/app/ml/`

4. **Integration**:
   - Use `docker-compose up` to start all services
   - Run `scripts/run_demo.py` for end-to-end test
   - Verify in browser at http://localhost:3000

---

## Next Steps

1. Create folder structure: `mkdir -p backend/app/agents frontend/src/components ml_models/trained`
2. Start with backend: Implement `main.py` and `base_agent.py`
3. Generate data: Run `python data_generators/generate_vehicles.py`
4. Train models: Run `python scripts/train_models.py`
5. Build frontend: Create `Dashboard.jsx` and `VehicleGrid.jsx`
6. Integrate: Connect frontend to backend via WebSocket
7. Test: Run demo mode and verify all features work

**This structure is designed for rapid development and easy navigation. Good luck! 🚀**
