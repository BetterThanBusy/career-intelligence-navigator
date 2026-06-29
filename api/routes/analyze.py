"""
api/routes/analyze.py

Two endpoints:
POST /api/ats/analyze     → run ATS pipeline
POST /api/career/analyze  → run Career Intelligence pipeline
"""

from fastapi import APIRouter, HTTPException
from schemas.models import ATSRequest, CareerRequest
from pipelines.ats_pipeline import run_ats_pipeline
from pipelines.career_pipeline import run_career_pipeline

router = APIRouter()


@router.post("/ats/analyze")
async def ats_analyze(request: ATSRequest):
    try:
        result = run_ats_pipeline(
            resume_text=request.resume_text,
            job_description=request.job_description
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/career/analyze")
async def career_analyze(request: CareerRequest):
    try:
        result = run_career_pipeline(
            resume_text=request.resume_text,
            target_role=request.target_role,
            industry=request.industry,
            hours_per_week=request.hours_per_week,
            budget=request.budget,
            learning_style=request.learning_style,
            timeline_months=request.timeline_months
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
