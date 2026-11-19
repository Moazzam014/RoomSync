
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.datetime_utils import utcnow_naive


class RoomInvitation(Base):
    __tablename__ = "room_invitations"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(
        Integer,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    inviter_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    invitee_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status = Column(String(20), default="pending", nullable=False)

    created_at = Column(
        DateTime,
        default=utcnow_naive,
        nullable=False,
    )

    responded_at = Column(DateTime, nullable=True)

    room = relationship("Room")

    inviter = relationship(
        "User",
        foreign_keys=[inviter_id],
    )

    invitee = relationship(
        "User",
        foreign_keys=[invitee_id],
    )
