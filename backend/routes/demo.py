from datetime import datetime
from fastapi import APIRouter
from backend.schemas.common import APIResponse
from backend.schemas.analysis import ResumeAnalysisOut, ATSCheckItem, BulletImprovementSchema
from backend.schemas.job import JobMatchOut, SkillGapPriority, LearningRoadmapStep

router = APIRouter(prefix="/demo", tags=["Demo Mode"])

@router.get("/data")
def get_demo_dataset():
    """Returns sample resume and job description text for quick demonstration."""
    sample_resume = """Alex Morgan
alex.morgan@email.com | +1 (555) 234-5678 | San Francisco, CA
LinkedIn: linkedin.com/in/alexmorgan-dev | GitHub: github.com/alexmorgan-code

SUMMARY
Results-driven Full Stack Software Engineer with 3+ years of experience designing and scaling web applications, microservices, and AI-assisted tools. Proficient in Python, JavaScript, FastAPI, React, and PostgreSQL.

SKILLS
- Programming: Python, JavaScript, TypeScript, SQL, Bash
- Frameworks & Libraries: FastAPI, Flask, React.js, Node.js, Express, Redux, SQLAlchemy
- Databases: PostgreSQL, MySQL, Redis, MongoDB
- Cloud & DevOps: Docker, AWS (EC2, S3), Git, GitHub Actions, Linux, Nginx
- Concepts: RESTful APIs, Microservices, CI/CD, Agile/Scrum, Object-Oriented Programming

EXPERIENCE
Software Engineer | NexaTech Solutions | June 2022 - Present
- Built and maintained 12+ RESTful APIs using Python FastAPI and PostgreSQL, serving 150,000+ monthly active users with 99.9% uptime.
- Optimized database queries and Redis caching layers, reducing average endpoint latency from 450ms to 95ms.
- Containerized legacy backend services with Docker and created automated CI/CD deployment pipelines using GitHub Actions.
- Collaborated with frontend engineers to integrate responsive React components with state management.

Junior Developer | CloudSphere Labs | Jan 2021 - May 2022
- Developed responsive web interfaces using HTML5, CSS3, and JavaScript for client dashboards.
- Integrated third-party payment gateways and authentication using JWT and OAuth2.
- Resolved 85+ production bug tickets and improved test coverage by 35% using Pytest.

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2017 - 2021 | GPA: 3.8/4.0

PROJECTS
AI Document Summarizer (Python, FastAPI, Gemini API, Docker)
- Developed an automated PDF extraction and summarization web application with real-time streaming responses.
- Implemented spaCy NLP pipelines for key concept tagging and entity recognition.

E-Commerce Microservices Platform (Node.js, Express, MongoDB, Redis)
- Architected an event-driven e-commerce backend handling product catalog, inventory, and order processing.
"""

    sample_job = """Senior Full Stack Engineer (Python / Cloud / AI)
InnovateAI Corp - San Francisco, CA (Hybrid)

About the Role:
We are looking for an exceptional Full Stack Engineer to lead the design and implementation of our next-generation AI workflows. You will build scalable microservices, integrate LLM pipelines, and deploy resilient cloud applications.

Key Responsibilities:
- Design, build, and deploy high-performance REST APIs and microservices using Python (FastAPI / Django).
- Integrate AI / LLM models and vector databases for semantic retrieval and intelligent document processing.
- Deploy and monitor applications on AWS and Kubernetes with automated CI/CD pipelines.
- Collaborate with product designers and frontend teams to build seamless web interfaces.

Required Qualifications:
- 3+ years of experience with Python, FastAPI, and relational databases (PostgreSQL/MySQL).
- Strong experience with Docker, container orchestration, and CI/CD pipelines.
- Hands-on experience with RESTful API design, microservices, and caching (Redis).
- Proficiency with modern frontend technologies (JavaScript/TypeScript, React/HTML5).
- Solid knowledge of Git version control and Linux environments.

Preferred Qualifications:
- Experience with Kubernetes (K8s) and AWS cloud infrastructure.
- Familiarity with NLP, Sentence Transformers, and Generative AI APIs (Gemini/OpenAI).
- Experience with Vector Databases and Semantic Search.
"""

    return APIResponse(
        success=True,
        message="Demo payload retrieved successfully.",
        data={
            "resume_text": sample_resume,
            "job_text": sample_job,
            "job_title": "Senior Full Stack Engineer",
            "company": "InnovateAI Corp"
        }
    )

@router.get("/analysis", response_model=APIResponse[ResumeAnalysisOut])
def get_demo_analysis():
    """Returns a full pre-computed AI & ATS analysis report for demonstration."""
    demo_analysis = ResumeAnalysisOut(
        id=999,
        resume_id=1,
        overall_score=87.5,
        ats_score=92.0,
        quality_score=85.0,
        skills_score=89.0,
        readability_score=94.0,
        formatting_score=90.0,
        section_breakdown={
            "contact_info": 100.0,
            "summary": 90.0,
            "experience": 88.0,
            "education": 95.0,
            "skills": 90.0,
            "projects": 82.0
        },
        ats_checks=[
            ATSCheckItem(
                check="Standard Section Headings",
                status="PASS",
                score=100.0,
                message="All industry-standard headings (Summary, Experience, Skills, Education, Projects) are clearly identified.",
                recommendation=None
            ),
            ATSCheckItem(
                check="Contact Information Completeness",
                status="PASS",
                score=100.0,
                message="Full name, email, phone number, location, LinkedIn, and GitHub links are all present.",
                recommendation=None
            ),
            ATSCheckItem(
                check="Quantifiable Metrics in Experience",
                status="PASS",
                score=90.0,
                message="Strong usage of percentages, latency drops (450ms to 95ms), and active users (150,000+).",
                recommendation=None
            ),
            ATSCheckItem(
                check="Formatting & Parseability",
                status="PASS",
                score=95.0,
                message="Clean single-column layout without tables or unreadable icons. ATS scanners will parse with 100% fidelity.",
                recommendation=None
            ),
            ATSCheckItem(
                check="Action Verb Variety",
                status="PASS",
                score=85.0,
                message="Used high-impact verbs: Built, Maintained, Optimized, Containerized, Architected.",
                recommendation="Replace passive verbs in junior developer section with more proactive phrasing."
            )
        ],
        strengths=[
            "Excellent quantifiable achievements (e.g. 150k+ users, 99.9% uptime, latency reduced from 450ms to 95ms).",
            "Clear technical skill taxonomy categorized into Programming, Frameworks, Databases, and DevOps.",
            "Strong single-column layout optimized for ATS scanning engines.",
            "Complete contact information including verified GitHub and LinkedIn profiles."
        ],
        weaknesses=[
            "Project section lacks detailed production deployment metrics or user reach figures.",
            "Could benefit from highlighting unit test frameworks (e.g., PyTest, Jest) more prominently in the skills list."
        ],
        recommendations=[
            "Add measurable outcomes to the 'AI Document Summarizer' project (e.g. processing speed or documents handled).",
            "Highlight experience with cloud orchestration (Kubernetes) if you have any exposure.",
            "Ensure certifications section is added if you hold AWS or Python certifications."
        ],
        project_feedback=[
            {
                "project": "AI Document Summarizer",
                "score": 85,
                "feedback": "Strong project showing Gemini API & spaCy NLP integration. Add quantitative benchmark on document processing throughput."
            },
            {
                "project": "E-Commerce Microservices Platform",
                "score": 88,
                "feedback": "Good architecture demonstration with microservices and Redis caching."
            }
        ],
        experience_feedback=[
            {
                "company": "NexaTech Solutions",
                "score": 92,
                "feedback": "Outstanding bullet points with precise metrics (150,000+ users, 95ms latency, 99.9% uptime)."
            }
        ],
        bullet_improvements=[
            BulletImprovementSchema(
                original_text="Developed responsive web interfaces using HTML5, CSS3, and JavaScript for client dashboards.",
                suggested_text="Engineered responsive client dashboards utilizing HTML5, CSS3, and modern JavaScript, improving page load responsiveness across desktop and mobile devices.",
                reasoning="Replaces common verb 'Developed' with 'Engineered' and emphasizes cross-device performance impact.",
                improvement_type="action_verb"
            ),
            BulletImprovementSchema(
                original_text="Integrated third-party payment gateways and authentication using JWT and OAuth2.",
                suggested_text="Architected secure authentication workflows utilizing JWT and OAuth2 alongside third-party payment gateway integrations.",
                reasoning="Enhances technical precision and leadership terminology while preserving factual integrity.",
                improvement_type="clarity"
            )
        ],
        created_at=datetime.utcnow()
    )
    return APIResponse(
        success=True,
        message="Demo analysis report loaded successfully.",
        data=demo_analysis
    )

@router.get("/match", response_model=APIResponse[JobMatchOut])
def get_demo_match():
    """Returns a full pre-computed semantic job match and skill gap report for demonstration."""
    demo_match = JobMatchOut(
        id=999,
        resume_id=1,
        job_description_id=1,
        overall_match_percentage=84.5,
        semantic_similarity_score=86.2,
        skill_match_score=82.0,
        experience_relevance_score=88.0,
        matching_skills=[
            "Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs",
            "Redis", "Microservices", "JavaScript", "React.js", "Git",
            "Linux", "CI/CD", "GitHub Actions", "HTML5", "CSS3"
        ],
        missing_skills=[
            "Kubernetes", "Vector Databases"
        ],
        partial_skills=[
            "AWS (EC2, S3 present, broader cloud deployment requested)",
            "NLP & Semantic Search (spaCy present, Sentence Transformers / Vector DBs preferred)"
        ],
        skill_gap_priority=SkillGapPriority(
            high=[
                {
                    "skill": "Kubernetes (K8s)",
                    "reason": "Required for microservice container orchestration in production cluster environments."
                }
            ],
            medium=[
                {
                    "skill": "Vector Databases (e.g., ChromaDB, Pinecone)",
                    "reason": "Crucial for production LLM embedding storage and semantic retrieval workflows."
                }
            ],
            low=[
                {
                    "skill": "Advanced AWS Cloud Architecture",
                    "reason": "Candidate already has foundational EC2/S3 experience; deeper IAM/EKS knowledge would solidify match."
                }
            ]
        ),
        learning_roadmap=[
            LearningRoadmapStep(
                skill="Kubernetes Container Orchestration",
                timeline="Week 1 - Week 2",
                resources=[
                    "Kubernetes Documentation (Pods, Deployments, Services)",
                    "Minikube / Kind local cluster setup guide"
                ],
                practical_project="Deploy the FastAPI microservices backend onto a local Minikube cluster with horizontal pod autoscaling."
            ),
            LearningRoadmapStep(
                skill="Vector Databases & Semantic Search",
                timeline="Week 3",
                resources=[
                    "ChromaDB / FAISS Quickstart guides",
                    "Sentence Transformers embedding generation documentation"
                ],
                practical_project="Build a vector search index over PDF document chunks to perform semantic QA."
            )
        ],
        created_at=datetime.utcnow()
    )
    return APIResponse(
        success=True,
        message="Demo job match report loaded successfully.",
        data=demo_match
    )
