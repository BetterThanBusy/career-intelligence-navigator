from core.base_agent import BaseAgent


class ResumeRewriterAgent(BaseAgent):
    prompt_path = "ats/rewrite.md"
    max_tokens = 2500
