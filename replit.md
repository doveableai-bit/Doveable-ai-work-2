# Doveable AI Website Builder

## Overview
A full-stack AI-powered website builder that uses multiple LLM providers (Google Gemini, Groq, OpenAI, Emergent LLM) to generate complete, multi-page, interactive web applications from natural language prompts.

## Project Architecture

### Frontend
- **Framework**: React 19.2.0 with TypeScript
- **Build Tool**: Vite 6.2.0
- **Styling**: Tailwind CSS (via CDN)
- **Port**: 5000 (configured for Replit)

### Backend (Optional - NEW!)
- **Framework**: FastAPI (Python)
- **LLM Providers**: Google Gemini, Groq, OpenAI, Emergent LLM
- **Database**: MongoDB (optional, for project persistence)
- **Port**: 8000 (default)
- **API Documentation**: Available at `/docs` when backend is running

### Storage
- **Frontend**: LocalStorage for user data and configurations
- **Backend**: MongoDB (optional) for persistent project storage

## Key Features
- **Multi-LLM Support**: Choose from Gemini, Groq, OpenAI, or Emergent LLM
- **Full-Stack Architecture**: React frontend + FastAPI backend
- **AI-Powered Generation**: Create complete websites from prompts
- **Project Management**: Save, edit, and manage multiple projects
- **File Explorer & Code Editor**: Browse and edit generated files
- **Live Preview**: Real-time preview of generated websites
- **Admin Panel**: Manage API keys and configurations
- **Vercel-Ready**: Optimized for deployment on Vercel

## Environment Variables

### Frontend (.env.local)
- `GEMINI_API_KEY`: Required for AI functionality (Gemini API key from Google)
- `VITE_API_URL`: Optional - Backend API URL (leave empty for frontend-only mode)

### Backend (backend/.env)
- `GEMINI_API_KEY`: Google Gemini API key
- `GROQ_API_KEY`: Groq API key (optional)
- `EMERGENT_LLM_KEY`: Emergent LLM API key (optional)
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `MONGO_URL`: MongoDB connection string (optional)
- `DB_NAME`: Database name (optional, default: doveable_ai)
- `CORS_ORIGINS`: Allowed CORS origins (default: *)

## Running Locally

### Frontend Only (Current Setup):
```bash
npm install
npm run dev
```
Visit http://localhost:5000

### Full Stack (Frontend + Backend):
**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

## Recent Changes (2025-11-12)

### AI Enhancement - Universal Website Generation (LATEST)
- **Enhanced AI to generate ANY type of website from a simple prompt**
- Added explicit support for 10+ website types:
  - E-Commerce (product grids, shopping cart, checkout)
  - Portfolio (project showcases, skills, contact forms)
  - Blog/Magazine (articles, categories, author bios)
  - SaaS Landing Pages (features, pricing, testimonials)
  - Business Websites (services, team, case studies)
  - Dashboards (data tables, charts, analytics)
  - Documentation Sites (navigation, search)
  - Restaurant/Food (menus, ordering, reservations)
  - Real Estate (property listings, filters)
  - And more!
- **Mobile-First Responsive Design** - All generated websites now automatically work perfectly on:
  - Android phones (mobile-first design)
  - Tablets (responsive breakpoints)
  - Desktop PCs (full responsive layout)
- Enhanced prompts with Tailwind CSS mobile-first best practices
- Mandatory viewport meta tags for accessibility
- Touch-friendly UI elements (44x44px minimum)
- Responsive grids, typography, spacing, and images

### Replit Migration
- **Successfully migrated from Vercel to Replit**
- Reorganized Python backend into routes/ directory structure with absolute imports
- Fixed all TypeScript import paths for flat frontend structure (all .tsx/.ts files in root)
- Created .env file with VITE_API_URL pointing to backend API
- Set up start.sh script to run both frontend and backend concurrently
- Configured workflow "Doveable AI" to auto-start both services
- Backend binds to 0.0.0.0:8000 (internal), Frontend serves on port 5000 (public)
- Application running successfully on Replit

### Frontend Setup
- Configured Vite to use port 5000 (required for Replit)
- Added HMR configuration for Replit's proxy environment
- Set up workflow for automatic server restart
- Installed all frontend dependencies (React, Vite, TypeScript, Axios)

### Backend
- FastAPI backend with Python on port 8000
- Implemented LLM service supporting multiple providers (Gemini, Groq, OpenAI, Emergent)
- MongoDB integration for project storage
- API endpoints for LLM generation, project management, chat history, auth, and GitHub sync

### Documentation
- Created comprehensive README.md
- Added DEPLOYMENT.md for deployment guide
- Updated .gitignore for Python and environment files

## File Structure

**Note**: The frontend currently uses a **flat file structure** (all .tsx and .ts files in root directory). This was maintained during the Replit migration to avoid breaking 40+ import paths. The backend Python code is properly organized in the routes/ directory.

```
doveable-ai-website-builder/
├── routes/                 # Python backend routes (organized)
│   ├── __init__.py
│   ├── llm_routes.py      # LLM API endpoints
│   ├── project_routes.py  # Project CRUD
│   ├── chat_history_routes.py
│   ├── auth_routes.py
│   └── github_sync_routes.py
├── main.py                # FastAPI application entry point
├── database.py            # MongoDB connection
├── llm_service.py         # Multi-provider LLM service
├── schemas.py             # Pydantic models
├── requirements.txt       # Python dependencies
├── start.sh               # Concurrent startup script
│
├── *.tsx                  # React components (flat structure)
│   ├── App.tsx, HomePage.tsx, WebsiteBuilder.tsx
│   ├── AdminPanel.tsx, AdminLoginPage.tsx
│   ├── CodePanel.tsx, ChatPanel.tsx, PreviewPanel.tsx
│   ├── FileExplorer.tsx, LogsPanel.tsx, Sidebar.tsx
│   ├── MyProjectsModal.tsx, PaymentModal.tsx
│   └── ... (all components in root)
│
├── *.ts                   # Services and utilities (flat structure)
│   ├── geminiService.ts, backendApiService.ts
│   ├── githubService.ts, googleDriveService.ts
│   ├── supabaseService.ts, learningService.ts
│   └── types.ts
│
├── Icons.tsx              # Icon components
├── index.tsx              # React entry point
├── vite.config.ts         # Vite configuration (port 5000)
├── package.json           # Node dependencies
├── .env                   # Environment variables
├── README.md              # Project documentation
└── replit.md              # This file
```

**Future Improvement**: Consider reorganizing frontend into `components/` and `services/` directories when time permits.

## API Endpoints (Backend)

### LLM Endpoints
- `POST /api/llm/generate` - Generate text using LLM
  - Request: `{ "prompt": "...", "provider": "auto|groq|gemini|openai" }`
  - Response: `{ "success": true, "response": "...", "provider": "...", "model": "..." }`
- `GET /api/llm/providers` - Get list of available LLM providers
- `GET /api/llm/health` - Check LLM service health status

### Project Endpoints
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}` - Get project by ID
- `DELETE /api/projects/{id}` - Delete project

## Deployment Options

### Option 1: Replit (Full Stack - Current)
Currently running on Replit with both frontend (port 5000) and backend (port 8000). The backend provides multi-LLM support, MongoDB integration, and API endpoints. Start with: `bash start.sh` or use the "Doveable AI" workflow.

### Option 2: Vercel (Full Stack)
Deploy both frontend and backend to Vercel:
```bash
vercel --prod
```
See DEPLOYMENT.md for detailed instructions.

### Option 3: Split Deployment
- Frontend: Deploy to Vercel/Netlify/Replit
- Backend: Deploy to Heroku/Railway/Render
- Set `VITE_API_URL` to point to your backend

## User Preferences
None specified yet.
