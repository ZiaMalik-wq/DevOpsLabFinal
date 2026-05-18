"""
Recommendations API — personalized upskilling roadmap.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CourseOut
from services.recommender import get_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("/{user_id}", response_model=list[CourseOut])
def recommendations(user_id: int, db: Session = Depends(get_db)):
    """Get personalized course recommendations based on user's skill gaps."""
    recs = get_recommendations(db, user_id)
    return [CourseOut(**r) for r in recs]
