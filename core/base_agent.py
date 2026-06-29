"""
core/base_agent.py

Every agent:
1. Defines a prompt (string)
2. Calls run(**kwargs)
3. Gets back a validated Pydantic model

Nothing else lives in an agent.
"""

from abc import ABC, abstractmethod
from core.claude import ask_json
from core.prompt_loader import load_prompt


class BaseAgent(ABC):

    @property
    @abstractmethod
    def prompt_path(self) -> str:
        """Path to prompt file relative to prompts/ directory."""
        pass

    @property
    def max_tokens(self) -> int:
        return 2000

    def run(self, **kwargs) -> dict:
        """Load prompt, inject kwargs, call Claude, return dict."""
        prompt = load_prompt(self.prompt_path, **kwargs)
        return ask_json(prompt, max_tokens=self.max_tokens)
