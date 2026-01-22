import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
