from fastapi import APIRouter
from app.schemas.livekit import LiveKitTokenRequest, LiveKitTokenResponse
from app.services.livekit_service import create_access_token
from app.core.config import settings

router = APIRouter()


@router.post("/token", response_model=LiveKitTokenResponse)
def get_token(payload: LiveKitTokenRequest):
    token = create_access_token(
        room_name=payload.room_name,
        identity=payload.identity,
        name=payload.name,
    )

    return LiveKitTokenResponse(token=token, livekit_url=settings.LIVEKIT_URL)
