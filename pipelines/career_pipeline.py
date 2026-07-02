"""
Career Intelligence Pipeline — Redesigned
3 focused agents. Minimum context passing. ~4,500 tokens total.

Agent 1: Profile Intelligence  → understands WHO they are (1,200 tokens)
Agent 2: Market Intelligence   → understands WHAT market wants (1,000 tokens)  
Agent 3: Career Report         → produces the intelligence report (2,000 tokens)

Original resume text used ONCE in Agent 1 only.
Agents 2 and 3 receive only compact extracted data.
"""

from agents.profile_intelligence import ProfileIntelligenceAgent
from agents.market_intelligence import MarketIntelligenceAgent
from agents.career_report import CareerReportAgent


def run_career_pipeline(
    resume_text: str = None,
    current_role: str = None,
    industry: str = None,
    years_experience: int = None,
    career_goal: str = None,
    biggest_challenge: str = None,
    hours_per_week: int = 5,
    budget: str = "free",
    timeline_months: int = 3,
    target_role: str = None,
) -> dict:

    print("[Career Pipeline] Starting — 3 agent chain")

    # ── Agent 1: Profile Intelligence ─────────────────────────
    # Resume text used HERE and ONLY here
    print("[Career Pipeline] Agent 1: Profile intelligence")
    profile = ProfileIntelligenceAgent().run(
        resume_text=resume_text or "Not provided",
        current_role=current_role or "Not specified",
        industry=industry or "Not specified",
        years_experience=years_experience or "Not specified",
        career_goal=career_goal or "Not specified",
        biggest_challenge=biggest_challenge or "Not specified"
    )

    # Extract ONLY what downstream agents need — not full profile
    role = profile.get("role", target_role or current_role or "Professional")
    top_skills = ", ".join(profile.get("top_skills", [])[:6])
    key_gaps = profile.get("key_gaps", [])[:3]
    experience_level = profile.get("experience_level", "mid-career")
    print(f"[Career Pipeline] Profile: {role}, {experience_level}")

    # ── Agent 2: Market Intelligence ──────────────────────────
    # Receives: role + top_skills only (NOT resume text)
    print("[Career Pipeline] Agent 2: Market intelligence")
    market = MarketIntelligenceAgent().run(
        role=role,
        top_skills=top_skills,
        industry=industry or "general"
    )

    in_demand = ", ".join(market.get("in_demand_skills", [])[:5])
    salary_mid = market.get("salary_range", {}).get("mid", 0)
    hiring_trend = market.get("hiring_trend", "stable")
    print(f"[Career Pipeline] Market: {hiring_trend}, salary mid ${salary_mid}")

    # ── Agent 3: Career Report ────────────────────────────────
    # Receives: compact profile + compact market data only
    # This is the intelligence layer — produces the full report
    print("[Career Pipeline] Agent 3: Generating career report")
    report_input = {
        "role": role,
        "experience_level": experience_level,
        "top_skills": top_skills,
        "key_gaps": ", ".join(str(g) for g in key_gaps),
        "career_goal": career_goal or "career growth",
        "biggest_challenge": biggest_challenge or "staying relevant",
        "in_demand_skills": in_demand,
        "salary_mid": salary_mid,
        "hiring_trend": hiring_trend,
        "hours_per_week": hours_per_week,
        "budget": budget,
        "timeline_months": timeline_months
    }

    report = CareerReportAgent().run(**report_input)
    print("[Career Pipeline] Report complete")

    return {
        "target_role": role,
        "profile_summary": profile,
        "market_intelligence": market,
        "career_report": report
    }
