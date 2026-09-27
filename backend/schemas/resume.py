from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class EducationItem(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    gpa: Optional[str] = None

class ExperienceItem(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    bullets: List[str] = []

class ProjectItem(BaseModel):
    title: Optional[str] = None
    technologies: List[str] = []
    description: Optional[str] = None
    bullets: List[str] = []

class ParsedResumeData(BaseModel):
    personal_info: ContactInfo = ContactInfo()
    education: List[EducationItem] = []
    skills: Dict[str, List[str]] = {}  # {'Programming': ['Python', 'C++'], ...}
    experience: List[ExperienceItem] = []
    projects: List[ProjectItem] = []
    certifications: List[str] = []
    achievements: List[str] = []

class ResumeSkillOut(BaseModel):
    skill_name: str
    category: str
    source: str
    confidence_score: float

    class Config:
        from_attributes = True

class ResumeOut(BaseModel):
    id: int
    user_id: Optional[int]
    filename: str
    file_type: str
    file_size_bytes: int
    parsed_json: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
