import os
import shutil
import time
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.database import get_db
from backend.models.user import User
from backend.models.resume import Resume
from backend.schemas.common import APIResponse
from backend.schemas.resume import ResumeOut
from backend.nlp.parser import parse_document
from backend.utils.security import get_optional_user, get_current_user
from backend.utils.validators import validate_resume_file

router = APIRouter(prefix="/resume", tags=["Resume Processing"])
settings = get_settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

class ResumeTextCreate(BaseModel):
    title: Optional[str] = "Pasted_Resume"
    raw_text: str

@router.post("/upload", response_model=APIResponse[ResumeOut], status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Uploads, validates, parses, and stores a resume (PDF/DOCX) in MySQL.
    """
    file_bytes = await file.read()
    validate_resume_file(file, file_bytes)

    # Clean filename and generate safe path
    original_name = os.path.basename(file.filename or "resume.pdf")
    user_prefix = f"user_{current_user.id}_" if current_user else "guest_"
    safe_filename = f"{user_prefix}{int(time.time())}_{original_name}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    ext = original_name.rsplit(".", 1)[-1].lower()

    # Extract raw text from document
    try:
        raw_text = parse_document(file_bytes, ext)
    except Exception as e:
        raw_text = ""

    if len(raw_text.strip().split()) < 15:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract sufficient text from this document. Please ensure the PDF is not an unreadable image, or paste your resume text directly using the 'Paste Text' tab."
        )

    # Create Resume DB Record in MySQL
    resume = Resume(
        user_id=current_user.id if current_user else None,
        filename=original_name,
        file_path=file_path,
        file_type=ext,
        file_size_bytes=len(file_bytes),
        raw_text=raw_text,
        parsed_json={}
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return APIResponse(
        success=True,
        message=f"Resume uploaded and parsed successfully ({len(raw_text.split())} words extracted).",
        data=ResumeOut.model_validate(resume)
    )

@router.post("/create_text", response_model=APIResponse[ResumeOut], status_code=status.HTTP_201_CREATED)
def create_resume_from_text(
    payload: ResumeTextCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Creates a resume record directly from pasted plain text.
    """
    if not payload.raw_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume text cannot be empty.")

    resume = Resume(
        user_id=current_user.id if current_user else None,
        filename=f"{payload.title or 'Pasted_Resume'}.txt",
        file_path="direct_text_input",
        file_type="txt",
        file_size_bytes=len(payload.raw_text.encode('utf-8')),
        raw_text=payload.raw_text.strip(),
        parsed_json={}
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return APIResponse(
        success=True,
        message="Resume text saved successfully.",
        data=ResumeOut.model_validate(resume)
    )

@router.get("/list", response_model=APIResponse[List[ResumeOut]])
def list_user_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lists all resumes uploaded by the authenticated user."""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return APIResponse(
        success=True,
        message=f"Retrieved {len(resumes)} resumes.",
        data=[ResumeOut.model_validate(r) for r in resumes]
    )

@router.get("/{resume_id}", response_model=APIResponse[ResumeOut])
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Retrieves metadata and parsed content of a specific resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
    return APIResponse(
        success=True,
        message="Resume retrieved.",
        data=ResumeOut.model_validate(resume)
    )
