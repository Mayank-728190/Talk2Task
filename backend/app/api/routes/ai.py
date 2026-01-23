from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
import io

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
from app.ai.providers.presenton_provider import generate_presentation_with_presenton

router = APIRouter()

# ================= REQUEST SCHEMAS =================

class AIGenerateRequest(BaseModel):
    room_name: str
    task: Literal["summary", "mom", "ppt", "flowchart"]
    provider: Literal["openai", "gemini"] = "openai"


class PPTExternalRequest(BaseModel):
    room_name: str
    provider: Literal["openai", "gemini"] = "openai"
    export_as: Literal["pdf", "pptx"] = "pptx"
    n_slides: int = 10  # Number of slides to generate
    template: str = "general"  # Template type
    tone: str = "professional"  # Presentation tone
    verbosity: str = "standard"  # Content verbosity


# ================= TEXT AI GENERATION =================

@router.post("/generate")
def generate_ai_output(req: AIGenerateRequest):
    transcript = merge_transcripts(req.room_name)

    if not transcript:
        return {"error": "No transcript available for this room"}

    context = build_base_context(req.room_name, transcript)

    if req.task == "summary":
        prompt = build_summary_prompt(context)
    elif req.task == "mom":
        prompt = build_mom_prompt(context)
    elif req.task == "ppt":
        prompt = build_ppt_prompt(context)
    elif req.task == "flowchart":
        prompt = build_flowchart_prompt(context)
    else:
        return {"error": "Invalid task"}

    output = (
        generate_openai(prompt)
        if req.provider == "openai"
        else generate_gemini(prompt)
    )

    return {
        "room": req.room_name,
        "task": req.task,
        "provider": req.provider,
        "output": output,
    }


# ================= PRESENTON PPT / PDF GENERATION =================

@router.post("/generate-ppt-external")
def generate_ppt_external(req: PPTExternalRequest):
    """
    ✅ Uses OpenAI / Gemini for content
    ✅ Uses Presenton.ai for slide generation
    ✅ Returns downloadable PDF or PPTX
    """

    transcript = merge_transcripts(req.room_name)

    if not transcript:
        raise ValueError("No transcript found for this room")

    context = build_base_context(req.room_name, transcript)

    # 🔹 AI produces a PROMPT for Presenton (not markdown structure)
    # The prompt should describe what the presentation should cover
    ppt_prompt = build_ppt_prompt(context)

    ai_content = (
        generate_openai(ppt_prompt)
        if req.provider == "openai"
        else generate_gemini(ppt_prompt)
    )

    # 🔹 Call Presenton with the correct parameter name: 'content'
    # Presenton generates the presentation from the content description
    file_bytes, content_type = generate_presentation_with_presenton(
        content=ai_content,  # Changed from prompt to content
        n_slides=req.n_slides,
        export_as=req.export_as,
        template=req.template,
        tone=req.tone,
        verbosity=req.verbosity,
        language="English",
    )

    filename = f"{req.room_name}.{req.export_as}"

    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type=content_type or "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )