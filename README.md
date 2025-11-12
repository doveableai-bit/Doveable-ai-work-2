# Doveable AI Website Builder

<div align="center">
  <img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

An AI-powered website builder that uses multiple LLM providers (Google Gemini, Groq, OpenAI, Emergent LLM) to generate complete, multi-page, interactive web applications from natural language prompts.

## 🚀 Features

- **AI-Powered Website Generation**: Generate complete websites using advanced LLMs
- **Multiple LLM Providers**: Support for Gemini, Groq, OpenAI, and Emergent LLM
- **Full-Stack Architecture**: React frontend with FastAPI backend
- **Project Management**: Save, edit, and manage multiple website projects
- **Live Preview**: Real-time preview of generated websites
- **File Explorer**: Browse and edit generated files
- **Code Editor**: Built-in code editor with syntax highlighting
- **Vercel-Ready**: Optimized for deployment on Vercel
- **MongoDB Integration**: Optional database for project persistence

## 🛠 Tech Stack

### Frontend
- **React 19.2** - UI framework
- **TypeScript** - Type safety
- **Vite 6.2** - Build tool and dev server
- **Tailwind CSS** - Styling (via CDN)
- **Alpine.js & htmx** - Lightweight interactivity

### Backend
- **FastAPI** - Python web framework
- **Motor** - Async MongoDB driver
- **Multiple LLM SDKs**:
  - Google Generative AI (Gemini)
  - Groq
  - OpenAI
  - Emergent LLM

## 📋 Prerequisites

- **Node.js** 18+ 
- **Python** 3.9+
- **MongoDB** (optional, for project persistence)
- At least one LLM API key:
  - [Google Gemini API Key](https://aistudio.google.com/apikey) (Recommended)
  - [Groq API Key](https://console.groq.com/)
  - [OpenAI API Key](https://platform.openai.com/)
  - Emergent LLM API Key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd doveable-ai-website-builder
```

### 2. Install Dependencies

#### Frontend:
```bash
npm install
```

#### Backend:
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Set Up Environment Variables

Create a `.env.local` file in the root directory:
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

Create a `backend/.env` file:
```env
# MongoDB (Optional)
MONGO_URL=mongodb://localhost:27017
DB_NAME=doveable_ai

# CORS
CORS_ORIGINS=*

# At least one LLM API key is required
GEMINI_API_KEY=your-gemini-key-here
GROQ_API_KEY=your-groq-key-here
EMERGENT_LLM_KEY=your-emergent-key-here
OPENAI_API_KEY=your-openai-key-here
```

### 4. Run the Application

#### Option A: Frontend Only (Recommended for Replit)
```bash
npm run dev
```
Visit http://localhost:5000

#### Option B: Full Stack (Frontend + Backend)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Set `VITE_API_URL=http://localhost:8000` in `.env.local` to connect frontend to backend.

## 🌐 Deployment to Vercel

### Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/doveable-ai-website-builder)

### Manual Deployment

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
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
   vercel env add MONGO_URL
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📁 Project Structure

```
doveable-ai-website-builder/
├── components/           # React components
│   ├── HomePage.tsx
│   ├── WebsiteBuilder.tsx
│   ├── AdminPanel.tsx
│   └── ...
├── services/            # Frontend services
│   ├── geminiService.ts
│   ├── backendApiService.ts
│   └── ...
├── backend/             # Python backend
│   ├── main.py         # FastAPI application
│   ├── services/       # Backend services
│   │   └── llm_service.py
│   ├── routes/         # API routes
│   │   ├── llm_routes.py
│   │   └── project_routes.py
│   ├── models/         # Pydantic models
│   │   └── schemas.py
│   └── database.py     # MongoDB connection
├── App.tsx             # Main React component
├── index.tsx           # React entry point
├── vite.config.ts      # Vite configuration
├── vercel.json         # Vercel deployment config
└── package.json        # Node dependencies
```

## 🔑 API Endpoints

### LLM Endpoints

- `POST /api/llm/generate` - Generate text using LLM
- `GET /api/llm/providers` - Get available LLM providers
- `GET /api/llm/health` - Check LLM service health

### Project Endpoints (Requires MongoDB)

- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}` - Get project details
- `DELETE /api/projects/{id}` - Delete a project

## 🔧 Configuration

### Vite Configuration
The app is configured to run on port 5000 with Replit-compatible HMR settings in `vite.config.ts`.

### Backend Configuration
FastAPI backend runs on port 8000 by default. CORS is configured to allow requests from the frontend.

### Environment Variables

#### Frontend (.env.local):
- `GEMINI_API_KEY` - Google Gemini API key
- `VITE_API_URL` - Backend API URL (optional)

#### Backend (backend/.env):
- `GEMINI_API_KEY` - Google Gemini API key (Primary - Recommended)
- `GROQ_API_KEY` - Groq API key (Optional - Fast inference)
- `EMERGENT_LLM_KEY` - Emergent LLM API key (Optional - Multi-model support)
- `OPENAI_API_KEY` - OpenAI API key (Optional)
- `MONGO_URL` - MongoDB connection string (Optional)
- `DB_NAME` - Database name (Optional)
- `CORS_ORIGINS` - Allowed CORS origins (Default: *)

## 🧪 Testing

### Test Frontend:
```bash
npm run dev
```
Visit http://localhost:5000

### Test Backend API:
```bash
cd backend
python main.py
```
Visit http://localhost:8000/docs for API documentation

### Test LLM Integration:
```bash
curl -X POST http://localhost:8000/api/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a simple landing page", "provider": "auto"}'
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment help
- Review API documentation at `/api/docs` (when backend is running)
- Ensure API keys are valid and have remaining quota

## 🎯 Roadmap

- [ ] Add more LLM providers
- [ ] Implement user authentication
- [ ] Add website templates
- [ ] Support for custom domains
- [ ] Real-time collaboration
- [ ] Version control for projects
- [ ] Enhanced code editor features

## 🙏 Acknowledgments

- Google Gemini AI
- Groq
- OpenAI
- Emergent LLM
- FastAPI
- React & Vite teams
