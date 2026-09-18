from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.room import Room
from app.schemas.member import MemberCreate, MemberResponse, MemberUpdate
from app.services import member_service


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED
)
def create_member(
    member_data: MemberCreate,
    db: Session = Depends(get_db)
):
    room = (
        db.query(Room)
        .filter(Room.id == member_data.room_id)
        .first()
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    return member_service.create_member(
        db=db,
        member_data=member_data
    )


@router.get(
    "/room/{room_id}",
    response_model=list[MemberResponse]
)
def get_room_members(
    room_id: int,
    db: Session = Depends(get_db)
):
    room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    return member_service.get_room_members(
        db=db,
        room_id=room_id
    )


@router.get(
    "/{member_id}",
    response_model=MemberResponse
)
def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = member_service.get_member(
        db=db,
        member_id=member_id
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    return member


@router.patch(
    "/{member_id}",
    response_model=MemberResponse
)
def update_member(
    member_id: int,
    member_data: MemberUpdate,
    db: Session = Depends(get_db)
):
    member = member_service.get_member(
        db=db,
        member_id=member_id
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    return member_service.update_member(
        db=db,
        member=member,
        member_data=member_data
    )


@router.delete(
    "/{member_id}",
    response_model=MemberResponse
)
def deactivate_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = member_service.get_member(
        db=db,
        member_id=member_id
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    return member_service.deactivate_member(
        db=db,
        member=member
    )