---
marp: true
theme: default
class: lead
backgroundColor: #f0f4f8
---

# Student Life Automation Platform 🚀
A smart bridge between academic learning and industry expectations.

---

## The Problem ⚠️

- **The Gap**: Students struggle to match their skills with rapidly evolving industry requirements.
- **Fragmentation**: Academic curricula often lag behind real-world job market demands.
- **Uncertainty**: "What should I learn next?" "Are my projects good enough?"

---

## Our Solution 💡

A comprehensive platform that:
1. **Analyzes**: Understands a student's profile (GitHub, LinkedIn).
2. **Identifies**: Maps current abilities against live job market data and uncovers skill gaps.
3. **Guides**: Generates personalized, actionable learning roadmaps.
4. **Suggests**: Recommends AI-curated hands-on projects to build out missing skills.

---

## What We Are Using 🛠️

**Frontend**:
- UI built with **React** (`react`, `react-dom`)
- Bundled and structured using **Vite** for blazing fast performance
- Vanilla **CSS** for custom, engaging visual aesthetics

**Backend**:
- Built with **FastAPI** for high-performance API endpoints
- Integrated **Google GenAI** (`google-genai`) to generate real-time AI profile analysis and project recommendations
- Robust **Python** environment with Uvicorn server and validation (Pydantic)

**Currently Built Components**:
- Dashboard interface (`Dashboard.jsx`, `Dashboard.css`)
- Visual skill gap analysis (`SkillGapVisualizer.jsx`)
- Roadmap guidance (`RoadmapRecommendations.jsx`)

---

## Current Architecture 🏗️

```text
student_analysis/
├── backend/            # Python Services (API, AI logic)
│   ├── main.py         # FastAPI application & /api/analyze endpoint
│   ├── models.py       # Pydantic schemas for data validation
│   └── venv/           # Virtual environment
└── frontend/           # React SPA
    └── src/
        ├── App.jsx     # Main entry
        └── components/ # Specialized UI elements
            ├── Dashboard.jsx
            ├── SkillGapVisualizer.jsx
            └── RoadmapRecommendations.jsx
```

---

## How it Works ⚙️

1. **User Profile Ingestion**: Connect academic history and coding portfolios.
2. **Market Evaluation Engine**: Compare ingested skills against updated job requirements.
3. **Skill Gap Visualizer**: Easily understand where you currently stand.
4. **Actionable Deliverables**: Receive a recommended list of tailored projects.

---

## Future Roadmap 🚀

- **Frontend Integration**: Connect the React application to the active `/api/analyze` FastAPI endpoint.
- **Data Ingestion**: Pluggable integrations for LinkedIn/GitHub APIs to parse profiles automatically.
- **Progress Tracking**: Continuous monitoring of the student's learning journey and completed projects.

*(Note: This presentation will be maintained and updated as the project evolves)*

---

# Thank You! 🎯
*Bridging the gap between students and the industry.*
