
import json
import re

from ai_service import client
from pii_detector import detect_pii
from pii_handler import redact_pii


def create_plan(task):
    # Convert task to text and mask detected PII locally.
    task_text = json.dumps(task, ensure_ascii=False)
    pii = detect_pii(task_text)
    safe_task = redact_pii(task_text, pii)

    prompt = f"""
You are the planning module of Veil Browser Agent.

Convert the understood user task into a simple,
structured browser action plan.

User task:
{safe_task}

Return ONLY valid JSON in this format:

{{
    "task": "short task name",
    "actions": [
        {{
            "action": "navigate",
            "target": "website or URL"
        }},
        {{
            "action": "click",
            "target": "element"
        }},
        {{
            "action": "type",
            "target": "input field",
            "value": "text"
        }}
    ],
    "expected_url": "optional URL fragment",
    "expected_text": "optional text to verify"
}}

Rules:
- Do not execute anything.
- Only create the plan.
- Use only the actions shown above.
- Include expected_url or expected_text only when
  the expected result is reasonably clear.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove optional Markdown JSON fences.
    response_text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response_text,
        flags=re.IGNORECASE
    ).strip()

    return json.loads(response_text)