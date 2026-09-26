import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


def ask_ai(safe_text):

    prompt = f"""
You are Veil Browser Agent.

Understand the following SAFE webpage information.
The information has already been processed to remove sensitive PII.

Webpage information:
{safe_text}

Explain what task the user appears to want to perform.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text