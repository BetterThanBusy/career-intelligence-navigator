from core.anthropic_client import AnthropicClient
from core.perplexity_client import PerplexityClient


class LLMRouter:

    def __init__(self):

        self.anthropic = AnthropicClient()

        self.perplexity = PerplexityClient()

    def complete(
        self,
        task: str,
        system_prompt: str,
        user_prompt: str,
    ):

        if task in [

            "planner",

            "critic",

            "resume",

            "career",

            "profile"

        ]:

            return self.anthropic.complete(
                system_prompt,
                user_prompt
            )

        return self.perplexity.complete(
            system_prompt,
            user_prompt
        )
