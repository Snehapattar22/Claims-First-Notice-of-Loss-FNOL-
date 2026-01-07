import os
from google import genai

def empathetic_response(user_message):
    api_key = os.getenv("GEMINI_API_KEY")
    print("GEMINI KEY LOADED INSIDE FUNCTION:", bool(api_key))

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not loaded")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an empathetic insurance FNOL assistant.
Respond calmly and guide the user step by step.

User message:
{user_message}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",

        contents=prompt
    )

    return response.text
