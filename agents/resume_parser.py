from core.base_agent import BaseAgent


class ResumeParserAgent(BaseAgent):
    prompt_path = "resume/parse.md"
    max_tokens = 1500
