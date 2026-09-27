
import json
import re

from ai_service import client
from pii_detector import detect_pii
from pii_handler import redact_pii


def parse_task(instruction: str):
    """
    Masks detected PII before sending the instruction to Gemini.
    """

    # Step 1: Detect personal information locally
    pii = detect_pii(instruction)

    # Step 2: Mask detected personal information locally
    safe_instruction = redact_pii(instruction, pii)

    # Step 3: Send only the masked instruction to Gemini
    prompt = f"""
You are the Task Understanding Module of Veil Browser Agent.

Understand the user's browser automation request
and convert it into structured JSON.

User instruction:
{safe_instruction}

Return ONLY valid JSON with these fields:

{{
    "goal": "What the user wants to accomplish",
    "website": "Website to use, if mentioned or clearly identifiable, otherwise null",
    "location": "Location, if mentioned, otherwise null",
    "time_range": "Time range, if mentioned, otherwise null",
    "keywords": ["important", "search", "keywords"],
    "actions_required": ["main", "actions", "needed"]
}}

Do not add explanations.
Do not use Markdown.
Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = response.text.strip()

    result = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        result
    ).strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        return {
            "error": "Gemini returned invalid JSON"
        }