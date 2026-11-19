
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.member import Member
from app.models.presence import Presence
from app.models.user import User
from app.schemas.presence import PresenceCreate, PresenceResponse


router = APIRouter(
    prefix="/presence",
    tags=["Presence"],
)


def get_authorized_member(
    db: Session,
    member_id: int,
    user_id: int,
):
    member = (
        db.query(Member)
        .filter(Member.id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    # The requesting user must be an active member
    # of the same room.
    requester_membership = (
        db.query(Member)
        .filter(
            Member.room_id == member.room_id,
            Member.user_id == user_id,
            Member.is_active == True,
        )
        .first()
    )

    if not requester_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found or access denied.",
        )

    return member


@router.post(
    "/",
    response_model=PresenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_presence(
    presence_data: PresenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = (
        db.query(Member)
        .filter(
            Member.id == presence_data.member_id,
            Member.is_active == True,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active member not found.",
        )

    # A user can record presence only for their own account.
    if member.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own presence.",
        )

    presence = Presence(
        member_id=member.id,
        is_present=presence_data.is_present,
    )

    db.add(presence)
    db.commit()
    db.refresh(presence)

    return presence


@router.get(
    "/member/{member_id}",
    response_model=list[PresenceResponse],
)
def get_member_presence(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = get_authorized_member(
        db=db,
        member_id=member_id,
        user_id=current_user.id,
    )

    return (
        db.query(Presence)
        .filter(Presence.member_id == member.id)
        .order_by(Presence.recorded_at.desc())
        .all()
    )
