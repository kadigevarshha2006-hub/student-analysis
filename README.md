# ⚡ ResumeAI - AI-Powered Resume Analyzer & Job Matching System

An enterprise-grade, AI-powered Resume Analyzer, ATS Compatibility Scorer, and Semantic Job Matcher built as a major college project.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (Zero-Framework SaaS Design System), Chart.js |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0 |
| **NLP & ML** | spaCy (`en_core_web_sm`), Sentence Transformers (`all-MiniLM-L6-v2`), scikit-learn |
| **Generative AI** | Google Gemini API (`gemini-2.5-flash`) for qualitative bullet point rewrites & learning roadmaps |
| **Database** | MySQL 8.0+ / SQLite (SQLAlchemy ORM with DDL in `database/schema.sql`) |
| **Document Parsing** | `pdfplumber`, `pypdf`, `python-docx` |
| **Security** | JWT (OAuth2 Bearer Tokens), Native bcrypt password hashing, magic byte file validation |

---

## 🏛️ System Architecture

![ResumeAI Architecture](frontend/assets/system_architecture.png)

---

## 🗄️ Database Architecture

The system features a normalized schema with indexes, relationships, and cascade behaviors:

- `users`: User profiles, credentials, timestamps.
- `resumes`: Uploaded files, raw extracted text, parsed structured JSON.
- `skills_master`: Extensible master taxonomy containing 500+ skills with aliases.
- `resume_skills`: Resume-specific extracted skills with confidence ratings and categories.
- `resume_analysis`: ATS scores, quality scores, readability scores, and AI recommendations.
- `job_descriptions`: Target job descriptions and extracted required/preferred skills.
- `job_matches`: Cosine semantic similarity, matching/missing skills, priority gap categorizer, and learning roadmap.
- `bullet_improvements`: Non-hallucinatory bullet point enhancements.

The complete MySQL DDL script is located at [`database/schema.sql`](database/schema.sql).

---

## 📂 Project Structure

```text
student_analysis/
├── database/
│   └── schema.sql                  # MySQL DDL Schema
├── backend/
│   ├── .env.example                # Environment template
│   ├── .env                        # Local configuration
│   ├── requirements.txt            # Python dependencies
│   ├── main.py                     # FastAPI entry point & CORS
│   ├── config.py                   # Pydantic BaseSettings
│   ├── database.py                 # SQLAlchemy connection & init
│   ├── models/                     # SQLAlchemy ORM Models
│   ├── schemas/                    # Pydantic Request/Response Models
│   ├── routes/                     # API Route Endpoints
│   ├── utils/                      # Password hashing & file validators
│   ├── nlp/                        # Document parsing & spaCy extractor (Phases 3-6)
│   ├── ai/                         # Gemini generative AI service (Phase 7)
│   └── services/                   # Business logic
├── frontend/
│   ├── index.html                  # SaaS Landing Page
│   ├── login.html                  # User Login
│   ├── register.html               # User Registration
│   ├── analyzer.html               # Resume & JD input
│   ├── results.html                # Interactive Analysis Dashboard
│   ├── dashboard.html              # History & Comparison
│   ├── css/                        # CSS3 styling system & dark/light theme
│   ├── js/                         # Vanilla JS modular scripts & API client
│   └── assets/                     # Icons & sample demo resumes
└── README.md
```

---

## 🚀 How to Run the Project

### 1. Backend Setup

```bash
# Navigate to the project root
cd student_analysis

# Activate Python Virtual Environment
# Windows PowerShell:
.\backend\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment (`backend/.env`)

```env
PORT=8000
HOST=0.0.0.0
SECRET_KEY=resume_ai_jwt_super_secret_key_college_major_project_2026_secure
DATABASE_URL=sqlite:///./resume_ai.db
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Note for MySQL**: To connect to a local MySQL instance, set:
> `DATABASE_URL=mysql+pymysql://root:password@localhost:3306/resume_ai_db`

### 3. Start the Server

```bash
uvicorn backend.main:app --reload --port 8000
```

- **Interactive API Documentation (Swagger)**: `http://127.0.0.1:8000/docs`
- **Frontend SaaS Application**: `http://127.0.0.1:8000`

---

## 🗓️ Multi-Phase Roadmap

- [x] **Phase 1**: Architecture, Database Schema, FastAPI Core, Security & Frontend Base Structure.
- [ ] **Phase 2**: Landing Page polish, Authentication UI (`login.html`, `register.html`), Auth API.
- [ ] **Phase 3**: Resume Upload Interface (Drag & Drop) + PDF / DOCX Parser pipeline.
- [ ] **Phase 4**: Information Extraction + Comprehensive Skill Taxonomy Knowledge Base + spaCy.
- [ ] **Phase 5**: Deterministic Resume Quality & ATS Compatibility Scoring Engine.
- [ ] **Phase 6**: Job Description Analysis + Sentence Transformers Semantic Matcher + Skill Gap.
- [ ] **Phase 7**: Gemini AI Qualitative Reasoning & Hallucination-Free Bullet Polisher.
- [ ] **Phase 8**: Interactive HTML/CSS/JS Results Dashboard with Chart.js.
- [ ] **Phase 9**: Resume History, Comparison Mode, and One-Click "Try Demo" Flow.
- [ ] **Phase 10**: Testing, Security Verification & College Presentation Materials.
