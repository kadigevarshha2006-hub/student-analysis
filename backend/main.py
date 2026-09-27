import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from backend.config import get_settings
from backend.database import init_db
from backend.routes import (
    auth_router,
    resume_router,
    analysis_router,
    job_router,
    demo_router,
)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent AI-Powered Resume Analyzer, ATS Scorer & Semantic Job Matching System.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database Schema on Application Startup
@app.on_event("startup")
def on_startup():
    init_db()

# Mount API Routers
app.include_router(auth_router, prefix="/api")
app.include_router(resume_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(job_router, prefix="/api")
app.include_router(demo_router, prefix="/api")

# System Health Check Endpoint
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Mount Frontend Static Assets
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
