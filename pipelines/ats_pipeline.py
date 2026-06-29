"""
pipelines/ats_pipeline.py

ATS Pipeline: 2 agents, runs sequentially, returns combined result.

Agent 1: ATSScorerAgent    → score, gaps, keywords
Agent 2: ResumeRewriterAgent → rewritten bullets, summary, skills

Each agent is independent. If rewriter fails, scorer result is still saved.
"""

import json
from agents.ats_scorer import ATSScorerAgent
from agents.resume_rewriter import ResumeRewriterAgent
from schemas.models import ATSResult


def run_ats_pipeline(resume_text: str, job_description: str) -> dict:
    """
    Run full ATS analysis.

    Returns combined dict ready for API response and DB storage.
    """

    print("[ATS Pipeline] Starting")

    # Agent 1: Score
    print("[ATS Pipeline] Agent 1: Scoring")
    scorer = ATSScorerAgent()
    score_result = scorer.run(
        resume=resume_text,
        job_description=job_description
    )
    print(f"[ATS Pipeline] Score: {score_result.get('ats_score')}")

    # Agent 2: Rewrite
    print("[ATS Pipeline] Agent 2: Rewriting")
    rewriter = ResumeRewriterAgent()
    rewrite_result = rewriter.run(
        resume=resume_text,
        job_description=job_description,
        missing_keywords=json.dumps(score_result.get("missing_keywords", [])),
        missing_skills=json.dumps(score_result.get("missing_skills", []))
    )
    print("[ATS Pipeline] Rewrite complete")

    # Merge results
    result = {**score_result, **rewrite_result}

    print(f"[ATS Pipeline] Complete. Score: {result.get('ats_score')}, Verdict: {result.get('final_verdict')}")
    return result
