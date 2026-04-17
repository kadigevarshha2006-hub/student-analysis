from pydantic import BaseModel, Field
from typing import List, Optional

class RoadmapTask(BaseModel):
    day: int = Field(description="The day number (1-7)")
    title: str = Field(description="Title of the daily task")
    description: str = Field(description="Detailed explanation of the task")
    resources: List[str] = Field(description="List of resources or links", default_factory=list)

class ProjectSuggestion(BaseModel):
    title: str = Field(description="Name of the project")
    description: str = Field(description="Description of what to build")
    skills_utilized: List[str] = Field(description="Skills that this project will help improve")
    difficulty: str = Field(description="e.g. Beginner, Intermediate, Advanced")

class AnalysisResult(BaseModel):
    error: Optional[str] = Field(default=None, description="Set this to a polite error message if the user input is gibberish, unrelated to tech roles, or invalid")
    currentSkills: List[str] = Field(default_factory=list, description="List of skills identified in the user's profile")
    missingSkills: List[str] = Field(default_factory=list, description="Skills required for the target role but missing from the user's profile")
    role: str = Field(default="", description="The requested Target Role")
    matchPercentage: int = Field(default=0, description="0-100 indicating how well the user's current skills match the target role requirements")
    roadmap: List[RoadmapTask] = Field(default_factory=list, description="Short-term roadmap to learn the missing skills")
    projects: List[ProjectSuggestion] = Field(default_factory=list, description="AI-generated project ideas")



class CourseSuggestion(BaseModel):
    name: str = Field(description="Name of the course or tutorial")
    link: str = Field(description="URL or search query to find this course or tutorial")
    duration: str = Field(description="Expected time to complete (e.g. 2 hours)")

class DocSuggestion(BaseModel):
    name: str = Field(description="Name of the official documentation or article")
    link: str = Field(description="URL or search query")

class DeepDiveRequest(BaseModel):
    topic: str
    targetRole: str

class DeepDiveResult(BaseModel):
    courses: List[CourseSuggestion] = Field(description="Curated high quality courses/tutorials")
    documentations: List[DocSuggestion] = Field(description="Curated official documentations or articles")
    mini_projects: List[str] = Field(description="1 or 2 small actionable coding steps to master this specific topic")
