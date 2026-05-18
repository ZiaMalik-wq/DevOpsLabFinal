"""
Recommendation engine — maps skill gaps to courses and prioritizes learning path.
"""

from sqlalchemy.orm import Session
from models import Course, UserSkill
from services.gap_analyzer import analyze_gaps
from services.trend_analyzer import get_all_trends


def get_recommendations(db: Session, user_id: int) -> list[dict]:
    """
    Generate a prioritized list of course recommendations based on the user's skill gaps.
    Priority levels:
        - critical: missing skill with growth > 15%
        - high: missing skill with growth <= 15% OR outdated skill with growth > 15%
        - medium: outdated skill with growth <= 15%
    """
    gap = analyze_gaps(db, user_id)
    trends = {t["name"]: t["growth"] for t in get_all_trends(db)}

    recommendations = []

    # Process missing skills
    for item in gap["missing"]:
        skill_name = item["name"]
        growth = trends.get(skill_name, 0)
        course = db.query(Course).filter(Course.skill == skill_name).first()
        if course:
            priority = "critical" if growth > 15 else "high"
            recommendations.append(_course_to_dict(course, priority, growth))

    # Process outdated skills
    for item in gap["outdated"]:
        skill_name = item["name"]
        growth = trends.get(skill_name, 0)
        course = db.query(Course).filter(Course.skill == skill_name).first()
        if course:
            priority = "high" if growth > 15 else "medium"
            recommendations.append(_course_to_dict(course, priority, growth))

    # Sort by priority order
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    recommendations.sort(key=lambda r: priority_order.get(r["priority"], 3))

    return recommendations


def _course_to_dict(course: Course, priority: str, growth: int) -> dict:
    return {
        "id": course.id,
        "skill": course.skill,
        "title": course.title,
        "provider": course.provider,
        "platform": course.platform,
        "duration": course.duration,
        "rating": course.rating,
        "level": course.level,
        "url": course.url,
        "icon": course.icon,
        "priority": priority,
        "growth": growth,
    }
