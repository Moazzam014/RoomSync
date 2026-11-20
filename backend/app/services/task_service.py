
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
):
    task = Task(
        name=task_data.name,
        description=task_data.description,
        frequency=task_data.frequency,
        room_id=task_data.room_id,
        is_active=True,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks_by_room(
    db: Session,
    room_id: int,
):
    return (
        db.query(Task)
        .filter(
            Task.room_id == room_id,
            Task.is_active.is_(True),
        )
        .order_by(Task.created_at.desc())
        .all()
    )


def get_task(
    db: Session,
    task_id: int,
):
    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
):
    task = get_task(db, task_id)

    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def deactivate_task(
    db: Session,
    task_id: int,
):
    task = get_task(db, task_id)

    if not task:
        return None

    task.is_active = False

    db.commit()
    db.refresh(task)

    return task
