from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Quantitative Scores (0 - 100)
    overall_score = Column(Float, nullable=False)
    ats_score = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False)
    skills_score = Column(Float, nullable=False)
    readability_score = Column(Float, nullable=False)
    formatting_score = Column(Float, nullable=False)
    
    # Detailed Structural & Qualitative Breakdowns
    section_breakdown = Column(JSON, nullable=True)     # {'contact': 100, 'education': 90, ...}
    ats_checks_json = Column(JSON, nullable=True)       # [{'check': 'Standard Headings', 'status': 'PASS', 'message': '...'}]
    strengths_json = Column(JSON, nullable=True)        # ['Strong technical skill profile', ...]
    weaknesses_json = Column(JSON, nullable=True)       # ['Missing measurable metrics in project bullets', ...]
    recommendations_json = Column(JSON, nullable=True)  # ['Add GitHub link to header', ...]
    project_feedback_json = Column(JSON, nullable=True)
    experience_feedback_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    resume = relationship("Resume", back_populates="analysis")
    bullet_improvements = relationship("BulletImprovement", back_populates="analysis", cascade="all, delete-orphan")

class BulletImprovement(Base):
    __tablename__ = "bullet_improvements"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analysis.id", ondelete="CASCADE"), nullable=False, index=True)
    original_text = Column(Text, nullable=False)
    suggested_text = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=False)
    improvement_type = Column(String(50), default="action_verb")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    analysis = relationship("ResumeAnalysis", back_populates="bullet_improvements")
