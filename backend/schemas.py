from pydantic import BaseModel
from typing import Optional


# ─── Skill schemas ───────────────────────────────────────
class SkillBase(BaseModel):
    name: str
    category: str
    avg_salary: str = ""


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True


class SkillTrendOut(BaseModel):
    name: str
    category: str
    demand: list[int]
    growth: int
    avgSalary: str


class TopEmergingOut(BaseModel):
    name: str
    category: str
    growth: int


class SkillCategoryOut(BaseModel):
    category: str
    skills: list[str]


# ─── Job schemas ─────────────────────────────────────────
class JobPostingOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    source: str
    salary: str
    posted: str
    description: str
    skills: list[str]

    class Config:
        from_attributes = True


class SkillFrequencyOut(BaseModel):
    skill: str
    count: int


# ─── User schemas ────────────────────────────────────────
class UserSkillIn(BaseModel):
    name: str
    proficiency: int = 50


class UserSkillUpdate(BaseModel):
    proficiency: int


class UserSkillOut(BaseModel):
    name: str
    proficiency: int

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    university: str
    degree: str
    semester: int
    skills: list[UserSkillOut]

    class Config:
        from_attributes = True


# ─── Analysis schemas ────────────────────────────────────
class GapItem(BaseModel):
    name: str
    proficiency: Optional[int] = None
    status: str  # "matched", "missing", "outdated"


class GapAnalysisOut(BaseModel):
    matched: list[GapItem]
    missing: list[GapItem]
    outdated: list[GapItem]


class MatchScoreOut(BaseModel):
    score: int


class DashboardStatsOut(BaseModel):
    totalJobsAnalyzed: int
    skillsTracked: int
    gapsDetected: int
    matchScore: int


# ─── Recommendation schemas ─────────────────────────────
class CourseOut(BaseModel):
    id: int
    skill: str
    title: str
    provider: str
    platform: str
    duration: str
    rating: float
    level: str
    url: str
    icon: str
    priority: str = "medium"
    growth: int = 0

    class Config:
        from_attributes = True


# ─── Regional demand ────────────────────────────────────
class RegionData(BaseModel):
    name: str
    data: list[int]


class RegionalDemandOut(BaseModel):
    labels: list[str]
    regions: list[RegionData]


# ─── NLP Extraction ─────────────────────────────────────
class ExtractedSkillsOut(BaseModel):
    job_id: int
    title: str
    extracted_skills: list[str]
