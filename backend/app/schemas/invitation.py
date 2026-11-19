
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InvitationCreate(BaseModel):
    room_id: int = Field(gt=0)
    invitee_username: str = Field(
        min_length=1,
        max_length=50,
    )

    @field_validator("invitee_username")
    @classmethod
    def clean_username(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty.")

        return value


class InvitationResponse(BaseModel):
    id: int
    room_id: int
    inviter_id: int
    invitee_id: int
    status: str
    created_at: datetime
    responded_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
