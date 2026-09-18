from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import (
    create_task,
    get_tasks_by_room,
    get_task,
    update_task,
    deactivate_task,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_db():
    db = SessionLocal()

    try:
        return db
    except Exception:
        db.close()
        raise


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task_endpoint(task_data: TaskCreate):
    db: Session = get_db()

    try:
        return create_task(db, task_data)
    finally:
        db.close()


@router.get("/room/{room_id}", response_model=list[TaskResponse])
def get_room_tasks(room_id: int):
    db: Session = get_db()

    try:
        return get_tasks_by_room(db, room_id)
    finally:
        db.close()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int):
    db: Session = get_db()

    try:
        task = get_task(db, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return task
    finally:
        db.close()


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    name: str | None = None,
    description: str | None = None,
    frequency: str | None = None,
    is_active: bool | None = None,
):
    db: Session = get_db()

    try:
        task = update_task(
            db=db,
            task_id=task_id,
            name=name,
            description=description,
            frequency=frequency,
            is_active=is_active,
        )

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return task
    finally:
        db.close()


@router.delete("/{task_id}", response_model=TaskResponse)
def deactivate_task_endpoint(task_id: int):
    db: Session = get_db()

    try:
        task = deactivate_task(db, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return task
    finally:
        db.close()