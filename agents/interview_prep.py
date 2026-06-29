from core.base_agent import BaseAgent


class InterviewPrepAgent(BaseAgent):
    prompt_path = "career/interview.md"
    max_tokens = 1500
