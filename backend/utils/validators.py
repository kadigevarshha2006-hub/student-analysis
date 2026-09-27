import os
from fastapi import UploadFile, HTTPException, status
from backend.config import get_settings

settings = get_settings()

def validate_resume_file(file: UploadFile, file_bytes: bytes):
    """
    Validates uploaded resume file extension, size, and basic magic byte signature.
    """
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    
    # 1. Extension check
    if ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '.{ext}'. Allowed formats: {', '.join(settings.allowed_extensions_list).upper()}"
        )
    
    # 2. File size check
    if len(file_bytes) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum permitted size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )
    
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty."
        )
    
    # 3. Magic bytes validation
    # PDF files start with %PDF- (hex: 25 50 44 46 2d)
    # DOCX files are ZIPs, starting with PK (hex: 50 4b 03 04)
    if ext == "pdf" and not file_bytes.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Corrupted or invalid PDF file header."
        )
    elif ext == "docx" and not file_bytes.startswith(b"PK"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Corrupted or invalid DOCX file header."
        )
    
    return True
