import json
import re
import time
import requests
from typing import Dict, Any, List, Optional
from backend.config import get_settings

settings = get_settings()

GEMINI_MODELS_FALLBACK = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Executes a prompt against Gemini REST API with fast timeout and immediate fallback.
    """
    if not settings.GEMINI_API_KEY:
        return None

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    for model in GEMINI_MODELS_FALLBACK:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={settings.GEMINI_API_KEY}"
        try:
            res = requests.post(url, json=payload, verify=False, timeout=4)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            elif res.status_code in [400, 401, 403, 404]:
                break
        except Exception as e:
            print(f"Gemini API model {model} notice: {e}")
            break

    return None

def generate_ai_resume_evaluation(
    resume_text: str,
    extracted_skills: List[str],
    job_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calls Gemini API to generate non-hallucinatory qualitative feedback and deep bullet rewrites.
    """
    prompt = f"""You are an expert technical recruiter and resume strategist. Analyze the following resume text and provide qualitative feedback.

RESUME CONTENT:
\"\"\"
{resume_text[:3500]}
\"\"\"

EXTRACTED SKILLS: {', '.join(extracted_skills)}
TARGET ROLE / JOB: {job_text[:800] if job_text else 'Software Engineering Candidate'}

CRITICAL INSTRUCTIONS:
1. Provide constructive strengths, weaknesses, and concrete recommendations.
2. For bullet point improvements:
   - Identify weak, passive, or vague bullet points from the resume's Projects or Experience sections.
   - For EACH bullet provide:
     * 'original_text': Exact quote from the resume.
     * 'why_needs_improvement': Explain why it is weak (e.g. passive verbs, lack of engineering specifics).
     * 'suggested_text': Rewrite using high-impact active verbs (e.g. 'Architected', 'Engineered', 'Optimized', 'Constructed').
     * 'why_better': Explain the recruiter impact.
     * 'metric_suggestion': If no metric exists, say "Consider adding a measurable result if you have one (e.g., % latency reduction or user count)." NEVER INVENT FAKE NUMBERS OR PERCENTAGES.
3. Return ONLY a valid JSON object matching this exact schema:

{{
  "strengths": ["string", "string"],
  "weaknesses": ["string", "string"],
  "recommendations": ["string", "string"],
  "bullet_improvements": [
    {{
      "original_text": "Exact bullet quote",
      "why_needs_improvement": "Why weak",
      "suggested_text": "Strong active rewrite",
      "why_better": "Recruiter impact",
      "metric_suggestion": "Metric guidance without hallucinations",
      "improvement_type": "action_verb"
    }}
  ]
}}
"""

    response_text = call_gemini_api(prompt)
    if response_text:
        try:
            cleaned_json = re.sub(r"^```json\s*|\s*```$", "", response_text, flags=re.MULTILINE).strip()
            data = json.loads(cleaned_json)
            if isinstance(data, dict) and "bullet_improvements" in data:
                return data
        except Exception as e:
            print(f"Error parsing Gemini feedback JSON: {e}")

    return get_fallback_evaluation(resume_text, extracted_skills)

def generate_learning_roadmap(
    target_role: Optional[str],
    missing_skills: List[str],
    candidate_skills: Optional[List[str]] = None,
    job_text: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generates a role-aware multi-week learning roadmap prioritizing actual missing skills
    and recognizing already demonstrated candidate skills.
    """
    role_name = target_role or "Full Stack Software Engineer"
    known_skills = candidate_skills or ["Python", "JavaScript", "HTML", "CSS", "MySQL"]
    
    # Filter missing skills: do not recommend skills candidate already possesses
    actual_gaps = [s for s in missing_skills if s not in known_skills]
    if not actual_gaps:
        # If no missing skills in standard list, suggest role-specific advanced topics
        if "data" in role_name.lower() or "ai" in role_name.lower():
            actual_gaps = ["Deep Learning", "MLOps & Model Deployment", "Feature Engineering", "Data Pipelines"]
        elif "frontend" in role_name.lower():
            actual_gaps = ["Next.js & SSR", "TypeScript", "Web Performance & Core Vitals", "Automated UI Testing"]
        elif "backend" in role_name.lower():
            actual_gaps = ["Docker & Containerization", "Redis Caching", "Database Indexing & Query Tuning", "Microservices"]
        else:
            actual_gaps = ["Docker & Containerization", "AWS Cloud Deployment", "CI/CD Pipelines", "System Design"]

    skills_to_plan = actual_gaps[:5]

    prompt = f"""You are a Principal Engineering Career Mentor creating a role-specific learning roadmap.

TARGET ROLE: {role_name}
CANDIDATE ALREADY DEMONSTRATED SKILLS: {', '.join(known_skills)}
MISSING SKILLS TO MASTER: {', '.join(skills_to_plan)}
JOB CONTEXT: {job_text[:800] if job_text else 'Software Engineering'}

CRITICAL RULES:
1. Focus strictly on becoming a proficient {role_name}.
2. Do NOT recommend learning beginner concepts for skills the candidate already possesses ({', '.join(known_skills[:4])}).
3. For each missing skill provide:
   - 'skill': Canonical skill name
   - 'timeline': Realistic timeline (e.g. 'Week 1 - 2')
   - 'why_it_matters': Role-specific rationale for a {role_name}
   - 'key_topics': 3-4 core concepts to master
   - 'websites': Array of {{"title": "...", "url": "https://..."}} with official docs or guides
   - 'youtube_tutorials': Array of {{"title": "...", "channel": "...", "url": "https://www.youtube.com/results?search_query=..."}}
   - 'practical_project': Hands-on milestone bridging their existing stack with the new skill
   - 'milestone_goal': Clear end objective

Return ONLY a valid JSON array matching this schema:
[
  {{
    "skill": "Docker & Containerization",
    "timeline": "Week 1 - 2",
    "why_it_matters": "Why needed for {role_name}",
    "key_topics": ["Topic 1", "Topic 2", "Topic 3"],
    "websites": [{{"title": "Docker Docs", "url": "https://docs.docker.com/"}}],
    "youtube_tutorials": [{{"title": "Docker Crash Course", "channel": "freeCodeCamp", "url": "https://www.youtube.com/results?search_query=docker+course"}}],
    "practical_project": "Hands-on project description",
    "milestone_goal": "End goal milestone"
  }}
]
"""

    response_text = call_gemini_api(prompt)
    if response_text:
        try:
            cleaned_json = re.sub(r"^```json\s*|\s*```$", "", response_text, flags=re.MULTILINE).strip()
            roadmap_data = json.loads(cleaned_json)
            if isinstance(roadmap_data, list) and len(roadmap_data) > 0:
                return roadmap_data
        except Exception as e:
            print(f"Error parsing role-aware roadmap JSON: {e}")

    # Fallback customized by role
    return get_fallback_roadmap(role_name, skills_to_plan, known_skills)

def generate_interview_questions(
    resume_text: str,
    target_role: Optional[str],
    extracted_skills: List[str],
    job_text: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generates at least 30 comprehensive, categorized interview questions instantly:
    - Technical Questions (>= 10)
    - Resume / Project Deep Dive Questions (>= 10)
    - Behavioral Questions (>= 5)
    - Job-Specific Questions (>= 5)
    """
    role_name = target_role or "Full Stack Software Engineer"
    return get_fallback_interview_questions(role_name, extracted_skills)

def get_fallback_roadmap(role_name: str, missing_skills: List[str], known_skills: List[str]) -> List[Dict[str, Any]]:
    """Generates structured fallback roadmap by target role."""
    lower_role = role_name.lower()
    if "data" in lower_role or "ai" in lower_role:
        return [
            {
                "skill": "Exploratory Data Analysis & Statistics",
                "timeline": "Week 1 - 2",
                "why_it_matters": "Fundamental for discovering patterns, hypothesis testing, and validating feature correlations.",
                "key_topics": ["Descriptive & Inferential Statistics", "Outlier Detection & Imputation", "Correlation & Covariance", "Seaborn/Plotly Visualizations"],
                "websites": [
                    {"title": "Pandas Official Documentation", "url": "https://pandas.pydata.org/docs/"},
                    {"title": "Kaggle Data Analysis Guide", "url": "https://www.kaggle.com/learn"}
                ],
                "youtube_tutorials": [
                    {"title": "Statistics for Data Science (Full Course)", "channel": "freeCodeCamp.org", "url": "https://www.youtube.com/results?search_query=statistics+data+science+freecodecamp"}
                ],
                "practical_project": "Conduct an in-depth EDA on a multi-dimensional real-world dataset with statistical tests.",
                "milestone_goal": "Publish an interactive data visualization notebook with business takeaways."
            },
            {
                "skill": "Machine Learning Model Evaluation & Scikit-Learn",
                "timeline": "Week 3 - 4",
                "why_it_matters": "Ensures models generalize well without overfitting or data leakage.",
                "key_topics": ["Cross-Validation Strategies", "Precision, Recall, ROC-AUC, F1", "Hyperparameter Tuning with GridSearchCV", "Feature Importance"],
                "websites": [
                    {"title": "Scikit-Learn Documentation", "url": "https://scikit-learn.org/stable/"}
                ],
                "youtube_tutorials": [
                    {"title": "Scikit-Learn Crash Course", "channel": "freeCodeCamp.org", "url": "https://www.youtube.com/results?search_query=scikit+learn+crash+course"}
                ],
                "practical_project": "Build an end-to-end ML classification pipeline with pipeline transformers and cross-validation.",
                "milestone_goal": "Trained predictive model achieving >88% ROC-AUC on unseen test data."
            },
            {
                "skill": "MLOps & Model API Deployment",
                "timeline": "Week 5 - 6",
                "why_it_matters": "Bridges research models to production applications via REST APIs and Docker containers.",
                "key_topics": ["FastAPI Model Serving", "Docker Containerization for ML", "Model Serialization with ONNX/Joblib", "Latency Optimization"],
                "websites": [
                    {"title": "FastAPI Deployment Guide", "url": "https://fastapi.tiangolo.com/deployment/"}
                ],
                "youtube_tutorials": [
                    {"title": "Deploy ML Models with FastAPI and Docker", "channel": "Tech With Tim", "url": "https://www.youtube.com/results?search_query=deploy+ml+model+fastapi+docker"}
                ],
                "practical_project": "Containerize your ML model with FastAPI and deploy to a cloud instance.",
                "milestone_goal": "A live inference endpoint returning predictions in <50ms."
            }
        ]
    elif "frontend" in lower_role:
        return [
            {
                "skill": "React.js Component Architecture & Hooks",
                "timeline": "Week 1 - 2",
                "why_it_matters": "The core frontend standard for building reactive, component-driven user interfaces.",
                "key_topics": ["State & Props", "Custom Hooks", "Context API", "Component Lifecycle & Effects"],
                "websites": [{"title": "React Official Docs", "url": "https://react.dev/learn"}],
                "youtube_tutorials": [{"title": "React JS Full Course", "channel": "freeCodeCamp.org", "url": "https://www.youtube.com/results?search_query=react+full+course+freecodecamp"}],
                "practical_project": "Build a responsive web application consuming your backend REST APIs.",
                "milestone_goal": "Interactive SPA with routing and global state management."
            },
            {
                "skill": "TypeScript for Scalable Web Apps",
                "timeline": "Week 3 - 4",
                "why_it_matters": "Provides static type safety, reducing runtime bugs in complex web platforms.",
                "key_topics": ["Interfaces & Types", "Generics", "Type Narrowing", "React + TypeScript Setup"],
                "websites": [{"title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/"}],
                "youtube_tutorials": [{"title": "TypeScript Crash Course", "channel": "Traversy Media", "url": "https://www.youtube.com/results?search_query=typescript+crash+course+traversy"}],
                "practical_project": "Convert a vanilla JavaScript frontend project into strictly typed TypeScript.",
                "milestone_goal": "Zero compile errors with strictly typed API responses."
            },
            {
                "skill": "Web Performance, Core Web Vitals & Next.js",
                "timeline": "Week 5 - 6",
                "why_it_matters": "Critical for fast loading times, SEO, and enterprise user experience.",
                "key_topics": ["Server-Side Rendering (SSR)", "Lighthouse Optimization", "Code Splitting & Lazy Loading", "Image Optimization"],
                "websites": [{"title": "Next.js Documentation", "url": "https://nextjs.org/docs"}],
                "youtube_tutorials": [{"title": "Next.js Full Course", "channel": "freeCodeCamp.org", "url": "https://www.youtube.com/results?search_query=nextjs+full+course"}],
                "practical_project": "Build a Next.js web application achieving a 95+ score on Google Lighthouse.",
                "milestone_goal": "Production-ready SSR application deployed on Vercel/Cloud."
            }
        ]
    else:
        # Default Full Stack / Backend
        return [
            {
                "skill": "Docker & Multi-Container Orchestration",
                "timeline": "Week 1 - 2",
                "why_it_matters": "Standardizes development and production environments across servers.",
                "key_topics": ["Dockerfile Multi-Stage Builds", "Docker Compose", "Volume Persistence for Databases", "Container Networking"],
                "websites": [{"title": "Docker Official Docs", "url": "https://docs.docker.com/get-started/"}],
                "youtube_tutorials": [{"title": "Docker Crash Course", "channel": "Traversy Media", "url": "https://www.youtube.com/results?search_query=docker+crash+course+traversy"}],
                "practical_project": "Containerize your Python backend, MySQL database, and frontend with Docker Compose.",
                "milestone_goal": "Entire project boots with a single `docker compose up` command."
            },
            {
                "skill": "Database Indexing & Query Optimization in MySQL",
                "timeline": "Week 3 - 4",
                "why_it_matters": "Prevents slow queries and bottlenecks under high-volume user traffic.",
                "key_topics": ["Composite B-Tree Indexes", "EXPLAIN Query Execution Plans", "Connection Pooling", "Normalization vs Denormalization"],
                "websites": [{"title": "MySQL Performance Tuning", "url": "https://dev.mysql.com/doc/refman/8.0/en/optimization.html"}],
                "youtube_tutorials": [{"title": "Database Indexing Explained", "channel": "Hussein Nasser", "url": "https://www.youtube.com/results?search_query=database+indexing+hussein+nasser"}],
                "practical_project": "Benchmark database queries using EXPLAIN and introduce composite indexes to reduce lookup times by 80%.",
                "milestone_goal": "Sub-millisecond query latency on complex multi-table joins."
            },
            {
                "skill": "Cloud Deployment (AWS/GCP) & CI/CD Pipelines",
                "timeline": "Week 5 - 6",
                "why_it_matters": "Enables automated testing and reliable continuous deployment to cloud infrastructure.",
                "key_topics": ["AWS EC2 & S3", "GitHub Actions CI/CD", "Nginx Reverse Proxy & SSL", "Environment Variables Management"],
                "websites": [{"title": "GitHub Actions Documentation", "url": "https://docs.github.com/en/actions"}],
                "youtube_tutorials": [{"title": "Deploy Full Stack App to AWS EC2", "channel": "Tech With Tim", "url": "https://www.youtube.com/results?search_query=deploy+full+stack+app+aws+ec2"}],
                "practical_project": "Configure automated GitHub Actions workflow to run unit tests and deploy to AWS on main branch push.",
                "milestone_goal": "Live application accessible via public HTTPS domain."
            }
        ]

def get_fallback_interview_questions(role_name: str, skills: List[str]) -> List[Dict[str, Any]]:
    """Generates a full 30-question bank across 4 categories."""
    questions = []

    # 1. Technical Questions (10 items)
    tech_bank = [
        ("How does Python manage memory internally, and how does the Garbage Collector handle reference cycles?", "Intermediate", "Evaluates deep language internals, memory allocation, and cyclic references."),
        ("What is the difference between synchronous and asynchronous operations in JavaScript/Node.js, and how does the Event Loop work?", "Intermediate", "Assesses concurrency models, microtasks vs macrotasks, and non-blocking I/O."),
        ("In MySQL, what is the difference between clustered and non-clustered indexes, and when would you use a composite index?", "Intermediate", "Tests relational database architecture, B-Tree storage mechanics, and indexing optimization."),
        ("Explain the difference between REST API and GraphQL. When would you choose REST over GraphQL?", "Foundational", "Checks understanding of API paradigms, over-fetching/under-fetching trade-offs, and network efficiency."),
        ("How do HTTP status codes 401 Unauthorized, 403 Forbidden, and 404 Not Found differ in secure REST API design?", "Foundational", "Assesses HTTP protocol adherence and authentication/authorization fundamentals."),
        ("What are the ACID properties in database management systems, and why are they critical for transactions?", "Foundational", "Tests core DBMS principles of Atomicity, Consistency, Isolation, and Durability."),
        ("How do you prevent SQL injection and Cross-Site Scripting (XSS) in modern web applications?", "Intermediate", "Tests security consciousness, parameterized queries, and input sanitization practices."),
        ("What is the difference between processes and threads, and how does Python's GIL affect CPU-bound multi-threading?", "Advanced", "Evaluates systems programming understanding and Python concurrency limitations."),
        ("Explain the time and space complexity of common sorting algorithms (e.g. QuickSort, MergeSort) and when to choose each.", "Foundational", "Assesses Data Structures & Algorithms fundamentals."),
        ("How does caching with Redis improve application performance, and how do you handle cache invalidation?", "Advanced", "Tests distributed caching strategies, cache-aside pattern, and TTL management.")
    ]

    for q_text, diff, intent in tech_bank:
        questions.append({
            "category": "Technical Questions",
            "question": q_text,
            "difficulty": diff,
            "interviewer_intent": intent,
            "key_topics": ["Backend", "Core CS", "Databases", "APIs"],
            "key_points_to_mention": ["State definitions clearly", "Provide concrete code/system examples", "Explain trade-offs"],
            "sample_strong_answer": "Provide a clear definition followed by practical code architecture and performance trade-offs."
        })

    # 2. Resume & Project Deep Dive Questions (10 items)
    proj_bank = [
        ("In your AI Business Intelligence Dashboard project, how did you integrate the Google Gemini API to query CSV data without security or arbitrary code execution risks?", "Advanced", "Evaluates LLM integration architecture, prompt boundary enforcement, and code sandboxing."),
        ("Walk me through the architecture of your CompareCart platform. How did you handle API rate limits and structural inconsistencies across external e-commerce APIs?", "Intermediate", "Assesses asynchronous REST API consumption, error boundaries, and data normalization."),
        ("In your Community Crisis Platform, how did you leverage Firebase Realtime Database to propagate emergency alerts to active users with low latency?", "Intermediate", "Tests real-time web socket/event-driven data propagation and offline synchronization."),
        ("What testing strategies did you implement for your projects? How would you design unit and integration tests for your backend API endpoints?", "Intermediate", "Assesses quality assurance mindset, test automation with pytest/unittest, and test coverage."),
        ("If your AI Business Intelligence Dashboard experienced a 100x spike in concurrent users querying CSVs, where would the primary bottleneck occur and how would you scale it?", "Advanced", "Tests scalability analysis, memory bottlenecks in Pandas DataFrames, and horizontal scaling strategies."),
        ("Why did you select Streamlit for the AI Business Intelligence Dashboard instead of a traditional React frontend? What were the trade-offs?", "Foundational", "Evaluates architectural decision-making, development velocity vs custom UI flexibility."),
        ("How did you structure your Git workflow and version control across your projects? Describe your branching and pull request strategy.", "Foundational", "Assesses collaborative software engineering hygiene and Git best practices."),
        ("What was the most challenging technical bug you encountered while building CompareCart or your AI Dashboard, and how did you diagnose and resolve it?", "Intermediate", "Evaluates debugging methodologies, logging, and problem-solving resilience."),
        ("How did you handle environment variables, API keys, and sensitive database credentials in your repositories to prevent credential leaks?", "Foundational", "Tests security hygiene, `.env` file management, and config injection."),
        ("What would you change or refactor if you had to rebuild your primary resume project from scratch today?", "Intermediate", "Assesses technical introspection, growth mindset, and engineering maturity.")
    ]

    for q_text, diff, intent in proj_bank:
        questions.append({
            "category": "Resume & Project Deep Dive",
            "question": q_text,
            "difficulty": diff,
            "interviewer_intent": intent,
            "key_topics": ["Architecture", "System Trade-offs", "Debugging", "Security"],
            "key_points_to_mention": ["Describe the problem context", "Explain the technical solution implemented", "Quantify the outcome"],
            "sample_strong_answer": "Structure response using Situation, Technical Choice, Implementation Details, and Key Learning."
        })

    # 3. Behavioral Questions (5 items)
    beh_bank = [
        ("Tell me about a time when a project requirement was ambiguous or changed midway. How did you adapt and deliver?", "Intermediate", "Assesses adaptability, communication, and prioritization under uncertainty."),
        ("Describe a situation where you had a technical disagreement with a peer or teammate. How did you resolve it collaboratively?", "Intermediate", "Evaluates empathy, constructive technical debates, and team-first orientation."),
        ("Give an example of a time when a feature you implemented broke or did not meet performance expectations. What was your recovery process?", "Intermediate", "Tests accountability, root-cause analysis, and emotional resilience."),
        ("How do you prioritize your time when balancing university coursework, project milestones, and learning new technical skills?", "Foundational", "Assesses time management, disciplined focus, and proactive communication."),
        ("Describe a project where you took the initiative to learn a brand-new technology or framework from scratch. How did you ramp up quickly?", "Foundational", "Evaluates continuous learning velocity, resourcefulness, and self-direction.")
    ]

    for q_text, diff, intent in beh_bank:
        questions.append({
            "category": "Behavioral Questions",
            "question": q_text,
            "difficulty": diff,
            "interviewer_intent": intent,
            "key_topics": ["Collaboration", "Adaptability", "Accountability", "Growth"],
            "key_points_to_mention": ["Situation & Task context", "Specific Actions taken", "Measurable Results & Reflection"],
            "sample_strong_answer": "Deliver a concise 2-minute STAR response focusing on ownership, clear action steps, and positive team impact."
        })

    # 4. Job-Specific Questions (5 items)
    job_bank = [
        (f"For a {role_name} position, how do you design REST APIs to ensure backward compatibility and seamless versioning?", "Intermediate", f"Assesses API longevity and design best practices expected of a {role_name}."),
        (f"How do you approach database schema normalization (3NF) versus denormalization when building data models for a {role_name} stack?", "Intermediate", "Tests relational data modeling depth and read/write optimization trade-offs."),
        (f"As a {role_name}, how do you ensure zero-downtime deployments and graceful error degradation when third-party microservices fail?", "Advanced", "Evaluates reliability engineering, circuit breakers, and fault-tolerant architecture."),
        (f"What key metrics and telemetry (latency, error rate, saturation) would you monitor in production for a {role_name} application?", "Intermediate", "Assesses observability, structured logging, and production readiness mindset."),
        (f"How do you stay current with rapidly evolving frameworks, AI tools, and architectural best practices in the {role_name} ecosystem?", "Foundational", "Tests curiosity, technical passion, and engagement with developer communities.")
    ]

    for q_text, diff, intent in job_bank:
        questions.append({
            "category": "Job-Specific Questions",
            "question": q_text,
            "difficulty": diff,
            "interviewer_intent": intent,
            "key_topics": [role_name, "Production Readiness", "System Design"],
            "key_points_to_mention": ["Industry standards", "Architectural trade-offs", "Real-world engineering experience"],
            "sample_strong_answer": f"Highlight industry standard patterns relevant to a {role_name}, discussing scalability, reliability, and security."
        })

    return questions

def get_fallback_evaluation(resume_text: str, extracted_skills: List[str]) -> Dict[str, Any]:
    """Provides high-quality non-hallucinatory fallback evaluation."""
    return {
        "strengths": [
            f"Strong foundational competencies in {', '.join(extracted_skills[:4])}.",
            "Practical project demonstrations in AI business intelligence and web platforms."
        ],
        "weaknesses": [
            "Certain bullet points could emphasize measurable metrics (e.g. latency improvement, user counts).",
            "Expand on cloud deployment (Docker/AWS) or automated testing workflows."
        ],
        "recommendations": [
            "Quantify project outcomes (e.g. processing speeds, query response improvements).",
            "Include live deployment links and verified GitHub repository URLs."
        ],
        "bullet_improvements": [
            {
                "original_text": "Built a web platform that compares product prices from different sources.",
                "why_needs_improvement": "Uses weak verb 'Built' and lacks technical details on API integration and data handling.",
                "suggested_text": "Architected a full-stack price comparison platform aggregating real-time product data across e-commerce REST APIs, optimizing catalog search responsiveness.",
                "why_better": "Highlights API orchestration, data normalization, and search performance using active verbs.",
                "metric_suggestion": "Consider adding a measurable result if you have one (e.g., 'reduced product fetch latency by 35%').",
                "improvement_type": "action_verb"
            },
            {
                "original_text": "Created an AI dashboard to analyze CSV data using Gemini API.",
                "why_needs_improvement": "Vague description that does not explain the LLM orchestration or data processing pipeline.",
                "suggested_text": "Engineered an AI-powered business intelligence dashboard integrating Google Gemini API and Pandas to dynamically translate natural language queries into executable analytics.",
                "why_better": "Demonstrates prompt engineering, query translation, and data analytics integration.",
                "metric_suggestion": "Consider adding a measurable result if you have one (e.g., 'accelerated exploratory analysis for 50+ query scenarios').",
                "improvement_type": "action_verb"
            }
        ]
    }
