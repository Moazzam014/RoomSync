
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.member import Member
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
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


def verify_room_membership(
    db: Session,
    room_id: int,
    user_id: int,
):
    membership = (
        db.query(Member)
        .filter(
            Member.room_id == room_id,
            Member.user_id == user_id,
            Member.is_active.is_(True),
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=404,
            detail="Room not found or access denied.",
        )

    return membership


def verify_room_owner(
    db: Session,
    room_id: int,
    user_id: int,
):
    membership = verify_room_membership(
        db=db,
        room_id=room_id,
        user_id=user_id,
    )

    if membership.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only the room owner can manage tasks.",
        )

    return membership


def get_authorized_task(
    db: Session,
    task_id: int,
    user_id: int,
):
    task = get_task(db, task_id)

    if not task or not task.is_active:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    verify_room_membership(
        db=db,
        room_id=task.room_id,
        user_id=user_id,
    )

    return task


def get_owner_authorized_task(
    db: Session,
    task_id: int,
    user_id: int,
):
    task = get_authorized_task(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

    verify_room_owner(
        db=db,
        room_id=task.room_id,
        user_id=user_id,
    )

    return task


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201,
)
def create_task_endpoint(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_room_owner(
        db=db,
        room_id=task_data.room_id,
        user_id=current_user.id,
    )

    return create_task(db, task_data)


@router.get(
    "/room/{room_id}",
    response_model=list[TaskResponse],
)
def get_room_tasks(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_room_membership(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    return get_tasks_by_room(db, room_id)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_authorized_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owner_authorized_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    return update_task(
        db=db,
        task_id=task_id,
        task_data=task_data,
    )


@router.delete(
    "/{task_id}",
    response_model=TaskResponse,
)
def deactivate_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owner_authorized_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    return deactivate_task(db, task_id)
