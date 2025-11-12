# Deployment Guide for Doveable AI Website Builder

## Overview
This project is a full-stack application with:
- **Frontend**: React + Vite + TypeScript
- **Backend**: FastAPI (Python) with multiple LLM providers
- **Database**: MongoDB (optional, for project storage)
- **Deployment Target**: Vercel

## Prerequisites

### 1. Environment Variables
You'll need to set up the following environment variables:

#### Required for AI Features (at least one):
- `GEMINI_API_KEY` - Google Gemini API key (Primary - Recommended)
- `GROQ_API_KEY` - Groq API key (Optional - Fast inference)
- `EMERGENT_LLM_KEY` - Emergent LLM API key (Optional - Multi-model support)
- `OPENAI_API_KEY` - OpenAI API key (Optional)

#### Optional (for MongoDB features):
- `MONGO_URL` - MongoDB connection string
- `DB_NAME` - Database name (default: doveable_ai)

#### Frontend Configuration:
- `VITE_API_URL` - Backend API URL (set automatically by Vercel)

### 2. Get API Keys

#### Google Gemini API Key:
1. Visit https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

#### Groq API Key (Optional):
1. Visit https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

#### OpenAI API Key (Optional):
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new secret key

## Deploying to Vercel

### Method 1: Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set Environment Variables:**
   ```bash
   vercel env add GEMINI_API_KEY
   vercel env add GROQ_API_KEY
   vercel env add EMERGENT_LLM_KEY
   vercel env add OPENAI_API_KEY
   vercel env add MONGO_URL
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Method 2: Vercel Dashboard

1. **Import Repository:**
   - Go to https://vercel.com/
   - Click "Add New Project"
   - Import your GitHub repository

2. **Configure Environment Variables:**
   - Go to Project Settings → Environment Variables
   - Add all required API keys:
     - `GEMINI_API_KEY`
     - `GROQ_API_KEY` (optional)
     - `EMERGENT_LLM_KEY` (optional)
     - `OPENAI_API_KEY` (optional)
     - `MONGO_URL` (optional)

3. **Deploy:**
   - Click "Deploy"
   - Vercel will automatically detect the configuration from `vercel.json`

## MongoDB Setup (Optional)

If you want to use MongoDB for project storage:

### Option 1: MongoDB Atlas (Free Tier)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new cluster
4. Get your connection string
5. Add it as `MONGO_URL` environment variable

### Option 2: Use Local Storage Only
The application will work without MongoDB, using browser's localStorage for data persistence.

## Running Locally

### Frontend Only:
```bash
npm install
npm run dev
```
Visit http://localhost:5000

### Backend (Optional):
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on http://localhost:8000

### Full Stack:
1. Start backend: `cd backend && python main.py`
2. Start frontend: `npm run dev`
3. Set `VITE_API_URL=http://localhost:8000` in `.env.local`

## Vercel Configuration

The `vercel.json` file is already configured with:
- Frontend build using Vite
- Backend API routes at `/api/*`
- Environment variable references
- Proper routing for SPA

## Post-Deployment

After deployment:
1. Visit your Vercel URL
2. The app should load the frontend
3. Test API endpoints at `https://your-app.vercel.app/api/health`
4. Check available LLM providers at `https://your-app.vercel.app/api/llm/providers`

## Troubleshooting

### Backend API Not Working:
- Check environment variables are set correctly
- Verify `vercel.json` routing configuration
- Check Vercel function logs

### Frontend Not Loading:
- Ensure build completed successfully
- Check browser console for errors
- Verify `dist` folder was created

### LLM Not Working:
- Verify at least one API key is set correctly
- Test with `/api/llm/health` endpoint
- Check API key quotas and limits

## Architecture

```
┌─────────────────────────────────────┐
│         Vercel Deployment           │
├─────────────────────────────────────┤
│                                     │
│  Frontend (React + Vite)            │
│  ├── Port 5000 (dev)                │
│  └── Served from /dist              │
│                                     │
│  Backend API (FastAPI)              │
│  ├── Routes at /api/*               │
│  ├── LLM Service (Multi-provider)   │
│  └── MongoDB Integration (optional) │
│                                     │
└─────────────────────────────────────┘
```

## Support

For issues or questions:
- Check Vercel deployment logs
- Review backend logs in Vercel Functions
- Verify all environment variables are set
- Ensure API keys are valid and have quota
