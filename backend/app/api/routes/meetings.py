import uuid
from fastapi import APIRouter
from app.schemas.meeting import CreateMeetingRequest, CreateMeetingResponse
from app.core.config import settings

router = APIRouter()


@router.post("/create", response_model=CreateMeetingResponse)
def create_meeting(payload: CreateMeetingRequest):
    meeting_id = str(uuid.uuid4())
    room_name = f"room-{meeting_id[:8]}"

    join_url = f"{settings.FRONTEND_URL}/meeting/{room_name}?name={payload.host_name}"

    return CreateMeetingResponse(
        meeting_id=meeting_id,
        room_name=room_name,
        join_url=join_url,
    )
