from backend.routes.auth import router as auth_router
from backend.routes.resume import router as resume_router
from backend.routes.analysis import router as analysis_router
from backend.routes.job import router as job_router
from backend.routes.demo import router as demo_router

__all__ = [
    "auth_router",
    "resume_router",
    "analysis_router",
    "job_router",
    "demo_router",
]


