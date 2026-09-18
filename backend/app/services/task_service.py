from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(db: Session, task_data: TaskCreate):
    task = Task(
        name=task_data.name,
        description=task_data.description,
        frequency=task_data.frequency,
        room_id=task_data.room_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks_by_room(db: Session, room_id: int):
    return (
        db.query(Task)
        .filter(Task.room_id == room_id)
        .all()
    )


def get_task(db: Session, task_id: int):
    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def update_task(
    db: Session,
    task_id: int,
    name: str | None = None,
    description: str | None = None,
    frequency: str | None = None,
    is_active: bool | None = None,
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        return None

    if name is not None:
        task.name = name

    if description is not None:
        task.description = description

    if frequency is not None:
        task.frequency = frequency

    if is_active is not None:
        task.is_active = is_active

    db.commit()
    db.refresh(task)

    return task


def deactivate_task(db: Session, task_id: int):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        return None

    task.is_active = False

    db.commit()
    db.refresh(task)

    return task