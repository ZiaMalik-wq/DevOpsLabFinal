"""
Job postings API — CRUD, filters, and NLP skill extraction.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import JobPosting
from schemas import JobPostingOut, SkillFrequencyOut, ExtractedSkillsOut
from services.nlp_extractor import extract_skills

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("", response_model=list[JobPostingOut])
def list_jobs(
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List job postings with optional filters."""
    q = db.query(JobPosting)

    if search:
        pattern = f"%{search}%"
        q = q.filter(
            JobPosting.title.ilike(pattern)
            | JobPosting.company.ilike(pattern)
            | JobPosting.description.ilike(pattern)
        )
    if location and location != "All":
        q = q.filter(JobPosting.location == location)
    if source and source != "All":
        q = q.filter(JobPosting.source == source)

    jobs = q.order_by(JobPosting.posted_date.desc()).all()
    return [
        JobPostingOut(
            id=j.id,
            title=j.title,
            company=j.company,
            location=j.location,
            source=j.source,
            salary=j.salary,
            posted=j.posted_date,
            description=j.description,
            skills=j.raw_skills or [],
        )
        for j in jobs
    ]


@router.get("/skill-frequency", response_model=list[SkillFrequencyOut])
def skill_frequency(
    location: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get skill frequency across filtered job postings."""
    q = db.query(JobPosting)
    if location and location != "All":
        q = q.filter(JobPosting.location == location)
    if source and source != "All":
        q = q.filter(JobPosting.source == source)

    jobs = q.all()
    freq: dict[str, int] = {}
    for job in jobs:
        for skill in (job.raw_skills or []):
            freq[skill] = freq.get(skill, 0) + 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [SkillFrequencyOut(skill=s, count=c) for s, c in sorted_freq[:15]]


@router.get("/{job_id}", response_model=JobPostingOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a single job posting by ID."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")
    return JobPostingOut(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        source=job.source,
        salary=job.salary,
        posted=job.posted_date,
        description=job.description,
        skills=job.raw_skills or [],
    )


@router.get("/{job_id}/extract-skills", response_model=ExtractedSkillsOut)
def extract_job_skills(job_id: int, db: Session = Depends(get_db)):
    """Run NLP extraction on a job's description and return extracted skills."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")

    extracted = extract_skills(f"{job.title} {job.description}")
    return ExtractedSkillsOut(
        job_id=job.id,
        title=job.title,
        extracted_skills=extracted,
    )
