from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    avg_salary = Column(String(20), default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    demands = relationship("SkillDemand", back_populates="skill", cascade="all, delete-orphan")


class SkillDemand(Base):
    __tablename__ = "skill_demands"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    month = Column(String(10), nullable=False)  # e.g. "Apr 25"
    demand_count = Column(Integer, default=0)

    skill = relationship("Skill", back_populates="demands")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(100), nullable=False)
    source = Column(String(50), nullable=False)
    salary = Column(String(50), default="")
    posted_date = Column(String(20), default="")
    description = Column(Text, default="")
    raw_skills = Column(JSONB, default=list)  # JSONB for efficient querying in PostgreSQL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    university = Column(String(200), default="")
    degree = Column(String(100), default="")
    semester = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(Integer, default=50)  # 0–100

    user = relationship("User", back_populates="skills")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    skill = Column(String(100), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    provider = Column(String(100), default="")
    platform = Column(String(100), default="")
    duration = Column(String(30), default="")
    rating = Column(Float, default=0.0)
    level = Column(String(30), default="Beginner")
    url = Column(String(500), default="#")
    icon = Column(String(10), default="📘")


class RegionalDemand(Base):
    __tablename__ = "regional_demands"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(50), nullable=False)
    month = Column(String(10), nullable=False)
    job_count = Column(Integer, default=0)
