"""
schemas/models.py

Pydantic models for every agent output.
Every agent result is validated before it leaves the pipeline.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────
# RESUME
# ─────────────────────────────────────────

class ResumeProfile(BaseModel):
    current_role: str
    years_experience: int
    skills: List[str]
    industries: List[str]
    education: List[str]
    companies: List[str]
    notable_achievements: List[str]
    inferred_strengths: List[str]
    potential_gaps: List[str]


# ─────────────────────────────────────────
# ATS
# ─────────────────────────────────────────

class ScoreBreakdown(BaseModel):
    keyword_match: int
    skills_alignment: int
    experience_relevance: int
    formatting_score: int


class CriticalFix(BaseModel):
    issue: str
    fix: str
    priority: str  # high | medium | low


class RewrittenBullet(BaseModel):
    original: str
    rewritten: str


class ATSResult(BaseModel):
    ats_score: int
    score_breakdown: ScoreBreakdown
    matched_keywords: List[str]
    missing_keywords: List[str]
    missing_skills: List[str]
    strengths: List[str]
    critical_fixes: List[CriticalFix]
    rewritten_summary: str
    rewritten_experience_bullets: List[RewrittenBullet]
    optimized_skills_section: List[str]
    final_verdict: str  # hire | maybe | no
    verdict_reason: str


# ─────────────────────────────────────────
# MARKET INTELLIGENCE
# ─────────────────────────────────────────

class SalaryRange(BaseModel):
    low: int
    mid: int
    high: int
    currency: str = "USD"


class MarketIntelligence(BaseModel):
    in_demand_skills: List[str]
    skills_at_risk: List[str]
    salary_range: SalaryRange
    target_job_titles: List[str]
    growing_adjacent_roles: List[str]
    top_certifications: List[str]
    market_summary: str
    hiring_trend: str  # growing | stable | declining
    source: Optional[str] = "claude"


# ─────────────────────────────────────────
# GAP ANALYSIS
# ─────────────────────────────────────────

class SkillGap(BaseModel):
    skill: str
    urgency: str  # high | medium | low
    reason: str
    time_to_learn: str


class SixMonthStep(BaseModel):
    month: str
    focus: str
    goal: str


class RecommendedPivot(BaseModel):
    target_role: str
    rationale: str
    time_to_qualify: str
    salary_upside: str


class GapAnalysis(BaseModel):
    gap_score: int
    critical_gaps: List[SkillGap]
    strengths_to_leverage: List[str]
    automation_risk_score: int
    automation_risk_breakdown: List[str]
    recommended_pivot: RecommendedPivot
    quick_wins: List[str]
    six_month_plan: List[SixMonthStep]
    competitive_advantage: str


# ─────────────────────────────────────────
# LEARNING PATH
# ─────────────────────────────────────────

class LearningPriority(BaseModel):
    priority: int
    skill: str
    why: str
    urgency: str
    weeks_needed: int


class Certification(BaseModel):
    name: str
    provider: str
    url: str
    cost: str
    duration_weeks: int
    salary_uplift: str
    employer_recognition: str
    why: str


class Resource(BaseModel):
    name: str
    url: str
    platform: str
    cost: str
    hours: float
    why: str


class WeeklyStep(BaseModel):
    week: int
    focus: str
    primary_resource: Resource
    milestone: str


class PortfolioProject(BaseModel):
    project_name: str
    description: str
    skills_demonstrated: List[str]
    tech_stack: List[str]
    deliverable: str
    interview_talking_point: str
    difficulty: str
    time_to_build: str


class ContentPlan(BaseModel):
    week: int
    content_type: str
    hook: str
    topic: str
    why_this_works: str


class InterviewQuestion(BaseModel):
    question: str
    why_asked: str
    star_framework: str


class GapHandling(BaseModel):
    gap: str
    how_to_address: str


class SalaryIntel(BaseModel):
    market_low: int
    market_mid: int
    market_high: int
    negotiation_tip: str


class InterviewPrep(BaseModel):
    likely_questions: List[InterviewQuestion]
    gap_handling: List[GapHandling]
    salary_range: SalaryIntel


# ─────────────────────────────────────────
# FULL CAREER INTELLIGENCE REPORT
# ─────────────────────────────────────────

class CareerIntelligenceReport(BaseModel):
    profile: ResumeProfile
    market: MarketIntelligence
    gap_analysis: GapAnalysis
    learning_priorities: List[LearningPriority]
    certifications: List[Certification]
    weekly_schedule: List[WeeklyStep]
    portfolio_projects: List[PortfolioProject]
    interview_prep: InterviewPrep
    quick_wins: List[str]
    target_role: str
    timeline_months: int


# ─────────────────────────────────────────
# API REQUEST MODELS
# ─────────────────────────────────────────

class ATSRequest(BaseModel):
    resume_text: str
    job_description: str


class CareerRequest(BaseModel):
    resume_text: str
    target_role: Optional[str] = None
    industry: Optional[str] = None
    hours_per_week: int = 5
    budget: str = "free"
    learning_style: str = "mixed"
    timeline_months: int = 3
