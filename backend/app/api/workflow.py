from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.engine.rotation_engine import assign_task
from app.services.workflow_service import (
    get_room_workflow,
    get_active_rotations,
    complete_rotation,
)
from app.schemas.rotation import RotationResponse


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
)


def get_db():
    return SessionLocal()


@router.get(
    "/room/{room_id}",
)
def get_workflow(room_id: int):
    db: Session = get_db()

    try:
        return get_room_workflow(
            db=db,
            room_id=room_id,
        )

    finally:
        db.close()


@router.get(
    "/room/{room_id}/active",
    response_model=list[RotationResponse],
)
def get_active_workflow(room_id: int):
    db: Session = get_db()

    try:
        return get_active_rotations(
            db=db,
            room_id=room_id,
        )

    finally:
        db.close()


@router.post(
    "/room/{room_id}/task/{task_id}/assign",
    response_model=RotationResponse,
)
def assign_workflow_task(
    room_id: int,
    task_id: int,
):
    db: Session = get_db()

    try:
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

    finally:
        db.close()


@router.patch(
    "/rotation/{rotation_id}/complete",
    response_model=RotationResponse,
)
def complete_workflow_rotation(
    rotation_id: int,
):
    db: Session = get_db()

    try:
        rotation = complete_rotation(
            db=db,
            rotation_id=rotation_id,
        )

        if not rotation:
            raise HTTPException(
                status_code=404,
                detail="Rotation not found",
            )

        return rotation

    finally:
        db.close()