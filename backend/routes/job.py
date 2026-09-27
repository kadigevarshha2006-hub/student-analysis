from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.job import JobDescription, JobMatch
from backend.schemas.common import APIResponse
from backend.schemas.job import (
    JobDescriptionCreate, JobDescriptionOut, MatchRequest, JobMatchOut
)
from backend.utils.security import get_optional_user, get_current_user

router = APIRouter(prefix="/job", tags=["Job Description & Matching"])

@router.post("/create", response_model=APIResponse[JobDescriptionOut], status_code=status.HTTP_201_CREATED)
def create_job_description(
    job_in: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Creates and parses a new Job Description."""
    job = JobDescription(
        user_id=current_user.id if current_user else None,
        title=job_in.title,
        company=job_in.company,
        raw_text=job_in.raw_text,
        required_skills=[],
        preferred_skills=[]
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return APIResponse(
        success=True,
        message="Job description created successfully.",
        data=JobDescriptionOut.from_orm(job)
    )

@router.get("/matches", response_model=APIResponse[List[JobMatchOut]])
def get_user_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves all job match reports for the authenticated user's resumes."""
    matches = (
        db.query(JobMatch)
        .join(JobDescription, JobMatch.job_description_id == JobDescription.id)
        .filter(JobDescription.user_id == current_user.id)
        .order_by(JobMatch.created_at.desc())
        .all()
    )
    return APIResponse(
        success=True,
        message=f"Retrieved {len(matches)} matches.",
        data=[JobMatchOut.from_orm(m) for m in matches]
    )

@router.get("/match/{match_id}", response_model=APIResponse[JobMatchOut])
def get_match_report(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Retrieves a specific match report."""
    match = db.query(JobMatch).filter(JobMatch.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match report not found.")
    return APIResponse(
        success=True,
        message="Match report retrieved.",
        data=JobMatchOut.from_orm(match)
    )
