from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.meetings import router as meetings_router
from app.api.routes.livekit import router as livekit_router
from app.api.routes.transcripts import router as transcripts_router
from app.api.routes.stt_ws import router as stt_ws_router
from app.api.routes.ai import router as ai_router




api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(meetings_router, prefix="/meetings", tags=["Meetings"])
api_router.include_router(livekit_router, prefix="/livekit", tags=["LiveKit"])
api_router.include_router(transcripts_router, prefix="/transcripts", tags=["Transcripts"])
api_router.include_router(stt_ws_router, tags=["STT WebSocket"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI"])