from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RotationCreate(BaseModel):
    room_id: int
    task_id: int
    member_id: int
    assignment_reason: str | None = None


class RotationResponse(BaseModel):
    id: int
    room_id: int
    task_id: int
    member_id: int
    status: str
    assignment_reason: str | None
    assigned_at: datetime
    completed_at: datetime | None
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


class RotationComplete(BaseModel):
    is_completed: bool = True