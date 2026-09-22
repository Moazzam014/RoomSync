from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InvitationCreate(BaseModel):
    room_id: int
    invitee_username: str


class InvitationResponse(BaseModel):
    id: int
    room_id: int
    inviter_id: int
    invitee_id: int
    status: str
    created_at: datetime
    responded_at: datetime | None

    model_config = ConfigDict(from_attributes=True)