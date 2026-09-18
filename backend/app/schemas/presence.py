from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PresenceCreate(BaseModel):
    member_id: int
    is_present: bool = True


class PresenceResponse(BaseModel):
    id: int
    member_id: int
    is_present: bool
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)