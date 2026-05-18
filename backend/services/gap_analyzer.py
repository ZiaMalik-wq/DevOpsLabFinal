"""
Gap analysis — compares user skills against market demand to identify gaps.
"""

from sqlalchemy.orm import Session
from models import Skill, SkillDemand, UserSkill


def _get_top_market_skills(db: Session, limit: int = 20) -> list[dict]:
    """Get top skills by latest month demand."""
    skills = db.query(Skill).all()
    skill_data = []
    for skill in skills:
        demands = (
            db.query(SkillDemand)
            .filter(SkillDemand.skill_id == skill.id)
            .order_by(SkillDemand.id)
            .all()
        )
        if demands:
            latest = demands[-1].demand_count
            skill_data.append({
                "name": skill.name,
                "latest_demand": latest,
                "category": skill.category,
            })
    skill_data.sort(key=lambda s: s["latest_demand"], reverse=True)
    return skill_data[:limit]


def analyze_gaps(db: Session, user_id: int) -> dict:
    """
    Compare user skills to top market skills.
    Returns { matched, missing, outdated } lists.
    """
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    user_skill_map = {us.skill_name: us.proficiency for us in user_skills}
    top_market = _get_top_market_skills(db)

    matched = []
    missing = []
    outdated = []

    for market_skill in top_market:
        name = market_skill["name"]
        if name in user_skill_map:
            prof = user_skill_map[name]
            if prof < 40:
                outdated.append({
                    "name": name,
                    "proficiency": prof,
                    "status": "outdated",
                })
            else:
                matched.append({
                    "name": name,
                    "proficiency": prof,
                    "status": "matched",
                })
        else:
            missing.append({
                "name": name,
                "proficiency": None,
                "status": "missing",
            })

    return {"matched": matched, "missing": missing, "outdated": outdated}


def compute_match_score(db: Session, user_id: int) -> int:
    """
    Weighted similarity score (0–100).
    Weight = latest demand of each top skill.
    Score = sum(weight * proficiency/100) / sum(weight) * 100
    """
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    user_skill_map = {us.skill_name: us.proficiency for us in user_skills}
    top_market = _get_top_market_skills(db)

    total_weight = 0
    matched_weight = 0.0

    for ms in top_market:
        weight = ms["latest_demand"]
        total_weight += weight
        if ms["name"] in user_skill_map:
            prof = user_skill_map[ms["name"]]
            matched_weight += weight * (prof / 100)

    if total_weight == 0:
        return 0
    return round((matched_weight / total_weight) * 100)
