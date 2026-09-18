from sqlalchemy.orm import Session

from app.engine.assignment_engine import select_member
from app.models.rotation import Rotation
from app.models.task import Task


def assign_task(
    db: Session,
    room_id: int,
    task_id: int,
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.room_id == room_id,
            Task.is_active == True,
        )
        .first()
    )

    if not task:
        return None

    member = select_member(
        db=db,
        room_id=room_id,
        task_id=task_id,
    )

    if not member:
        return None

    rotation = Rotation(
        room_id=room_id,
        task_id=task_id,
        member_id=member.id,
        status="assigned",
        assignment_reason=(
            "Selected using eligibility and fairness rules."
        ),
        is_completed=False,
    )

    db.add(rotation)
    db.commit()
    db.refresh(rotation)

    return rotation