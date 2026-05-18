"""
Analysis API — gap analysis, match score, dashboard stats.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import JobPosting, Skill, User, UserSkill
from schemas import GapAnalysisOut, GapItem, MatchScoreOut, DashboardStatsOut
from services.gap_analyzer import analyze_gaps, compute_match_score

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.get("/{user_id}/gap", response_model=GapAnalysisOut)
def gap_analysis(user_id: int, db: Session = Depends(get_db)):
    """Get gap analysis for a user — matched, missing, and outdated skills."""
    result = analyze_gaps(db, user_id)
    return GapAnalysisOut(
        matched=[GapItem(**item) for item in result["matched"]],
        missing=[GapItem(**item) for item in result["missing"]],
        outdated=[GapItem(**item) for item in result["outdated"]],
    )


@router.get("/{user_id}/match-score", response_model=MatchScoreOut)
def match_score(user_id: int, db: Session = Depends(get_db)):
    """Get the user's market match score (0–100)."""
    score = compute_match_score(db, user_id)
    return MatchScoreOut(score=score)


@router.get("/dashboard-stats", response_model=DashboardStatsOut)
def dashboard_stats(db: Session = Depends(get_db)):
    """Get aggregate stats for the dashboard."""
    total_jobs = db.query(JobPosting).count()
    total_skills = db.query(Skill).count()

    # For a default user (id=1), compute gaps
    user = db.query(User).first()
    gaps_detected = 0
    match = 0
    if user:
        result = analyze_gaps(db, user.id)
        gaps_detected = len(result["missing"]) + len(result["outdated"])
        match = compute_match_score(db, user.id)

    return DashboardStatsOut(
        totalJobsAnalyzed=total_jobs,
        skillsTracked=total_skills,
        gapsDetected=gaps_detected,
        matchScore=match,
    )
