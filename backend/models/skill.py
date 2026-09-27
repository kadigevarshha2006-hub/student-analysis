from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.database import Base

class SkillsMaster(Base):
    __tablename__ = "skills_master"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)  # Programming, Web Development, Data, etc.
    aliases = Column(JSON, nullable=True)  # List of synonym strings
    created_at = Column(DateTime, default=datetime.utcnow)

class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), index=True, nullable=False)
    category = Column(String(50), nullable=False)
    source = Column(String(30), default="explicit")  # explicit, inferred, project, experience
    confidence_score = Column(Float, default=1.00)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    resume = relationship("Resume", back_populates="skills")
