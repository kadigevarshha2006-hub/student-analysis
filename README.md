# ⚡ ResumeAI — AI-Powered Resume Analyzer & Job Matching System

A full-stack web application designed to help job seekers evaluate their resumes against Applicant Tracking Systems (ATS) and target job descriptions. The system parses resumes, extracts technical skills, computes semantic similarity with job descriptions, and provides AI-powered bullet point improvements and learning roadmaps.

---

## 🌐 Live Demo & Repository

- **Live Application**: [Add your live Render link here, e.g., `https://resume-ai-xxxx.onrender.com`]
- **GitHub Repository**: [https://github.com/kadigevarshha2006-hub/student-analysis](https://github.com/kadigevarshha2006-hub/student-analysis)

---

## ✨ Features

- **Document Parsing**: Extracts text, contact information, education, and work experience from PDF and DOCX files.
- **Skill Extraction**: Automatically extracts 500+ technical and soft skills with alias normalization (e.g., "JS" and "ES6" map to "JavaScript").
- **ATS Compatibility Scoring**: Calculates a deterministic compatibility score (0–100) based on section completeness, skill relevance, readability, and formatting hygiene.
- **Semantic Job Matching**: Uses dense vector embeddings (`all-MiniLM-L6-v2`) and cosine similarity to measure true semantic alignment between candidate experience and job descriptions.
- **AI Bullet Point Refinement**: Utilizes Google Gemini (`gemini-2.5-flash`) to rewrite weak bullet points into high-impact, action-driven statements without inventing false metrics.
- **Skill-Gap Learning Roadmap**: Categorizes missing skills into High, Medium, and Low priorities with an actionable learning schedule.
- **Interactive Visualizations**: Visualizes score breakdowns and category benchmarks using Chart.js radar and bar charts.
- **Authentication & Dashboard**: Secure user registration and login with JWT and bcrypt, with saved historical analysis tracking.
- **Responsive UI**: Clean SaaS design with dark/light mode support for desktop and mobile devices.

---

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Chart.js
- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0
- **NLP & Machine Learning**: Sentence Transformers (`all-MiniLM-L6-v2`), Scikit-learn
- **Generative AI**: Google Gemini API (`gemini-2.5-flash`)
- **Document Parsing**: `pdfplumber`, `pypdf`, `python-docx`
- **Database**: SQLite (default zero-config) & MySQL 8.0 support
- **Security**: JWT (OAuth2 Bearer Tokens), Native Bcrypt password hashing
- **Deployment**: Render, Docker, Uvicorn

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.10 or higher
- Git
- A free Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the Repository
```bash
git clone https://github.com/kadigevarshha2006-hub/student-analysis.git
cd student-analysis
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `backend/` folder (or copy from `.env.example`):
```env
PORT=8000
HOST=0.0.0.0
SECRET_KEY=your_super_secret_jwt_key_here
DATABASE_URL=sqlite:///./resume_ai.db
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Start the Application
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
*(On Windows, you can also simply double-click `run.bat`)*

Open your browser and navigate to:
```text
http://localhost:8000
```
Interactive API documentation is available at `http://localhost:8000/docs`.

---

## 📖 Usage

1. **Sign Up / Sign In**: Create an account or explore using guest mode.
2. **Upload Resume**: Drag and drop your resume file (`.pdf` or `.docx`) or paste raw resume text.
3. **Add Job Description**: Paste the target job description to match against.
4. **View ATS Analysis**: Inspect your overall compatibility score, section checks, and keyword density.
5. **Review Skill Gaps**: Explore matched, partial, and missing skills with recommended learning timelines.
6. **Improve Bullet Points**: Review and copy AI-enhanced bullet points for your resume.

---

## 📸 Screenshots / Demo

### Home & Landing Page
*[Add Landing Page Screenshot Here, e.g. `![Landing Page](assets/screenshot_home.png)`]*

### Resume & Job Description Analyzer
*[Add Analyzer Screenshot Here, e.g. `![Analyzer Screen](assets/screenshot_analyzer.png)`]*

### Interactive ATS Scoring Dashboard
*[Add Results Screenshot Here, e.g. `![Results Dashboard](assets/screenshot_results.png)`]*

---

## 🔮 Future Improvements

- **Direct Export**: Download enhanced resumes directly into formatted PDF and Word templates.
- **Live Job Board Integration**: Fetch live job postings directly from platforms like LinkedIn or Indeed.
- **Multi-Language Parsing**: Support non-English resumes and international job descriptions.
- **Recruiter Batch Mode**: Allow HR teams to upload and rank multiple resumes against a single job description.

---

## 📄 License

This project was built for academic and portfolio purposes. Feel free to use and adapt it for learning.
