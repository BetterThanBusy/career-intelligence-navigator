from core.base_agent import BaseAgent


class WeeklyScheduleAgent(BaseAgent):
    prompt_path = "career/weekly_schedule.md"
    max_tokens = 2000
