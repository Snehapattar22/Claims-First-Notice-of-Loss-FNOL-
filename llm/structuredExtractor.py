import os
import json
from google import genai

def extract_claim_details(text):
    api_key = os.getenv("GEMINI_API_KEY")
    print("GEMINI KEY LOADED (extractor):", bool(api_key))

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not loaded")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Extract insurance claim details and return STRICT JSON only.

Required fields:
- policy_number
- incident_type
- incident_date
- location
- description

Text:
{text}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",

        contents=prompt
    )

    raw = response.text.strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1

    return json.loads(raw[start:end])
