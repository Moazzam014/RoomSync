
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.core.datetime_utils import utcnow_naive
from app.models.member import Member
from app.models.room import Room
from app.models.room_invitation import RoomInvitation
from app.models.user import User
from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
)
from app.services.room_service import get_active_member


router = APIRouter(
    prefix="/invitations",
    tags=["Room Invitations"],
)


def get_locked_room(
    db: Session,
    room_id: int,
) -> Room:
    room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .with_for_update()
        .populate_existing()
        .first()
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )

    return room


def verify_room_owner(
    db: Session,
    room_id: int,
    user_id: int,
) -> Member:
    member = get_active_member(
        db=db,
        room_id=room_id,
        user_id=user_id,
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )

    if member.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the room owner can send invitations.",
        )

    return member


@router.post(
    "/",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_invitation(
    data: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = get_locked_room(
        db=db,
        room_id=data.room_id,
    )

    verify_room_owner(
        db=db,
        room_id=room.id,
        user_id=current_user.id,
    )

    invitee = (
        db.query(User)
        .filter(
            User.username == data.invitee_username,
            User.is_active.is_(True),
        )
        .first()
    )

    if not invitee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if invitee.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot invite yourself.",
        )

    existing_member = (
        db.query(Member)
        .filter(
            Member.room_id == room.id,
            Member.user_id == invitee.id,
            Member.is_active.is_(True),
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this room.",
        )

    existing_invitation = (
        db.query(RoomInvitation)
        .filter(
            RoomInvitation.room_id == room.id,
            RoomInvitation.invitee_id == invitee.id,
            RoomInvitation.status == "pending",
        )
        .first()
    )

    if existing_invitation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation already pending.",
        )

    invitation = RoomInvitation(
        room_id=room.id,
        inviter_id=current_user.id,
        invitee_id=invitee.id,
        status="pending",
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return invitation


@router.get(
    "/me",
    response_model=list[InvitationResponse],
)
def get_my_invitations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(RoomInvitation)
        .filter(
            RoomInvitation.invitee_id == current_user.id,
            RoomInvitation.status == "pending",
        )
        .order_by(RoomInvitation.created_at.desc())
        .all()
    )


@router.patch(
    "/{invitation_id}/accept",
    response_model=InvitationResponse,
)
def accept_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invitation_reference = (
        db.query(RoomInvitation)
        .filter(RoomInvitation.id == invitation_id)
        .first()
    )

    if not invitation_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found.",
        )

    if invitation_reference.invitee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation does not belong to you.",
        )

    # Lock order: room first, then invitation.
    room = get_locked_room(
        db=db,
        room_id=invitation_reference.room_id,
    )

    invitation = (
        db.query(RoomInvitation)
        .filter(
            RoomInvitation.id == invitation_id,
            RoomInvitation.room_id == room.id,
        )
        .with_for_update()
        .populate_existing()
        .first()
    )

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found.",
        )

    if invitation.invitee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation does not belong to you.",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation is no longer pending.",
        )

    existing_member = (
        db.query(Member)
        .filter(
            Member.room_id == room.id,
            Member.user_id == current_user.id,
        )
        .first()
    )

    if existing_member and existing_member.is_active:
        invitation.status = "accepted"
        invitation.responded_at = utcnow_naive()

        db.commit()
        db.refresh(invitation)

        return invitation

    if existing_member:
        existing_member.is_active = True
        existing_member.role = "member"
    else:
        db.add(
            Member(
                name=current_user.full_name or current_user.username,
                room_id=room.id,
                user_id=current_user.id,
                role="member",
                is_active=True,
                is_irregular=False,
                total_tasks_completed=0,
            )
        )

    invitation.status = "accepted"
    invitation.responded_at = utcnow_naive()

    db.commit()
    db.refresh(invitation)

    return invitation


@router.patch(
    "/{invitation_id}/decline",
    response_model=InvitationResponse,
)
def decline_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invitation = (
        db.query(RoomInvitation)
        .filter(RoomInvitation.id == invitation_id)
        .with_for_update()
        .populate_existing()
        .first()
    )

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found.",
        )

    if invitation.invitee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation does not belong to you.",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation is no longer pending.",
        )

    invitation.status = "declined"
    invitation.responded_at = utcnow_naive()

    db.commit()
    db.refresh(invitation)

    return invitation
