from pydantic import BaseModel


class CreateMeetingRequest(BaseModel):
    title: str
    host_name: str


class CreateMeetingResponse(BaseModel):
    meeting_id: str
    room_name: str
    join_url: str
