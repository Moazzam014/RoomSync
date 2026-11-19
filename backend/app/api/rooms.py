
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.room import (
    RoomCreate,
    RoomResponse,
    RoomUpdate,
)
from app.services import room_service


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


def require_room_member(
    db: Session,
    room_id: int,
    user_id: int,
):
    member = room_service.get_active_member(
        db=db,
        room_id=room_id,
        user_id=user_id,
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )

    return member


def require_room_owner(
    db: Session,
    room_id: int,
    user_id: int,
):
    member = require_room_member(
        db=db,
        room_id=room_id,
        user_id=user_id,
    )

    if member.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the room owner can perform this action.",
        )

    return member


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return room_service.create_room(
        db=db,
        room_data=room_data,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[RoomResponse],
)
def get_my_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return room_service.get_user_rooms(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{room_id}",
    response_model=RoomResponse,
)
def get_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_room_member(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    room = room_service.get_room(
        db=db,
        room_id=room_id,
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )

    return room


@router.patch(
    "/{room_id}",
    response_model=RoomResponse,
)
def update_room(
    room_id: int,
    room_data: RoomUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_room_owner(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    room = room_service.get_room(
        db=db,
        room_id=room_id,
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )

    return room_service.update_room(
        db=db,
        room=room,
        room_data=room_data,
    )


@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_room_owner(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    room = room_service.get_room(
        db=db,
        room_id=room_id,
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )

    room_service.delete_room(
        db=db,
        room=room,
    )

    return None
