
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.member import Member
from app.models.user import User
from app.schemas.member import (
    MemberCreate,
    MemberResponse,
    MemberUpdate,
)
from app.services.member_service import (
    create_member,
    get_member,
    get_room_members,
    update_member,
    deactivate_member,
)


router = APIRouter(
    prefix="/members",
    tags=["Members"],
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found or access denied.",
        )

    return membership


def require_room_owner(
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the room owner can manage members.",
        )

    return membership


def get_authorized_member(
    db: Session,
    member_id: int,
    user_id: int,
):
    member = get_member(
        db=db,
        member_id=member_id,
    )

    if not member or not member.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    verify_room_membership(
        db=db,
        room_id=member.room_id,
        user_id=user_id,
    )

    return member


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member_endpoint(
    member_data: MemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_room_owner(
        db=db,
        room_id=member_data.room_id,
        user_id=current_user.id,
    )

    return create_member(
        db=db,
        member_data=member_data,
    )


@router.get(
    "/room/{room_id}",
    response_model=list[MemberResponse],
)
def get_room_members_endpoint(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_room_membership(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
    )

    return get_room_members(
        db=db,
        room_id=room_id,
    )


@router.get(
    "/{member_id}",
    response_model=MemberResponse,
)
def get_member_endpoint(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_authorized_member(
        db=db,
        member_id=member_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{member_id}",
    response_model=MemberResponse,
)
def update_member_endpoint(
    member_id: int,
    member_data: MemberUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = get_authorized_member(
        db=db,
        member_id=member_id,
        user_id=current_user.id,
    )

    require_room_owner(
        db=db,
        room_id=member.room_id,
        user_id=current_user.id,
    )

    return update_member(
        db=db,
        member=member,
        member_data=member_data,
    )


@router.delete(
    "/{member_id}",
    response_model=MemberResponse,
)
def deactivate_member_endpoint(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = get_authorized_member(
        db=db,
        member_id=member_id,
        user_id=current_user.id,
    )

    require_room_owner(
        db=db,
        room_id=member.room_id,
        user_id=current_user.id,
    )

    if member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The room owner cannot be removed.",
        )

    return deactivate_member(
        db=db,
        member=member,
    )
