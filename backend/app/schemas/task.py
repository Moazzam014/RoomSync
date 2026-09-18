from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    frequency: str = "daily"
    room_id: int


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str | None
    frequency: str
    room_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)