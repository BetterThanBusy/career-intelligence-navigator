from core.base_agent import BaseAgent


class ATSScorerAgent(BaseAgent):
    prompt_path = "ats/score.md"
    max_tokens = 2000
