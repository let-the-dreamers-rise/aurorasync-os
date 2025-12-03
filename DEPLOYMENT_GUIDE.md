# 🚀 Deployment Guide - GitHub & Vercel

## Step 1: Push to GitHub

### Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit - AuroraSync OS Hackathon Project"
```

### Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., "aurorasync-os")
3. Don't initialize with README (we already have one)

### Push to GitHub
```bash
# Replace YOUR_USERNAME and YOUR_REPO with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Frontend to Vercel

### Option A: Deploy via Vercel Website (Recommended)

1. **Go to Vercel**
   - Visit https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Build Settings**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Environment Variables** (Optional)
   ```
   VITE_API_URL=http://localhost:8000
   ```
   (Leave as localhost for demo, or deploy backend separately)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live at: `https://your-project.vercel.app`

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: aurorasync-os
# - Directory: ./
# - Override settings? No

# Deploy to production
vercel --prod
```

## Step 3: Deploy Backend (Optional)

### Option A: Deploy to Render.com

1. **Go to Render**
   - Visit https://render.com
   - Sign up/Sign in

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     ```
     Name: aurorasync-backend
     Root Directory: backend
     Runtime: Python 3
     Build Command: pip install -r requirements-simple.txt
     Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

3. **Environment Variables**
   ```
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Get your backend URL: `https://aurorasync-backend.onrender.com`

### Option B: Deploy to Railway.app

1. **Go to Railway**
   - Visit https://railway.app
   - Sign in with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Root directory: `backend`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**
   - Railway will auto-deploy
   - Get your URL from the deployment

## Step 4: Update Frontend API URL

If you deployed the backend, update the frontend to use the production API:

### Edit `frontend/.env.production`
```env
VITE_API_URL=https://your-backend-url.onrender.com
```

### Redeploy Frontend
```bash
cd frontend
vercel --prod
```

## Step 5: Test Deployment

1. **Visit your Vercel URL**
   ```
   https://your-project.vercel.app
   ```

2. **Test all pages:**
   - ✅ Dashboard
   - ✅ Vehicles
   - ✅ Predictions
   - ✅ Scheduling
   - ✅ AI Conversations
   - ✅ Workshops
   - ✅ RCA Insights
   - ✅ System Health

3. **Verify mock data is working**
   - All pages should load with mock data
   - No errors in console
   - Smooth navigation

## Quick Commands Summary

```bash
# 1. Clean up docs
cleanup_docs.bat

# 2. Commit and push
git add .
git commit -m "Ready for hackathon demo"
git push origin main

# 3. Deploy frontend
cd frontend
vercel --prod

# 4. Get your URL
# Check Vercel dashboard or CLI output
```

## Troubleshooting

### Build Fails on Vercel
- Check Node version (should be 18+)
- Verify package.json is in frontend directory
- Check build logs for errors

### Frontend Shows Blank Page
- Check browser console for errors
- Verify build output directory is `dist`
- Check if all dependencies installed

### API Calls Failing
- This is expected! Frontend uses mock data
- No backend needed for demo
- All features work with mock data

## Demo URLs

After deployment, you'll have:

**Frontend (Vercel):**
```
https://aurorasync-os.vercel.app
```

**Backend (Optional - Render/Railway):**
```
https://aurorasync-backend.onrender.com
```

## For Hackathon Judges

Share these links:
- 🌐 **Live Demo:** https://your-project.vercel.app
- 📦 **GitHub Repo:** https://github.com/YOUR_USERNAME/YOUR_REPO
- 📖 **Documentation:** See README.md in repo

## Notes

- ✅ Frontend works standalone with mock data
- ✅ No backend required for demo
- ✅ All features functional
- ✅ Fast loading, no errors
- ✅ Mobile responsive

**Your AuroraSync OS is ready for the hackathon!** 🎉
