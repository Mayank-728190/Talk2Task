from pydantic import BaseModel


class LiveKitTokenRequest(BaseModel):
    room_name: str
    identity: str
    name: str


class LiveKitTokenResponse(BaseModel):
    token: str
    livekit_url: str
