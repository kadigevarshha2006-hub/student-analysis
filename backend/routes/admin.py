from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.database import get_db, engine
from backend.models.user import User
from backend.models.resume import Resume
from backend.models.analysis import ResumeAnalysis
from backend.models.job import JobDescription, JobMatch
from backend.models.skill import ResumeSkill
from backend.schemas.common import APIResponse

router = APIRouter(prefix="/admin", tags=["Database Administration"])

@router.get("/overview", response_model=APIResponse[Dict[str, Any]])
def get_database_overview(db: Session = Depends(get_db)):
    """
    Returns an overview of all database records:
    - Connected database engine (SQLite on Render / MySQL)
    - Total record counts
    - List of all registered users
    - List of all uploaded resumes with uploader email & scores
    - List of all resume analyses & ATS scores
    """
    driver_name = engine.url.drivername if hasattr(engine, "url") else "unknown"
    db_type_label = "SQLite (Render Cloud Storage)" if "sqlite" in driver_name.lower() else "MySQL Database"

    # Query counts
    user_count = db.query(User).count()
    resume_count = db.query(Resume).count()
    analysis_count = db.query(ResumeAnalysis).count()
    match_count = db.query(JobMatch).count()

    # Query all users
    users = db.query(User).order_by(User.created_at.desc()).all()
    user_list = []
    for u in users:
        resume_cnt = len(u.resumes) if u.resumes else 0
        user_list.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "is_active": u.is_active,
            "resumes_count": resume_cnt,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else "N/A"
        })

    # Query all resumes
    resumes = db.query(Resume).order_by(Resume.created_at.desc()).all()
    resume_list = []
    for r in resumes:
        uploader_email = r.user.email if r.user else "Guest Upload"
        uploader_name = r.user.full_name if r.user else "Guest"
        
        overall = None
        ats = None
        analysis_id = None
        if r.analysis:
            overall = round(r.analysis.overall_score, 1)
            ats = round(r.analysis.ats_score, 1)
            analysis_id = r.analysis.id

        resume_list.append({
            "id": r.id,
            "filename": r.filename,
            "file_type": r.file_type,
            "file_size_bytes": r.file_size_bytes,
            "user_id": r.user_id,
            "uploader_email": uploader_email,
            "uploader_name": uploader_name,
            "overall_score": overall,
            "ats_score": ats,
            "analysis_id": analysis_id,
            "has_analysis": bool(r.analysis),
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "N/A"
        })

    # Query all analyses
    analyses = db.query(ResumeAnalysis).order_by(ResumeAnalysis.created_at.desc()).all()
    analysis_list = []
    for a in analyses:
        resume_name = a.resume.filename if a.resume else "N/A"
        user_email = a.resume.user.email if (a.resume and a.resume.user) else "Guest"
        analysis_list.append({
            "id": a.id,
            "resume_id": a.resume_id,
            "resume_filename": resume_name,
            "user_email": user_email,
            "overall_score": round(a.overall_score, 1) if a.overall_score is not None else 0,
            "ats_score": round(a.ats_score, 1) if a.ats_score is not None else 0,
            "quality_score": round(a.quality_score, 1) if a.quality_score is not None else 0,
            "skills_score": round(a.skills_score, 1) if a.skills_score is not None else 0,
            "readability_score": round(a.readability_score, 1) if a.readability_score is not None else 0,
            "formatting_score": round(a.formatting_score, 1) if a.formatting_score is not None else 0,
            "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else "N/A"
        })

    return APIResponse(
        success=True,
        message="Database overview retrieved successfully.",
        data={
            "database_engine": db_type_label,
            "database_dialect": driver_name,
            "server_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "counts": {
                "users": user_count,
                "resumes": resume_count,
                "analyses": analysis_count,
                "job_matches": match_count
            },
            "users": user_list,
            "resumes": resume_list,
            "analyses": analysis_list
        }
    )

@router.get("/export")
def export_database_json(db: Session = Depends(get_db)):
    """Exports all non-sensitive database records as formatted JSON."""
    overview = get_database_overview(db)
    return JSONResponse(
        content=overview.data,
        headers={"Content-Disposition": f"attachment; filename=resume_ai_db_dump_{int(datetime.utcnow().timestamp())}.json"}
    )
