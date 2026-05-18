"""
Skills API — trends, categories, emerging skills, regional demand.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Skill, SkillDemand, RegionalDemand
from schemas import SkillOut, SkillTrendOut, TopEmergingOut, SkillCategoryOut, RegionalDemandOut, RegionData
from services.trend_analyzer import get_all_trends, get_top_emerging

router = APIRouter(prefix="/api/skills", tags=["Skills"])


MONTHS = [
    "Apr 25", "May 25", "Jun 25", "Jul 25", "Aug 25", "Sep 25",
    "Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26",
]


@router.get("", response_model=list[SkillOut])
def list_skills(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List all tracked skills, optionally filtered by category."""
    q = db.query(Skill)
    if category and category != "All":
        q = q.filter(Skill.category == category)
    return q.order_by(Skill.name).all()


@router.get("/trends", response_model=list[SkillTrendOut])
def skill_trends(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all skill trends with 12-month demand data."""
    trends = get_all_trends(db)

    if category and category != "All":
        trends = [t for t in trends if t["category"] == category]
    if search:
        lower = search.lower()
        trends = [t for t in trends if lower in t["name"].lower()]

    return [
        SkillTrendOut(
            name=t["name"],
            category=t["category"],
            demand=t["demand"],
            growth=t["growth"],
            avgSalary=t["avgSalary"],
        )
        for t in trends
    ]


@router.get("/categories", response_model=list[SkillCategoryOut])
def skill_categories(db: Session = Depends(get_db)):
    """Get skills grouped by category."""
    skills = db.query(Skill).order_by(Skill.category, Skill.name).all()
    cats: dict[str, list[str]] = {}
    for s in skills:
        cats.setdefault(s.category, []).append(s.name)
    return [SkillCategoryOut(category=c, skills=ss) for c, ss in cats.items()]


@router.get("/top-emerging", response_model=list[TopEmergingOut])
def top_emerging(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Get top N skills by growth rate."""
    return get_top_emerging(db, limit)


@router.get("/regional-demand", response_model=RegionalDemandOut)
def regional_demand(db: Session = Depends(get_db)):
    """Get regional job demand over 12 months."""
    all_entries = db.query(RegionalDemand).order_by(RegionalDemand.id).all()

    regions_data: dict[str, list[int]] = {}
    for entry in all_entries:
        regions_data.setdefault(entry.region, []).append(entry.job_count)

    return RegionalDemandOut(
        labels=MONTHS,
        regions=[RegionData(name=name, data=data) for name, data in regions_data.items()],
    )
