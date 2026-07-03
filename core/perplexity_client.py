import os

from openai import OpenAI


class PerplexityClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            base_url="https://api.perplexity.ai"
        )

        self.model = os.getenv(
            "PERPLEXITY_MODEL",
            "sonar-pro"
        )

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=temperature,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.choices[0].message.content
