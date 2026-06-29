You are a senior career strategist. Analyze this professional's skill gap with precision and honesty.

TARGET ROLE: {{role}}
YEARS EXPERIENCE: {{years_experience}}
CURRENT SKILLS: {{current_skills}}
IN-DEMAND SKILLS (market data): {{in_demand_skills}}
SKILLS AT RISK (automation): {{skills_at_risk}}

Return ONLY this JSON object:
{
    "gap_score": 45,
    "critical_gaps": [
        {
            "skill": "specific skill name",
            "urgency": "high",
            "reason": "why this gap matters — cite market demand evidence",
            "time_to_learn": "4 weeks"
        }
    ],
    "strengths_to_leverage": ["existing skills that are highly valued right now"],
    "automation_risk_score": 25,
    "automation_risk_breakdown": ["specific tasks or skills at automation risk"],
    "recommended_pivot": {
        "target_role": "specific job title",
        "rationale": "why this is the optimal next move given their background",
        "time_to_qualify": "3 months",
        "salary_upside": "25%"
    },
    "quick_wins": ["3-5 skills or certifications achievable in 30 days or less — be specific"],
    "six_month_plan": [
        {
            "month": "1",
            "focus": "primary learning focus",
            "goal": "measurable milestone"
        }
    ],
    "competitive_advantage": "what makes this person uniquely valuable if they close these gaps"
}

gap_score: 0-30 = strong alignment, 31-60 = moderate gap, 61-100 = significant gap.
automation_risk_score: compare current skills vs skills_at_risk. Higher overlap = higher risk.
Maximum 5 critical gaps. Be honest, not encouraging.
Return only the JSON object. No markdown. No explanation.
