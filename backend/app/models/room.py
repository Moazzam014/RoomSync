from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    members = relationship(
        "Member",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    tasks = relationship(
        "Task",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    rotations = relationship(
        "Rotation",
        back_populates="room",
        cascade="all, delete-orphan"
    )