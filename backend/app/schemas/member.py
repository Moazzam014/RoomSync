from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MemberBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )


class MemberCreate(MemberBase):
    room_id: int


class MemberUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )


class MemberResponse(MemberBase):
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )