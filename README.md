# Student Analysis Platform

An AI-powered web application that analyzes a student's GitHub profile or uploaded resume against current industry demands to identify skill gaps and generate actionable, day-by-day learning roadmaps and dynamic project recommendations.

## Tech Stack
- **Frontend**: React + Vite
- **Backend**: FastAPI (Python)
- **AI Engine**: Google Gemini (flash-lite)
- **Deployment**: Vercel (Frontend) & Render (Backend)

## Setup Locally
1. Navigate to the `backend` folder, install requirements with `pip install -r requirements.txt`, create a `.env` file with `GEMINI_API_KEY`, and run `uvicorn main:app --reload`.
2. Navigate to the `frontend` folder, install dependencies with `npm install`, and start the development server with `npm run dev`.
