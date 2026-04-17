from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

from typing import Optional, List
from models import AnalysisResult, DeepDiveRequest, DeepDiveResult

load_dotenv()

app = FastAPI()

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
    
@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_profile(
    targetRole: str = Form(...),
    githubUrl: Optional[str] = Form(""),
    completedItems: Optional[str] = Form("[]"),
    fastMode: bool = Form(False),
    file: Optional[UploadFile] = File(None)
):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in backend/.env")

    # Parse completed items since it comes as a string in Form
    try:
        completed_list = json.loads(completedItems)
    except:
        completed_list = []

    # Construct the instruction for the LLM
    completed_context = ""
    if completed_list:
        completed_context = f"\nThe user has explicitly completed the following items: {', '.join(completed_list)}.\nTreat these as Acquired Skills, exclude them from the new roadmap, and progress them to more advanced topics."

    roadmap_length = "7 days"
    project_count = "2-3"
    conciseness_instruction = "IMPORTANT FOR SPEED: Strictly limit all 'description' fields to a maximum of 5 to 10 words. Omit unnecessary details." if fastMode else ""

    prompt = f"""
    You are an expert Career Coach and Technical Recruiter. 
    Analyze the following candidate profile details and target role to generate a skill gap analysis, short-term learning roadmap, and project recommendations.
    {completed_context}

    Candidate Profile Information / URL Provided: {githubUrl}
    Target Role: {targetRole}
    
    IMPORTANT: If the Candidate Profile Information or Target Role provided is gibberish, nonsensical (e.g. 'jasdfio', 'asdf'), or completely unrelated to a real professional job/role, DO NOT hallucinate a random roadmap. Instead, return a JSON object with ONLY the "error" field set to "Please provide a valid tech role and meaningful profile information." and leave all other fields empty/default. If a document is attached, extract the baseline skills from the text of the attached document.

    Your tasks:
    1. Extract the candidate's current skills from the profile info (if it's a URL, infer skills a baseline candidate there might have, or if it's text, extract them). If an attached document is present, deeply parse it. Mock baseline skills realistically if URL only.
    2. Determine the core skills required for the Target Role in the current tech industry.
    3. Identify missing skills.
    4. Calculate a match percentage (0-100).
    5. Generate a short-term (e.g. {roadmap_length}) roadmap to learn these missing skills.
    6. Suggest {project_count} specific, domain-relevant practical projects (not just generic courses) that utilize the missing skills.
    
    {conciseness_instruction}

    Return the final result EXCLUSIVELY as a JSON object matching this schema:
    {{
        "currentSkills": ["skill1", "skill2"],
        "missingSkills": ["missing1", "missing2"],
        "role": "{targetRole}",
        "matchPercentage": 50,
        "roadmap": [
            {{ "day": 1, "title": "...", "description": "...", "resources": ["Url"] }}
        ],
        "projects": [
            {{ "title": "...", "description": "...", "skills_utilized": ["..."], "difficulty": "Intermediate" }}
        ]
    }}
    """

    contents = [prompt]
    if file and file.filename:
        file_bytes = await file.read()
        file_part = types.Part.from_bytes(data=file_bytes, mime_type=file.content_type)
        contents.append(file_part)

    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # Parse JSON and validate against our Pydantic model
        result_json = json.loads(response.text)
        analysis = AnalysisResult(**result_json)
        return analysis

    except Exception as e:
        print(f"Error during AI Analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/deep-dive", response_model=DeepDiveResult)
async def get_deep_dive(request: DeepDiveRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set")
    
    prompt = f"""
    Topic to learn: {request.topic}
    Target Role: {request.targetRole}
    
    You are an expert technical mentor. Provide a deep dive for the user to master this specific topic.
    1. Suggest 3 specific, highly-rated courses or tutorials (names and links/search queries).
    2. Suggest 2 official documentations or primary articles.
    3. Suggest 1 or 2 small actionable mini-projects or coding exercises to practice it locally.
    
    Return EXACTLY a JSON matching this schema:
    {{
        "courses": [ {{"name": "...", "link": "...", "duration": "..."}} ],
        "documentations": [ {{"name": "...", "link": "..."}} ],
        "mini_projects": [ "..." ]
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return DeepDiveResult(**json.loads(response.text))
    except Exception as e:
        print(f"Error Deep Dive: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Student Analysis API is running!"}
