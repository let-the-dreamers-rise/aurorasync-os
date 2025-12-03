# 🚀 AuroraSync OS - Quick Start Guide

## Get Started in 30 Minutes

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git

### Step 1: Clone and Setup (5 min)
```bash
git clone <your-repo>
cd aurorasync-os
```

### Step 2: Start Infrastructure (5 min)
```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Wait 30 seconds for services to start
```

### Step 3: Setup Backend (10 min)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python scripts/setup_db.py
python scripts/seed_data.py
python scripts/train_models.py
uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000

### Step 4: Setup Frontend (10 min)
```bash
# New terminal
cd frontend
npm install
npm run dev
```

Frontend will run on: http://localhost:3000

### Step 5: Verify Installation
1. Open http://localhost:3000
2. You should see 10 vehicles on the dashboard
3. Click on VEH003 to see the failure prediction
4. Check Agent Status panel - all should be green

### Demo Mode
```bash
# Start demo simulation
python scripts/run_demo.py
```

This will:
- Generate real-time telematics data
- Trigger failure prediction for VEH003
- Simulate customer call
- Auto-schedule workshop appointment

### Troubleshooting

**Database connection error**:
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart if needed
docker-compose restart postgres
```

**Redis connection error**:
```bash
# Check if Redis is running
docker ps | grep redis

# Restart if needed
docker-compose restart redis
```

**Port already in use**:
```bash
# Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Next Steps
1. Read MASTER_PLAN.md for complete architecture
2. Review DEMO_SCRIPT.md for presentation guide
3. Practice the demo flow
4. Customize for your needs

### Quick Commands
```bash
# Reset database
python scripts/setup_db.py --reset

# Generate new synthetic data
python scripts/seed_data.py --vehicles 10

# Retrain ML models
python scripts/train_models.py

# Run tests
pytest backend/tests

# Build for production
docker-compose up --build
```

### Support
- Check logs: `docker-compose logs -f`
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Ready to win! 🏆**
