"""
AI-Based Skill Gap Analyzer — FastAPI Backend
"""

from dotenv import load_dotenv
load_dotenv()  # Load .env before anything else imports database config

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from seed import seed_database

# Import routers
from routers import jobs, skills, users, analysis, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB and seed data on startup."""
    init_db()
    seed_database()
    yield


app = FastAPI(
    title="AI-Based Skill Gap Analyzer",
    description="Backend API for skill extraction, trend analysis, gap detection, and upskilling recommendations.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server and AKS deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost",
        "http://127.0.0.1",
        "http://85.211.171.9",
        "http://85.211.171.9:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(jobs.router)
app.include_router(skills.router)
app.include_router(users.router)
app.include_router(analysis.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {
        "name": "AI-Based Skill Gap Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
