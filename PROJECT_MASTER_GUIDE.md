# ⚡ ResumeAI — Master Project Architecture, Tech Stack & Viva Guide

---

## 📌 Executive Summary
**ResumeAI** is an enterprise-grade, AI-powered Resume Analyzer, Applicant Tracking System (ATS) Compatibility Scorer, and Semantic Job Matching platform. Built as a comprehensive major project, it bridges the gap between raw candidate resumes and modern recruiter recruitment algorithms using Natural Language Processing (NLP), Dense Vector Semantic Matching (Sentence Transformers), and Generative AI (Google Gemini 2.5 Flash).

---

## 🛠️ 1. Complete Technology Stack

| Layer | Technologies Used | Purpose & Rationale |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Chart.js | Built without heavy JavaScript frameworks (React/Vue/Angular) to achieve near-instant initial page loads, zero npm build step dependency in production, and seamless rendering on any device or mobile screen. |
| **Backend Framework** | Python 3.10+, FastAPI, Uvicorn | High-performance asynchronous ASGI web framework. Significantly faster than Flask and lighter than Django, featuring native OpenAPI/Swagger documentation (`/docs`) and async request concurrency. |
| **Data Validation** | Pydantic v2, Pydantic-Settings | Strict request/response data typing, automated schema validation, and safe environment variable parsing. |
| **Database & ORM** | SQLite & MySQL 8.0, SQLAlchemy 2.0 | Normalized relational schema. The engine features an automatic resilient fallback: it attempts MySQL first; if unavailable, it gracefully defaults to zero-config SQLite. |
| **NLP & Extraction** | spaCy Canonical Taxonomy, Regex Boundary Matchers | Hierarchical taxonomy engine mapping 500+ technical and soft skills with bidirectional alias resolution (e.g., "JS", "ES6", "Vanilla JS" $\rightarrow$ "JavaScript"). |
| **Semantic Matching** | Sentence Transformers (`all-MiniLM-L6-v2`), Scikit-learn | Generates 384-dimensional dense semantic vector embeddings to calculate true cosine similarity between candidate experience and job descriptions beyond exact keyword spelling. Includes TF-IDF fallback. |
| **Generative AI** | Google Gemini API (`gemini-2.5-flash`) | Contextual qualitative bullet-point refinement (turning weak passive bullets into quantified active achievements) and personalized 7-day skill-gap learning roadmaps. |
| **Document Parsing** | `pdfplumber`, `pypdf`, `python-docx` | Multi-engine document text and table extraction supporting both modern vector PDFs and Microsoft Word (`.docx`) files. |
| **Security & Auth** | JWT (JSON Web Tokens), Native Bcrypt (12 rounds), Magic Byte Verification | Stateless OAuth2 token authentication, industry-standard salted password hashing, and MIME/magic-byte validation to prevent malicious file execution. |
| **DevOps & Cloud** | Render, Docker, GitHub CI/CD | Production containerization and automated Git-push cloud deployment with CPU-optimized PyTorch wheels. |

---

## 📂 2. File-by-File Purpose & Directory Structure

```text
student_analysis/
├── PROJECT_MASTER_GUIDE.md         # Master architectural reference and viva guide
├── README.md                       # GitHub documentation & quickstart
├── requirements.txt                # Production Python dependencies (CPU-optimized)
├── Procfile                        # Cloud process manager start command
├── render.yaml                     # Render infrastructure blueprint
├── Dockerfile                      # Production container build recipe
├── .dockerignore                   # Docker build exclusions
├── .gitignore                      # Protects secrets (.env) and databases from leaking
├── .env.example                    # Template for environment configuration
├── run.bat                         # 1-Click local startup script for Windows
│
├── database/
│   └── schema.sql                  # Production MySQL DDL schema (tables, foreign keys, cascades)
│
├── backend/
│   ├── main.py                     # FastAPI application factory, CORS setup & static mounting
│   ├── config.py                   # Pydantic BaseSettings loading environment configurations
│   ├── database.py                 # Resilient SQLAlchemy engine & session dependency
│   │
│   ├── models/                     # SQLAlchemy Relational ORM Models
│   │   ├── __init__.py             # Model package exports
│   │   ├── user.py                 # User authentication & credential entities
│   │   ├── resume.py               # Resume metadata, file paths, raw text & parsed JSON
│   │   ├── skill.py                # Skills taxonomy & resume-skill relational mappings
│   │   ├── job.py                  # Job descriptions & semantic matching records
│   │   └── analysis.py             # ATS scores, category metrics & bullet improvements
│   │
│   ├── schemas/                    # Pydantic Request & Response Data Contracts
│   │   ├── __init__.py             # Schema exports
│   │   ├── auth.py                 # User registration, login, and JWT token models
│   │   ├── resume.py               # Parsed resume entities (Contact, Work, Education, Skills)
│   │   ├── job.py                  # Job description input & match response models
│   │   ├── analysis.py             # Score breakdown, metrics & AI recommendations
│   │   └── common.py               # Standardized API response wrapper: APIResponse[T]
│   │
│   ├── routes/                     # REST API Endpoints
│   │   ├── __init__.py             # Router exports
│   │   ├── auth.py                 # /api/auth: Register, login, session profile
│   │   ├── resume.py               # /api/resume: Upload file, text paste, user resumes
│   │   ├── analysis.py             # /api/analysis: Run ATS evaluation & bullet rewrite
│   │   ├── job.py                  # /api/job: Submit JD & semantic match execution
│   │   └── demo.py                 # /api/demo: Instant pre-loaded mock analyses for demoing
│   │
│   ├── nlp/                        # Document Extraction & NLP Engine
│   │   ├── parser.py               # Multi-engine document text extraction (PDF & DOCX)
│   │   ├── section_extractor.py    # Header recognition regex & contact info extractor
│   │   ├── skill_taxonomy.py       # 500+ skill taxonomy database & canonical alias mapping
│   │   ├── skill_extractor.py      # Regex boundary-protected taxonomy skill matcher
│   │   └── semantic_matcher.py     # SentenceTransformers cosine similarity & gap categorizer
│   │
│   ├── ai/                         # Generative AI Services
│   │   └── gemini_client.py        # Google Gemini 2.5 Flash service (bullet rewrites & roadmaps)
│   │
│   ├── services/                   # Business Logic & Math Models
│   │   └── scoring_service.py      # Deterministic 4-pillar ATS scoring engine
│   │
│   └── utils/                      # Helper Utilities
│       ├── __init__.py             # Utility package exports
│       ├── security.py             # Password hashing (bcrypt) & JWT token verification
│       └── validators.py           # Magic-byte file validation & upload constraints
│
├── frontend/                       # Zero-Framework SaaS User Interface
│   ├── index.html                  # Landing page with hero section & feature cards
│   ├── analyzer.html               # Dual-mode input (file drag-and-drop & job description)
│   ├── results.html                # Interactive ATS score dashboard, radar & bar charts
│   ├── dashboard.html              # Historical analyses, comparisons & score trends
│   ├── login.html                  # User sign-in interface
│   ├── register.html               # User registration interface
│   │
│   ├── css/                        # CSS3 Modular Styling System
│   │   ├── style.css               # Global variables, typography, dark/light theme, navbar
│   │   ├── components.css          # Buttons, form controls, cards, badges, modal dialogs
│   │   ├── analyzer.css            # Upload dropzone & job description input styling
│   │   ├── results.css             # Radial score gauges, skill tag badges, roadmap grid
│   │   ├── dashboard.css           # Comparison tables & history cards
│   │   └── auth.css                # Authentication forms & login card styling
│   │
│   ├── js/                         # Vanilla JavaScript Client Layer
│   │   ├── api.js                  # Dynamic API base URL resolver & unified fetch wrapper
│   │   ├── app.js                  # Global theme toggle, auth state & session handling
│   │   ├── auth.js                 # Login/Registration form submission & token storage
│   │   ├── upload.js               # File drag-and-drop, validation & analyze trigger
│   │   ├── results.js              # Results rendering, skill gaps, roadmaps & PDF export
│   │   └── charts.js               # Chart.js initialization (Radar score & Bar breakdowns)
│   │
│   └── assets/                     # Demo Assets
│       └── sample_resume.docx      # Test resume document for evaluation & viva
│
└── uploads/
    └── .gitkeep                    # Target folder for user uploaded resumes
```

---

## 🏛️ 3. Overall System Architecture & Workflow

### High-Level Architecture Diagram

```
+-------------------------------------------------------------------------------+
|                                CLIENT LAYER                                   |
|   HTML5 / CSS3 Glassmorphism UI (Desktop, Tablet, Mobile Responsive)          |
|   Vanilla JS Modules (api.js, upload.js, results.js, charts.js)               |
+---------------------------------------+---------------------------------------+
                                        |  REST HTTPS (JSON / FormData)
                                        v
+-------------------------------------------------------------------------------+
|                            FASTAPI BACKEND GATEWAY                            |
|   Uvicorn ASGI Server | CORS Middleware | Static Files Mount                  |
|   OAuth2 Bearer JWT Authentication | Magic-Byte File Validation               |
+-------------------+-----------------------------------+-----------------------+
                    |                                   |
                    v                                   v
+--------------------------------------+   +------------------------------------+
|         NLP PARSING PIPELINE         |   |         AI & SCORING LAYER         |
|  1. pdfplumber / python-docx Text    |   |  1. SentenceTransformer Vectors    |
|  2. Regex Section Classifier         |   |  2. Cosine Similarity Matching     |
|  3. Contact Regex (Email/Phone/URLs) |   |  3. Multi-Pillar ATS Scorer        |
|  4. Canonical Taxonomy Extractor     |   |  4. Google Gemini 2.5 Flash        |
+-------------------+------------------+   +-----------------+------------------+
                    |                                        |
                    +-------------------+--------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                               PERSISTENCE LAYER                               |
|   SQLAlchemy 2.0 ORM Engine                                                   |
|   Dual Mode: Primary MySQL 8.0 <---> Resilient Auto-Fallback SQLite           |
+-------------------------------------------------------------------------------+
```

---

## ⚙️ 4. The 7-Stage Resume Processing Pipeline

```
[Uploaded File] 
       │
       ▼
1. Validation ──────► Magic-byte check, size limit (10MB), extension whitelist (.pdf, .docx)
       │
       ▼
2. Text Extraction ─► pdfplumber / pypdf / python-docx stream parsing
       │
       ▼
3. Section Parsing ─► Regex boundary classification (Education, Experience, Skills, Projects)
       │
       ▼
4. Taxonomy Match ──► 500+ canonical skills matched; aliases normalized to standard names
       │
       ▼
5. Semantic Match ──► 384-dimensional dense vectors compare resume text against Job Description
       │
       ▼
6. ATS Scoring ─────► 4-pillar deterministic score calculation (0 - 100 scale)
       │
       ▼
7. Generative AI ───► Gemini 2.5 Flash generates bullet rewrites and 7-day skill gap roadmap
```

---

## 🧮 5. Core Algorithms & Mathematical Formulations

### 1. ATS Composite Compatibility Score
The ATS Score is calculated deterministically across 4 weighted pillars:

$$\text{ATS Score} = (0.25 \times S_{\text{sections}}) + (0.40 \times S_{\text{skills}}) + (0.15 \times S_{\text{readability}}) + (0.20 \times S_{\text{formatting}})$$

- **Section Completeness ($S_{\text{sections}}$)**: Evaluates presence of 5 critical sections: Contact Info, Work Experience, Education, Skills, and Projects/Summary (20 points each).
- **Skill Alignment ($S_{\text{skills}}$)**: Ratio of required and preferred skills found in the resume against the target role.
- **Readability ($S_{\text{readability}}$)**: Word count density, average sentence length, and bullet-point structure.
- **Formatting Hygiene ($S_{\text{formatting}}$)**: Absence of parsing errors, tables that break ATS scanners, and presence of standard section header names.

### 2. Semantic Embedding Cosine Similarity
To measure true semantic alignment between the candidate's experience and the job description, text chunks are converted to 384-dimensional dense vectors using `all-MiniLM-L6-v2`:

$$\text{Similarity}(\mathbf{u}, \mathbf{v}) = \cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^{n} u_i v_i}{\sqrt{\sum_{i=1}^{n} u_i^2} \sqrt{\sum_{i=1}^{n} v_i^2}}$$

- **Why this beats keyword matching**: If a job description asks for *"container orchestration"*, and the resume mentions *"Docker and Kubernetes cluster deployment"*, traditional keyword matching gives 0%. Semantic cosine similarity scores **88%+** because the dense vectors occupy nearby points in vector space.

### 3. Skill Gap Categorization Matrix
Skills extracted from the Job Description are cross-checked and sorted into three actionable priority tiers:
- **High Priority (Immediate Blocker)**: Core skills required by the JD but completely absent from the resume.
- **Medium Priority (Transferable / Partial)**: Required skills where the candidate possesses a known transferable counterpart (e.g., candidate has *PostgreSQL*, but JD asks for *MySQL*).
- **Low Priority (Bonus)**: Preferred or soft skills that enhance competitiveness but are not strict prerequisites.

---

## 🎯 6. Key Viva & Project Defense Questions

### Q1: Why did you use FastAPI instead of Flask or Django?
* **Answer**: FastAPI is built on modern ASGI standards (`asyncio` and `uvicorn`), allowing concurrent non-blocking handling of long-running operations like document parsing and AI calls. It provides automatic schema validation with Pydantic and automatically generates interactive Swagger documentation at `/docs`. Flask is WSGI (synchronous by default), and Django introduces excessive boilerplate not required for a microservice API architecture.

### Q2: How does the system prevent Generative AI hallucinations?
* **Answer**: The parsing, skill extraction, ATS scoring, and gap matching are completely **deterministic**—calculated using regex taxonomy and mathematical cosine similarity, **not** LLM prompts. The Gemini API is only invoked for qualitative enrichment: rewriting existing bullet points using strict prompt constraints (forbidding the addition of fabricated metrics or fake employers) and recommending public learning resources.

### Q3: How is the database resilient between development and production?
* **Answer**: In [`backend/database.py`](backend/database.py), the `create_resilient_engine()` function checks the `DATABASE_URL`. If configured for MySQL, it tests the connection. If the external MySQL server is offline or not installed, it automatically and gracefully falls back to local SQLite without crashing the server.

### Q4: How is user security maintained?
* **Answer**:
  1. Passwords are never stored in plain text; they are hashed using **Bcrypt with 12 salt rounds**.
  2. Authentication uses **OAuth2 Password Bearer flow** with signed **JWT (HS256)** tokens containing expiration timestamps.
  3. File uploads undergo **magic-byte inspection** (validating true file headers rather than trusting the user-provided file extension) to block malicious scripts disguised as PDFs.
