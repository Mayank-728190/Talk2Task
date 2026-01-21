from fastapi import APIRouter
from app.services.transcript_store import get_room_logs, get_user_logs

router = APIRouter()


@router.get("/{room_name}")
def fetch_room_transcripts(room_name: str):
    return {"room": room_name, "users": get_room_logs(room_name)}


@router.get("/{room_name}/{speaker_id}")
def fetch_user_transcripts(room_name: str, speaker_id: str):
    return {"room": room_name, "speaker_id": speaker_id, "logs": get_user_logs(room_name, speaker_id)}
