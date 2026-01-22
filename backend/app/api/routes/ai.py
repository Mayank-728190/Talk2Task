from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.prompt_builder import (
    build_base_context,
    build_summary_prompt,
    build_mom_prompt,
    build_ppt_prompt,
    build_flowchart_prompt,
)
from app.ai.ai_router import merge_transcripts
from app.ai.providers.openai_provider import generate_openai
from app.ai.providers.gemini_provider import generate_gemini

router = APIRouter()


# ✅ Request body schema
class AIGenerateRequest(BaseModel):
    room_name: str
    task: str          # summary | mom | ppt | flowchart
    provider: str = "openai"  # openai | gemini


@router.post("/generate")
def generate_ai_output(payload: AIGenerateRequest):
    transcript = merge_transcripts(payload.room_name)
    context = build_base_context(payload.room_name, transcript)

    if payload.task == "summary":
        prompt = build_summary_prompt(context)
    elif payload.task == "mom":
        prompt = build_mom_prompt(context)
    elif payload.task == "ppt":
        prompt = build_ppt_prompt(context)
    elif payload.task == "flowchart":
        prompt = build_flowchart_prompt(context)
    else:
        return {"error": "Invalid task"}

    if payload.provider == "openai":
        result = generate_openai(prompt)
    else:
        result = generate_gemini(prompt)

    return {
        "room": payload.room_name,
        "task": payload.task,
        "provider": payload.provider,
        "output": result,
    }
