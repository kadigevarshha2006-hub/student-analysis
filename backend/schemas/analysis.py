from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ATSCheckItem(BaseModel):
    check: str
    status: str  # PASS, WARNING, FAIL
    score: float
    message: str
    recommendation: Optional[str] = None

class BulletImprovementSchema(BaseModel):
    original_text: str
    suggested_text: str
    reasoning: str
    improvement_type: str = "action_verb"

class ResumeAnalysisOut(BaseModel):
    id: int
    resume_id: int
    overall_score: float
    ats_score: float
    quality_score: float
    skills_score: float
    readability_score: float
    formatting_score: float
    section_breakdown: Optional[Dict[str, float]] = None
    ats_checks: Optional[List[ATSCheckItem]] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendations: List[str] = []
    project_feedback: Optional[List[Dict[str, Any]]] = None
    experience_feedback: Optional[List[Dict[str, Any]]] = None
    bullet_improvements: Optional[List[BulletImprovementSchema]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ResumeAnalysisRequest(BaseModel):
    resume_id: int
    enable_ai_reasoning: bool = True
