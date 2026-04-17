import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="say hello in JSON",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    print("[SUCCESS] gemini-2.5-flash", response.text)
except Exception as e:
    print("[FAILED] gemini-2.5-flash", e)

try:
    response = client.models.generate_content(
        model='gemini-flash-lite-latest',
        contents="say hello in JSON",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    print("[SUCCESS] gemini-flash-lite-latest", response.text)
except Exception as e:
    print("[FAILED] gemini-flash-lite-latest", e)
