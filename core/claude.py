import json
import os
import re
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


def _repair_json(raw: str) -> str:
    """
    Attempt to repair truncated or malformed JSON.
    Tries to close any open brackets/braces.
    """
    # Count open vs closed braces and brackets
    open_braces = raw.count("{") - raw.count("}")
    open_brackets = raw.count("[") - raw.count("]")

    # Close any unclosed strings first
    # Find last complete value boundary
    repaired = raw.rstrip()

    # Remove trailing comma if present
    if repaired.endswith(","):
        repaired = repaired[:-1]

    # Close open brackets first (inner), then braces (outer)
    repaired += "]" * open_brackets
    repaired += "}" * open_braces

    return repaired


def _extract_json(raw: str) -> dict:
    """
    Robustly extract JSON from Claude response.
    Tries multiple strategies before giving up.
    """
    # Clean markdown fences
    if "```" in raw:
        raw = raw.replace("```json", "").replace("```", "").strip()

    # Find JSON boundaries
    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1:
        candidate = raw[start:end + 1]

        # Strategy 1: Direct parse
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

        # Strategy 2: Repair and parse
        try:
            repaired = _repair_json(candidate)
            return json.loads(repaired)
        except json.JSONDecodeError:
            pass

        # Strategy 3: Find last valid JSON boundary
        # Walk backwards to find last valid closing brace
        for i in range(len(raw) - 1, start, -1):
            if raw[i] == "}":
                try:
                    return json.loads(raw[start:i + 1])
                except json.JSONDecodeError:
                    continue

    raise json.JSONDecodeError(
        f"No valid JSON found in response",
        raw, 0
    )


def ask_json(
    prompt: str,
    max_tokens: int = 2000,
    model: str = "claude-sonnet-4-6",
    retries: int = 2,
) -> dict:
    """
    Send a prompt to Claude. Return parsed JSON dict.
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
            print(f"[Claude] Response length: {len(raw)}")

            return _extract_json(raw)

        except json.JSONDecodeError as e:
            last_error = e
            if attempt < retries:
                print(f"[Claude] JSON parse failed attempt {attempt + 1}, retrying")
                time.sleep(2 ** attempt)
            else:
                raise json.JSONDecodeError(
                    f"Claude returned invalid JSON: {str(e)}",
                    str(e), 0
                )
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(2 ** attempt)

    raise ClaudeError(f"Claude failed after {retries + 1} attempts: {last_error}")


class ClaudeError(Exception):
    pass
