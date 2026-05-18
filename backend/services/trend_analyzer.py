"""
Skill trend analysis — computes growth rates and identifies emerging / declining skills.
"""

from sqlalchemy.orm import Session
from models import Skill, SkillDemand


def compute_growth(demand_values: list[int]) -> int:
    """
    Compute growth percentage from first to last month.
    Growth = ((last - first) / first) * 100
    """
    if not demand_values or demand_values[0] == 0:
        return 0
    first = demand_values[0]
    last = demand_values[-1]
    return round(((last - first) / first) * 100)


def get_skill_trend_data(db: Session, skill_name: str) -> dict:
    """
    Get the trend data for a single skill.
    Returns { name, category, demand: [12 months], growth, avgSalary }
    """
    skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill:
        return None

    demands = (
        db.query(SkillDemand)
        .filter(SkillDemand.skill_id == skill.id)
        .order_by(SkillDemand.id)
        .all()
    )
    demand_values = [d.demand_count for d in demands]
    growth = compute_growth(demand_values)

    return {
        "name": skill.name,
        "category": skill.category,
        "demand": demand_values,
        "growth": growth,
        "avgSalary": skill.avg_salary,
    }


def get_all_trends(db: Session) -> list[dict]:
    """Get trend data for all tracked skills."""
    skills = db.query(Skill).all()
    results = []
    for skill in skills:
        trend = get_skill_trend_data(db, skill.name)
        if trend:
            results.append(trend)
    return results


def get_top_emerging(db: Session, limit: int = 10) -> list[dict]:
    """Get top N skills by growth rate."""
    trends = get_all_trends(db)
    trends.sort(key=lambda t: t["growth"], reverse=True)
    return [{"name": t["name"], "category": t["category"], "growth": t["growth"]} for t in trends[:limit]]
