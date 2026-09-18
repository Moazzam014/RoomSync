from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoomBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Room 302"]
    )

    description: str | None = Field(
        default=None,
        max_length=255,
        examples=["Room management and task rotation"]
    )


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )