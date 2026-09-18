from datetime import datetime

from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.rotation import Rotation
from app.models.task import Task


def get_room_workflow(
    db: Session,
    room_id: int,
):
    tasks = (
        db.query(Task)
        .filter(
            Task.room_id == room_id,
            Task.is_active == True,
        )
        .all()
    )

    rotations = (
        db.query(Rotation)
        .filter(Rotation.room_id == room_id)
        .order_by(Rotation.assigned_at.desc())
        .all()
    )

    return {
        "room_id": room_id,
        "tasks": tasks,
        "rotations": rotations,
    }


def get_active_rotations(
    db: Session,
    room_id: int,
):
    return (
        db.query(Rotation)
        .filter(
            Rotation.room_id == room_id,
            Rotation.is_completed == False,
        )
        .order_by(Rotation.assigned_at.asc())
        .all()
    )


def complete_rotation(
    db: Session,
    rotation_id: int,
):
    rotation = (
        db.query(Rotation)
        .filter(Rotation.id == rotation_id)
        .first()
    )

    if not rotation:
        return None

    if rotation.is_completed:
        return rotation

    rotation.is_completed = True
    rotation.status = "completed"
    rotation.completed_at = datetime.utcnow()

    member = (
        db.query(Member)
        .filter(Member.id == rotation.member_id)
        .first()
    )

    if member:
        member.total_tasks_completed = (
            member.total_tasks_completed or 0
        ) + 1

    db.commit()
    db.refresh(rotation)

    return rotation