# 🚀 AuroraSync OS Backend - Complete Setup Guide

Step-by-step guide to get the backend running in 10 minutes.

---

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.11 or higher installed
- [ ] pip (Python package manager) installed
- [ ] PostgreSQL 15+ installed OR Docker Desktop
- [ ] Git installed
- [ ] Terminal/Command Prompt access

---

## 📦 Step 1: Install Python Dependencies (2 minutes)

### 1.1 Navigate to backend directory
```bash
cd backend
```

### 1.2 Create virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.3 Install dependencies
```bash
pip install -r requirements.txt
```

Expected output: Successfully installed fastapi, uvicorn, sqlalchemy, etc.

---

## 🗄️ Step 2: Set Up PostgreSQL (3 minutes)

Choose **Option A** (Docker - Recommended) or **Option B** (Local PostgreSQL).

### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL container
docker run -d \
  --name aurorasync-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=aurorasync \
  -p 5432:5432 \
  postgres:15

# Verify it's running
docker ps
```

You should see `aurorasync-postgres` in the list.

### Option B: Using Local PostgreSQL

1. **Start PostgreSQL service**
   - Windows: Services → PostgreSQL → Start
   - Mac: `brew services start postgresql`
   - Linux: `sudo systemctl start postgresql`

2. **Create database**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE aurorasync;
   
   # Exit
   \q
   ```

---

## ⚙️ Step 3: Configure Environment (1 minute)

### 3.1 Copy environment template
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

### 3.2 Edit .env file (if needed)

Open `.env` in your text editor. Default values should work:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aurorasync
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**Only change if**:
- Your PostgreSQL password is different
- Your PostgreSQL port is different (default: 5432)
- Your database name is different

---

## 🏗️ Step 4: Create Database Tables (1 minute)

```bash
python scripts/setup_db.py
```

Expected output:
```
============================================================
🔧 AuroraSync OS - Database Setup
============================================================

📊 Project: AuroraSync OS v0.1.0
🗄️  Database URL: postgresql://postgres:postgres@localhost:5432/aurorasync
🌍 Environment: development

📦 Creating database tables...

📋 Registered models:
   - Vehicle
   - Prediction
   - UEBAEvent

✅ Database tables created successfully!
✅ Successfully created tables:
   ✓ vehicles
   ✓ predictions
   ✓ ueba_events

============================================================
🎉 Database setup complete!
============================================================
```

---

## 🚀 Step 5: Start the API Server (1 minute)

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     🚀 Starting AuroraSync OS v0.1.0
INFO:     📊 Environment: development
INFO:     🔗 API Prefix: /api/v1
INFO:     🌐 CORS Origins: http://localhost:3000, http://localhost:5173
INFO:     ✅ Application startup complete
INFO:     Application startup complete.
```

**Server is now running!** 🎉

---

## ✅ Step 6: Verify Installation (2 minutes)

### 6.1 Test with browser

Open your browser and visit:

1. **API Root**: http://localhost:8000
   - Should show welcome message

2. **Health Check**: http://localhost:8000/health
   - Should show `{"status": "ok"}`

3. **API Docs**: http://localhost:8000/docs
   - Should show interactive API documentation

4. **System Info**: http://localhost:8000/api/v1/info
   - Should show project information

5. **Database Check**: http://localhost:8000/api/v1/db-check
   - Should show `{"status": "ok", "database": "connected"}`

### 6.2 Test with script

In a **new terminal** (keep the server running):

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run test script
python scripts/test_api.py
```

Expected output:
```
============================================================
🧪 AuroraSync OS - API Test Suite
============================================================

Testing Root endpoint... ✅ PASS
Testing Health check (root)... ✅ PASS
Testing Health check (API v1)... ✅ PASS
Testing System info... ✅ PASS
Testing Database check... ✅ PASS

============================================================
✅ All tests passed! (5/5)
============================================================

🎉 Backend is working correctly!
```

---

## 🎉 Success! What's Next?

Your backend is now running successfully! Here's what you can do:

### Explore the API
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### Next Development Steps
1. ✅ Backend structure created
2. ✅ Database models defined
3. ✅ Core API endpoints working
4. 🔄 Add vehicle CRUD endpoints
5. 🔄 Add prediction endpoints
6. 🔄 Implement agent modules
7. 🔄 Add ML model integration

### Useful Commands

```bash
# Start server
uvicorn app.main:app --reload

# Start on different port
uvicorn app.main:app --reload --port 8080

# Reset database (WARNING: deletes all data)
python scripts/setup_db.py --drop

# Test API
python scripts/test_api.py

# Stop server
# Press CTRL+C in the terminal
```

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'app'"

**Solution**:
```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "could not connect to server"

**Solution**:
```bash
# Check if PostgreSQL is running
docker ps  # If using Docker

# Or restart PostgreSQL
docker restart aurorasync-postgres  # Docker
# OR
# Restart PostgreSQL service on your system
```

### Problem: "Address already in use"

**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Then start server again
uvicorn app.main:app --reload
```

### Problem: "Database does not exist"

**Solution**:
```bash
# Using Docker
docker exec -it aurorasync-postgres psql -U postgres -c "CREATE DATABASE aurorasync;"

# Using local PostgreSQL
psql -U postgres -c "CREATE DATABASE aurorasync;"
```

### Problem: "Permission denied" on PostgreSQL

**Solution**:
```bash
# Update DATABASE_URL in .env with correct password
# Example:
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/aurorasync
```

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

---

## 🎯 Quick Reference

### File Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── database.py      # DB connection
│   ├── api/routes/      # API endpoints
│   └── models/          # Database models
├── scripts/
│   ├── setup_db.py      # Database setup
│   └── test_api.py      # API tests
└── requirements.txt     # Dependencies
```

### Key URLs
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Info: http://localhost:8000/api/v1/info

### Key Commands
```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/setup_db.py

# Run
uvicorn app.main:app --reload

# Test
python scripts/test_api.py
```

---

<div align="center">

**🎉 Congratulations! Your backend is ready! 🎉**

**Next**: Follow Day 4 tasks in `IMPLEMENTATION_ROADMAP.md`

</div>
