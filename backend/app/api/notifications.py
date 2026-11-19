from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.member import Member
from app.models.notification import Notification
from app.models.user import User
from app.services.notification_service import (
    get_member_notifications,
    mark_notification_read,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


def get_authorized_member(db: Session, member_id: int, user_id: int):
    member = db.query(Member).filter(
        Member.id == member_id,
        Member.user_id == user_id,
        Member.is_active == True,
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found or access denied.",
        )

    return member


@router.get("/member/{member_id}")
def get_notifications(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_authorized_member(db, member_id, current_user.id)

    return get_member_notifications(
        db=db,
        member_id=member_id,
    )


@router.patch("/{notification_id}/read")
def read_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found.",
        )

    get_authorized_member(
        db,
        notification.member_id,
        current_user.id,
    )

    return mark_notification_read(
        db=db,
        notification_id=notification_id,
    )