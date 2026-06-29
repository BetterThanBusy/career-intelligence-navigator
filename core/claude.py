"""
core/claude.py

Single shared Claude service.
Every agent calls ask_json(). Nothing else.

Rules:
- One function
- Returns parsed dict
- Raises ClaudeError on failure
- No retries hidden inside agents
"""

import json
import os
import time
import anthropic

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def ask_json(
    prompt: str,
    max_tokens: int = 2000,
    model: str = "claude-sonnet-4-6",
    retries: int = 2,
) -> dict:
    """
    Send a prompt to Claude. Return parsed JSON dict.

    Usage:
        result = ask_json(prompt)

    Raises:
        ClaudeError if all retries fail
        json.JSONDecodeError if response is not valid JSON
    """
    client = _get_client()
    last_error = None

    for attempt in range(retries + 1):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )

            raw = ""
            for block in response.content:
                if hasattr(block, "text"):
                    raw += block.text

            raw = raw.strip()

            # Strip markdown fences
            if "```" in raw:
                raw = raw.replace("```json", "").replace("```", "").strip()

            # Extract first valid JSON object
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                raw = raw[start:end + 1]

            return json.loads(raw)

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Claude returned invalid JSON: {str(e)}", e.doc, e.pos
            )
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(2 ** attempt)

    raise ClaudeError(f"Claude failed after {retries + 1} attempts: {last_error}")


class ClaudeError(Exception):
    pass
