"""
pipelines/career_pipeline.py

Career Intelligence Pipeline: 7 focused agents.

Each agent:
- Receives only what it needs
- Returns a small focused JSON
- Fails independently (won't break other agents)

Agent 1: ResumeParserAgent        → structured profile
Agent 2: MarketIntelligenceAgent  → live market data
Agent 3: GapAnalyzerAgent         → gap score + plan
Agent 4: LearningPrioritiesAgent  → what to learn + order
Agent 5: CertificationsAgent      → which certs + ROI
Agent 6: WeeklyScheduleAgent      → week by week plan
Agent 7: PortfolioAgent           → GitHub projects
Agent 8: InterviewPrepAgent       → questions + salary

All results stored independently.
Orchestrator combines into final report.
"""

import json

from agents.resume_parser import ResumeParserAgent
from agents.market_intelligence import MarketIntelligenceAgent
from agents.gap_analyzer import GapAnalyzerAgent
from agents.learning_priorities import LearningPrioritiesAgent
from agents.certifications import CertificationsAgent
from agents.weekly_schedule import WeeklyScheduleAgent
from agents.portfolio import PortfolioAgent
from agents.interview_prep import InterviewPrepAgent


def run_career_pipeline(
    resume_text: str,
    target_role: str = None,
    industry: str = None,
    hours_per_week: int = 5,
    budget: str = "free",
    learning_style: str = "mixed",
    timeline_months: int = 3,
) -> dict:
    """
    Run full Career Intelligence analysis.
    Returns structured report ready for API response and DB storage.
    """

    print("[Career Pipeline] Starting")

    # ── Agent 1: Parse Resume ──────────────────────────────────
    print("[Career Pipeline] Agent 1: Parsing resume")
    profile = ResumeParserAgent().run(resume_text=resume_text)
    role = target_role or profile.get("current_role", "Professional")
    skills = json.dumps(profile.get("skills", [])[:8])
    print(f"[Career Pipeline] Role: {role}")

    # ── Agent 2: Market Intelligence ──────────────────────────
    print("[Career Pipeline] Agent 2: Market intelligence")
    market = MarketIntelligenceAgent().run(
        role=role,
        skills=skills,
        industry=industry or "general"
    )
    print(f"[Career Pipeline] Hiring trend: {market.get('hiring_trend')}")

    # ── Agent 3: Gap Analysis ─────────────────────────────────
    print("[Career Pipeline] Agent 3: Gap analysis")
    in_demand = json.dumps(market.get("in_demand_skills", []))
    at_risk = json.dumps(market.get("skills_at_risk", []))
    gap = GapAnalyzerAgent().run(
        role=role,
        current_skills=skills,
        in_demand_skills=in_demand,
        skills_at_risk=at_risk,
        years_experience=profile.get("years_experience", 5)
    )
    print(f"[Career Pipeline] Gap score: {gap.get('gap_score')}")

    # ── Agent 4: Learning Priorities ──────────────────────────
    print("[Career Pipeline] Agent 4: Learning priorities")
    critical_gaps = json.dumps(gap.get("critical_gaps", [])[:4])
    target = gap.get("recommended_pivot", {}).get("target_role", role)
    priorities = LearningPrioritiesAgent().run(
        target_role=target,
        critical_gaps=critical_gaps
    )
    priority_list = priorities.get("priorities", [])
    skills_to_learn = json.dumps([p.get("skill") for p in priority_list[:4]])
    print(f"[Career Pipeline] Priorities set: {len(priority_list)}")

    # ── Agent 5: Certifications ───────────────────────────────
    print("[Career Pipeline] Agent 5: Certifications")
    certs = CertificationsAgent().run(
        target_role=target,
        skills_to_certify=skills_to_learn
    )
    cert_list = certs.get("certifications", [])
    print(f"[Career Pipeline] Certs found: {len(cert_list)}")

    # ── Agent 6: Weekly Schedule ──────────────────────────────
    print("[Career Pipeline] Agent 6: Weekly schedule")
    schedule = WeeklyScheduleAgent().run(
        target_role=target,
        priorities=json.dumps(priority_list[:4]),
        hours_per_week=hours_per_week,
        timeline_months=timeline_months,
        budget=budget,
        learning_style=learning_style
    )
    schedule_list = schedule.get("weeks", [])
    print(f"[Career Pipeline] Schedule weeks: {len(schedule_list)}")

    # ── Agent 7: Portfolio Projects ───────────────────────────
    print("[Career Pipeline] Agent 7: Portfolio projects")
    portfolio = PortfolioAgent().run(
        target_role=target,
        skills_to_demonstrate=skills_to_learn
    )
    project_list = portfolio.get("projects", [])
    print(f"[Career Pipeline] Projects: {len(project_list)}")

    # ── Agent 8: Interview Prep ───────────────────────────────
    print("[Career Pipeline] Agent 8: Interview prep")
    interview = InterviewPrepAgent().run(
        target_role=target,
        critical_gaps=critical_gaps,
        salary_range=json.dumps(market.get("salary_range", {}))
    )
    print("[Career Pipeline] Interview prep complete")

    # ── Compose Final Report ──────────────────────────────────
    report = {
        "target_role": target,
        "profile": profile,
        "market_intelligence": market,
        "gap_analysis": gap,
        "learning_priorities": priority_list,
        "certifications": cert_list,
        "weekly_schedule": schedule_list,
        "portfolio_projects": project_list,
        "interview_prep": interview,
        "quick_wins": gap.get("quick_wins", []),
        "timeline_months": timeline_months,
        "hours_per_week": hours_per_week,
    }

    print("[Career Pipeline] Complete")
    return report
