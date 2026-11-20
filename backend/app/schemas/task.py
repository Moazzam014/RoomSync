
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    frequency: str = Field(default="daily", min_length=1, max_length=50)
    room_id: int = Field(gt=0)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class TaskUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    frequency: str | None = Field(default=None, min_length=1, max_length=50)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_update_fields(cls, values):
        if not isinstance(values, dict) or not values:
            raise ValueError("At least one field must be provided.")

        for field in ("name", "frequency"):
            if field in values and values[field] is None:
                raise ValueError(f"{field} cannot be null.")

        return values


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
