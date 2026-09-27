from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class JobDescriptionCreate(BaseModel):
    title: Optional[str] = Field(None, example="Senior Full-Stack Developer")
    company: Optional[str] = Field(None, example="Tech Innovations Inc.")
    raw_text: str = Field(..., min_length=20, example="We are looking for a Python and React Developer...")

class JobDescriptionOut(BaseModel):
    id: int
    title: Optional[str]
    company: Optional[str]
    required_skills: Optional[List[str]]
    preferred_skills: Optional[List[str]]
    experience_level: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class MatchRequest(BaseModel):
    resume_id: int
    job_description_id: Optional[int] = None
    job_description_text: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None

class SkillGapPriority(BaseModel):
    high: List[Dict[str, str]] = []    # [{'skill': 'Docker', 'reason': 'Crucial requirement'}]
    medium: List[Dict[str, str]] = []
    low: List[Dict[str, str]] = []

class LearningRoadmapStep(BaseModel):
    skill: str
    timeline: str
    resources: List[str]
    practical_project: str

class JobMatchOut(BaseModel):
    id: Optional[int] = None
    resume_id: int
    job_description_id: Optional[int] = None
    overall_match_percentage: float
    semantic_similarity_score: float
    skill_match_score: float
    experience_relevance_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    partial_skills: List[str] = []
    skill_gap_priority: Optional[SkillGapPriority] = None
    learning_roadmap: Optional[List[LearningRoadmapStep]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
