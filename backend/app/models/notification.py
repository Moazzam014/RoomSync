
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.datetime_utils import utcnow_naive


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String(150), nullable=False)
    message = Column(String(500), nullable=False)

    notification_type = Column(
        String(50),
        default="task_assignment",
        nullable=False,
    )

    is_read = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime,
        default=utcnow_naive,
        nullable=False,
    )

    member = relationship(
        "Member",
        back_populates="notifications",
    )
