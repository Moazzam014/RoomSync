from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Rotation(Base):
    __tablename__ = "rotations"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    status = Column(
        String(30),
        default="assigned",
        nullable=False
    )

    assignment_reason = Column(
        String(255),
        nullable=True
    )

    assigned_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    is_completed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    room = relationship(
        "Room",
        back_populates="rotations"
    )

    member = relationship(
        "Member",
        back_populates="rotations"
    )

    task = relationship(
        "Task",
        back_populates="rotations"
    )