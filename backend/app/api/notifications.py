from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.notification_service import (
    get_member_notifications,
    mark_notification_read,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


def get_db():
    return SessionLocal()


@router.get("/member/{member_id}")
def get_notifications(member_id: int):
    db: Session = get_db()

    try:
        return get_member_notifications(
            db=db,
            member_id=member_id,
        )

    finally:
        db.close()


@router.patch("/{notification_id}/read")
def read_notification(notification_id: int):
    db: Session = get_db()

    try:
        notification = mark_notification_read(
            db=db,
            notification_id=notification_id,
        )

        if not notification:
            raise HTTPException(
                status_code=404,
                detail="Notification not found",
            )

        return notification

    finally:
        db.close()