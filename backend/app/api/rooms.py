from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.services import room_service


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED
)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db)
):
    return room_service.create_room(
        db=db,
        room_data=room_data
    )


@router.get(
    "/",
    response_model=list[RoomResponse]
)
def get_all_rooms(
    db: Session = Depends(get_db)
):
    return room_service.get_all_rooms(db)


@router.get(
    "/{room_id}",
    response_model=RoomResponse
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    room = room_service.get_room(
        db=db,
        room_id=room_id
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    return room


@router.patch(
    "/{room_id}",
    response_model=RoomResponse
)
def update_room(
    room_id: int,
    room_data: RoomUpdate,
    db: Session = Depends(get_db)
):
    room = room_service.get_room(
        db=db,
        room_id=room_id
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    return room_service.update_room(
        db=db,
        room=room,
        room_data=room_data
    )


@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    room = room_service.get_room(
        db=db,
        room_id=room_id
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    room_service.delete_room(
        db=db,
        room=room
    )