
from sqlalchemy.orm import Session

from app.engine.assignment_engine import select_member
from app.models.rotation import Rotation
from app.models.task import Task


def assign_task(
    db: Session,
    room_id: int,
    task_id: int,
):
    # PostgreSQL SELECT FOR UPDATE locks this task row.
    # Another assignment request for the same task must wait
    # until this transaction finishes.
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.room_id == room_id,
            Task.is_active.is_(True),
        )
        .with_for_update()
        .first()
    )

    if not task:
        return None

    # Check for an existing incomplete assignment after
    # acquiring the task lock.
    existing_rotation = (
        db.query(Rotation)
        .filter(
            Rotation.room_id == room_id,
            Rotation.task_id == task_id,
            Rotation.is_completed.is_(False),
        )
        .order_by(Rotation.assigned_at.asc())
        .first()
    )

    if existing_rotation:
        return existing_rotation

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
            "Selected using eligibility, pending workload "
            "and fairness rules."
        ),
        is_completed=False,
    )

    db.add(rotation)
    db.commit()
    db.refresh(rotation)

    return rotation
