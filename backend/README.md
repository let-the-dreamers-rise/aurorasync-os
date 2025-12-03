# AuroraSync OS - Backend

FastAPI backend for the Self-Healing Vehicle Brain predictive maintenance system.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional for now)

### Installation

1. **Create virtual environment**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
# Copy example environment file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env and update DATABASE_URL if needed
```

4. **Start PostgreSQL**

Using Docker:
```bash
docker run -d \
  --name aurorasync-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=aurorasync \
  -p 5432:5432 \
  postgres:15
```

Or use your local PostgreSQL installation.

5. **Create database tables**
```bash
python scripts/setup_db.py
```

6. **Start the API server**
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── core.py      # Core API routes (health, info)
│   │
│   └── models/
│       ├── __init__.py
│       ├── vehicle.py       # Vehicle model
│       ├── prediction.py    # Prediction model
│       └── ueba_event.py    # UEBA event model
│
├── scripts/
│   ├── __init__.py
│   └── setup_db.py          # Database setup script
│
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── README.md               # This file
```

## 🔌 API Endpoints

### Root Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check

### API v1 Endpoints (`/api/v1`)

- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - System information
- `GET /api/v1/db-check` - Database connectivity check

## 🗄️ Database Models

### Vehicle
Stores vehicle information:
- `vehicle_id` - Unique identifier (e.g., VEH001)
- `make`, `model`, `year` - Vehicle details
- `mileage` - Current odometer reading
- `owner_name`, `owner_phone` - Owner information
- `status` - Health status (healthy, warning, critical)

### Prediction
Stores ML predictions:
- `prediction_id` - Unique identifier
- `vehicle_id` - Reference to vehicle
- `component` - Component at risk
- `failure_probability` - Probability (0.0 to 1.0)
- `severity` - Severity level
- `predicted_failure_date` - Estimated failure date

### UEBAEvent
Stores security events:
- `event_id` - Unique identifier
- `agent_name` - Agent being monitored
- `metric` - Metric monitored
- `anomaly_score` - Anomaly score (0.0 to 1.0)
- `severity` - Event severity

## 🧪 Testing

### Manual Testing

1. **Check API is running**
```bash
curl http://localhost:8000/health
```

2. **Check system info**
```bash
curl http://localhost:8000/api/v1/info
```

3. **Check database connection**
```bash
curl http://localhost:8000/api/v1/db-check
```

### Interactive API Documentation

Visit http://localhost:8000/docs to:
- View all endpoints
- Test endpoints interactively
- See request/response schemas

## 🔧 Configuration

Configuration is managed through environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aurorasync

# Redis
REDIS_URL=redis://localhost:6379/0

# Application
LOG_LEVEL=INFO
ENVIRONMENT=development

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🛠️ Development Commands

### Start server with auto-reload
```bash
uvicorn app.main:app --reload
```

### Start server on different port
```bash
uvicorn app.main:app --reload --port 8080
```

### Reset database (WARNING: deletes all data)
```bash
python scripts/setup_db.py --drop
```

### Run with debug logging
```bash
# Edit .env and set LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

## 🐛 Troubleshooting

### Database connection error

**Error**: `could not connect to server`

**Solution**:
1. Ensure PostgreSQL is running
2. Check DATABASE_URL in .env
3. Verify database exists:
   ```bash
   psql -U postgres -c "CREATE DATABASE aurorasync;"
   ```

### Import errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
1. Ensure you're in the backend directory
2. Activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`

### Port already in use

**Error**: `Address already in use`

**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

## 🤖 Machine Learning Pipeline

### Generate Synthetic Data

```bash
python data_generators/generate_telematics.py
```

This generates:
- 10 vehicles (VEH001-VEH010)
- 2000 rows per vehicle
- Realistic failure patterns
- Output: `ml_models/datasets/telematics_logs.csv`

### Train Model

```bash
python ml_models/train_simple_model.py
```

This trains:
- RandomForest classifier
- 7 features (engine_temp, brake_pad_wear, etc.)
- Binary classification (failure/no failure)
- Output: `ml_models/trained/simple_failure_model.pkl`

### Test Predictions

```bash
# Test via API
curl -X POST http://localhost:8000/api/v1/predict/test \
  -H "Content-Type: application/json" \
  -d '{
    "engine_temp": 110.0,
    "brake_pad_wear": 2.0,
    "battery_voltage": 11.5,
    "vibration": 1.2,
    "tyre_pressure": 28.0,
    "odometer": 50000.0,
    "ambient_temp": 35.0
  }'

# Or run test script
python scripts/test_ml_pipeline.py
```

### ML Endpoints

- `POST /api/v1/predict/test` - Single prediction
- `POST /api/v1/predict/batch` - Batch predictions
- `GET /api/v1/predict/model-info` - Model information

## 🎤 Voice Agent System

### Start Voice Conversation

```bash
curl -X POST http://localhost:8000/api/v1/voice/engage \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "predicted_failure",
    "vehicle_data": {
      "vehicle_id": "VEH001",
      "owner_name": "Rahul",
      "model": "Honda Accord"
    },
    "prediction_data": {
      "component": "brake_system",
      "probability": 0.85,
      "risk_level": "high"
    },
    "booking_data": {
      "workshop_name": "AutoCare Mumbai",
      "recommended_slot": "tomorrow at 10 AM"
    }
  }'
```

### Voice Endpoints

- `POST /api/v1/voice/engage` - Start voice conversation
- `POST /api/v1/voice/continue` - Continue conversation
- `POST /api/v1/voice/transcribe` - Transcribe audio
- `GET /api/v1/voice/voices` - List available voices
- `POST /api/v1/voice/tts` - Generate TTS

### Available Scenarios

- `predicted_failure` - Notify about predicted failure
- `urgent_alert` - Critical alert
- `appointment_reminder` - Remind about appointment
- `post_service_feedback` - Collect feedback
- `booking_recovery` - Recover declined booking

### Available Voices

- `Aurora_Default` - Standard female voice
- `Aurora_Indian_Female` - Warm, empathetic female
- `Aurora_Indian_Male` - Professional male voice
- `Aurora_Urgent_Alert` - Urgent but calm voice

## 📚 Next Steps

1. ✅ Backend structure created
2. ✅ Database models defined
3. ✅ Core API endpoints working
4. ✅ Multi-agent system implemented
5. ✅ ML pipeline integrated
6. ✅ Voice Agent system implemented
7. 🔄 Add vehicle CRUD endpoints
8. 🔄 Add Redis pub/sub
9. 🔄 Build frontend dashboard

## 🤝 Contributing

Follow the implementation roadmap in `IMPLEMENTATION_ROADMAP.md`.

## 📄 License

MIT License - See LICENSE file for details.
