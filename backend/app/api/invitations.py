from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.member import Member
from app.models.room import Room
from app.models.room_invitation import RoomInvitation
from app.models.user import User
from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
)


router = APIRouter(
    prefix="/invitations",
    tags=["Room Invitations"],
)


@router.post(
    "/",
    response_model=InvitationResponse,
)
def send_invitation(
    data: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = (
        db.query(Room)
        .filter(Room.id == data.room_id)
        .first()
    )

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found.",
        )

    invitee_username = data.invitee_username.strip()

    invitee = (
        db.query(User)
        .filter(
            User.username == invitee_username
        )
        .first()
    )

    if not invitee:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    if invitee.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot invite yourself.",
        )

    # Check if user is already a member
    existing_member = (
        db.query(Member)
        .filter(
            Member.room_id == room.id,
            Member.user_id == invitee.id,
            Member.is_active == True,
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this room.",
        )

    # Room capacity
    active_member_count = (
        db.query(Member)
        .filter(
            Member.room_id == room.id,
            Member.is_active == True,
        )
        .count()
    )

    if active_member_count >= 7:
        raise HTTPException(
            status_code=400,
            detail="This room has reached its maximum capacity of 7 members.",
        )

    # Check existing pending invitation
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
            status_code=400,
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
    invitations = (
        db.query(RoomInvitation)
        .filter(
            RoomInvitation.invitee_id == current_user.id,
            RoomInvitation.status == "pending",
        )
        .order_by(
            RoomInvitation.created_at.desc()
        )
        .all()
    )

    return invitations


@router.patch(
    "/{invitation_id}/accept",
    response_model=InvitationResponse,
)
def accept_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invitation = (
        db.query(RoomInvitation)
        .filter(
            RoomInvitation.id == invitation_id,
        )
        .first()
    )

    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Invitation not found.",
        )

    if invitation.invitee_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="This invitation does not belong to you.",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Invitation is no longer pending.",
        )

    existing_member = (
        db.query(Member)
        .filter(
            Member.room_id == invitation.room_id,
            Member.user_id == current_user.id,
        )
        .first()
    )

    if existing_member:
        existing_member.is_active = True
    else:
        member = Member(
            name=(
                current_user.full_name
                or current_user.username
            ),
            room_id=invitation.room_id,
            user_id=current_user.id,
            is_active=True,
            is_irregular=False,
            total_tasks_completed=0,
        )

        db.add(member)

    invitation.status = "accepted"
    invitation.responded_at = datetime.utcnow()

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
        .filter(
            RoomInvitation.id == invitation_id,
        )
        .first()
    )

    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Invitation not found.",
        )

    if invitation.invitee_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="This invitation does not belong to you.",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Invitation is no longer pending.",
        )

    invitation.status = "declined"
    invitation.responded_at = datetime.utcnow()

    db.commit()
    db.refresh(invitation)

    return invitation