"""
User profile API — CRUD for user and their skills.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserSkill
from schemas import UserOut, UserSkillIn, UserSkillUpdate, UserSkillOut

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile with all skills."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        university=user.university,
        degree=user.degree,
        semester=user.semester,
        skills=[
            UserSkillOut(name=s.skill_name, proficiency=s.proficiency)
            for s in skills
        ],
    )


@router.post("/{user_id}/skills", response_model=UserSkillOut)
def add_skill(user_id: int, skill_in: UserSkillIn, db: Session = Depends(get_db)):
    """Add a skill to the user's profile."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if skill already exists
    existing = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id, UserSkill.skill_name == skill_in.name)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    new_skill = UserSkill(
        user_id=user_id,
        skill_name=skill_in.name,
        proficiency=skill_in.proficiency,
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return UserSkillOut(name=new_skill.skill_name, proficiency=new_skill.proficiency)


@router.put("/{user_id}/skills/{skill_name}", response_model=UserSkillOut)
def update_skill(user_id: int, skill_name: str, update: UserSkillUpdate, db: Session = Depends(get_db)):
    """Update a skill's proficiency."""
    skill = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id, UserSkill.skill_name == skill_name)
        .first()
    )
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill.proficiency = update.proficiency
    db.commit()
    db.refresh(skill)
    return UserSkillOut(name=skill.skill_name, proficiency=skill.proficiency)


@router.delete("/{user_id}/skills/{skill_name}")
def delete_skill(user_id: int, skill_name: str, db: Session = Depends(get_db)):
    """Remove a skill from the user's profile."""
    skill = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id, UserSkill.skill_name == skill_name)
        .first()
    )
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return {"detail": "Skill removed"}
