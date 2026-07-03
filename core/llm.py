"""
Enterprise LLM Gateway

Every model call in the system goes through this file.

Responsibilities:
- OpenAI connection
- Retry logic
- JSON mode
- Token tracking
- Cost estimation
- Logging
"""

from __future__ import annotations

import json
import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
MAX_RETRIES = 3

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class LLMGateway:

    def __init__(self):

        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_output_tokens: int = 1200
    ) -> str:

        for attempt in range(MAX_RETRIES):

            try:

                response = client.responses.create(

                    model=MODEL,

                    temperature=temperature,

                    max_output_tokens=max_output_tokens,

                    input=[
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

                usage = response.usage

                self.total_prompt_tokens += usage.input_tokens
                self.total_completion_tokens += usage.output_tokens

                return response.output_text

            except Exception as e:

                if attempt == MAX_RETRIES - 1:
                    raise e

                time.sleep(2)

    def json_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0
    ) -> dict:

        result = self.chat(
            system_prompt,
            user_prompt,
            temperature=temperature
        )

        try:

            return json.loads(result)

        except Exception:

            raise ValueError(
                "LLM did not return valid JSON.\n\n"
                + result
            )

    def stats(self):

        return {

            "prompt_tokens": self.total_prompt_tokens,

            "completion_tokens": self.total_completion_tokens,

            "total_tokens":
                self.total_prompt_tokens
                + self.total_completion_tokens

        }


llm = LLMGateway()
