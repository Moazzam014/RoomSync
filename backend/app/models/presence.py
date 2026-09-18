from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Presence(Base):
    __tablename__ = "presence"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    is_present = Column(
        Boolean,
        default=True,
        nullable=False
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    member = relationship(
        "Member",
        back_populates="presences"
    )