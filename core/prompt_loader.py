"""
core/prompt_loader.py

Loads prompt templates from prompts/ directory.
Replaces {{variable}} placeholders with actual values.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PROMPTS_DIR = ROOT_DIR / "prompts"


def load_prompt(prompt_path: str, **kwargs) -> str:
    """
    Load a prompt template and inject variables.

    Usage:
        load_prompt("resume/parse.md", resume_text=resume)
        load_prompt("ats/score.md", resume=resume, job_description=jd)
    """
    file_path = PROMPTS_DIR / prompt_path

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt not found: {file_path}")

    prompt = file_path.read_text(encoding="utf-8")

    for key, value in kwargs.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

    return prompt
