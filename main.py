from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from routes.llm_routes import router as llm_router
from routes.project_routes import router as project_router
from routes.chat_history_routes import router as chat_history_router
from routes.auth_routes import router as auth_router
from routes.github_sync_routes import router as github_sync_router
from database import connect_to_mongo, close_mongo_connection

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Doveable AI Backend",
    description="Backend API for Doveable AI Website Builder with multiple LLM providers, Google Drive OAuth, and GitHub integration",
    version="1.0.0",
    lifespan=lifespan
)

cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router)
app.include_router(project_router)
app.include_router(chat_history_router)
app.include_router(auth_router)
app.include_router(github_sync_router)

@app.get("/")
async def root():
    return {
        "message": "Doveable AI Backend API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
