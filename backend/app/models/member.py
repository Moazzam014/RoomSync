
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.datetime_utils import utcnow_naive


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    role = Column(
        String(20),
        default="member",
        server_default="member",
        nullable=False,
    )

    is_active = Column(Boolean, default=True, nullable=False)
    is_irregular = Column(Boolean, default=False, nullable=False)
    total_tasks_completed = Column(Integer, default=0, nullable=False)

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

    room = relationship("Room", back_populates="members")
    user = relationship("User")

    presences = relationship(
        "Presence",
        back_populates="member",
        cascade="all, delete-orphan",
    )

    rotations = relationship(
        "Rotation",
        back_populates="member",
        cascade="all, delete-orphan",
    )

    task_exemptions = relationship(
        "TaskExemption",
        back_populates="member",
        cascade="all, delete-orphan",
    )

    notifications = relationship(
        "Notification",
        back_populates="member",
        cascade="all, delete-orphan",
    )
