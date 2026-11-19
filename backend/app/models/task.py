
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.datetime_utils import utcnow_naive


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    frequency = Column(String(50), default="daily", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime,
        default=utcnow_naive,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=utcnow_naive,
        onupdate=utcnow_naive,
        nullable=False,
    )

    room = relationship("Room", back_populates="tasks")

    exemptions = relationship(
        "TaskExemption",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    rotations = relationship(
        "Rotation",
        back_populates="task",
        cascade="all, delete-orphan",
    )
