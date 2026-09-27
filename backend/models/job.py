from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), nullable=True)
    company = Column(String(150), nullable=True)
    raw_text = Column(Text, nullable=False)
    required_skills = Column(JSON, nullable=True)   # ['Python', 'FastAPI', 'Docker']
    preferred_skills = Column(JSON, nullable=True)  # ['Kubernetes', 'AWS']
    experience_level = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    matches = relationship("JobMatch", back_populates="job_description", cascade="all, delete-orphan")

class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Matching Scores (0 - 100)
    overall_match_percentage = Column(Float, nullable=False)
    semantic_similarity_score = Column(Float, nullable=False)
    skill_match_score = Column(Float, nullable=False)
    experience_relevance_score = Column(Float, nullable=False)
    
    # Skill Gap & Analysis Details
    matching_skills = Column(JSON, nullable=False)        # ['Python', 'SQL']
    missing_skills = Column(JSON, nullable=False)         # ['Docker', 'AWS']
    partial_skills = Column(JSON, nullable=True)          # ['Cloud Deployment']
    skill_gap_priority = Column(JSON, nullable=True)      # {'high': [...], 'medium': [...], 'low': [...]}
    learning_roadmap = Column(JSON, nullable=True)        # Structured learning path for missing skills
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job_description = relationship("JobDescription", back_populates="matches")
