from sqlalchemy.orm import Session

from app.models.notification import Notification


def create_notification(
    db: Session,
    member_id: int,
    title: str,
    message: str,
    notification_type: str = "task_assignment",
):
    notification = Notification(
        member_id=member_id,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_member_notifications(
    db: Session,
    member_id: int,
):
    return (
        db.query(Notification)
        .filter(Notification.member_id == member_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_notification_read(
    db: Session,
    notification_id: int,
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        return None

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification