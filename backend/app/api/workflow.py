
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.engine.rotation_engine import assign_task
from app.models.member import Member
from app.models.rotation import Rotation
from app.models.user import User
from app.schemas.rotation import RotationResponse
from app.services.workflow_service import (
    get_room_workflow,
    get_active_rotations,
    complete_rotation,
)


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
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


@router.get("/room/{room_id}")
def get_workflow(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_room_membership(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    return get_room_workflow(
        db=db,
        room_id=room_id,
    )


@router.get(
    "/room/{room_id}/active",
    response_model=list[RotationResponse],
)
def get_active_workflow(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_room_membership(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    return get_active_rotations(
        db=db,
        room_id=room_id,
    )


@router.post(
    "/room/{room_id}/task/{task_id}/assign",
    response_model=RotationResponse,
)
def assign_workflow_task(
    room_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Any active room member can trigger assignment.
    verify_room_membership(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    rotation = assign_task(
        db=db,
        room_id=room_id,
        task_id=task_id,
    )

    if not rotation:
        raise HTTPException(
            status_code=404,
            detail=(
                "Task could not be assigned. "
                "Check task, room, members, "
                "eligibility and exemptions."
            ),
        )

    return rotation


@router.patch(
    "/rotation/{rotation_id}/complete",
    response_model=RotationResponse,
)
def complete_workflow_rotation(
    rotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rotation = (
        db.query(Rotation)
        .filter(Rotation.id == rotation_id)
        .first()
    )

    if not rotation:
        raise HTTPException(
            status_code=404,
            detail="Rotation not found.",
        )

    verify_room_membership(
        db=db,
        room_id=rotation.room_id,
        user_id=current_user.id,
    )

    assigned_member = (
        db.query(Member)
        .filter(
            Member.id == rotation.member_id,
            Member.room_id == rotation.room_id,
            Member.user_id == current_user.id,
            Member.is_active.is_(True),
        )
        .first()
    )

    if not assigned_member:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this task.",
        )

    completed_rotation = complete_rotation(
        db=db,
        rotation_id=rotation_id,
    )

    if not completed_rotation:
        raise HTTPException(
            status_code=404,
            detail="Rotation not found.",
        )

    return completed_rotation
