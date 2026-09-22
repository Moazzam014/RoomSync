from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.member import Member
from app.models.room import Room
from app.models.user import User


router = APIRouter(
    prefix="/my-rooms",
    tags=["My Rooms"],
)


@router.get("/")
def get_my_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    members = (
        db.query(Member)
        .filter(
            Member.user_id == current_user.id,
            Member.is_active == True,
        )
        .all()
    )

    rooms = []

    for member in members:
        room = (
            db.query(Room)
            .filter(Room.id == member.room_id)
            .first()
        )

        if room:
            active_members = (
                db.query(Member)
                .filter(
                    Member.room_id == room.id,
                    Member.is_active == True,
                )
                .count()
            )

            rooms.append(
                {
                    "id": room.id,
                    "name": room.name,
                    "description": room.description,
                    "member_count": active_members,
                    "capacity": 7,
                    "created_at": room.created_at,
                }
            )

    return rooms


@router.post("/")
def create_my_room(
    room_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    name = str(room_data.get("name", "")).strip()
    description = room_data.get("description")

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Room name is required.",
        )

    room = Room(
        name=name,
        description=description,
    )

    db.add(room)
    db.flush()

    owner = Member(
        name=current_user.full_name or current_user.username,
        room_id=room.id,
        user_id=current_user.id,
        is_active=True,
        is_irregular=False,
        total_tasks_completed=0,
    )

    db.add(owner)
    db.commit()
    db.refresh(room)

    return {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "member_count": 1,
        "capacity": 7,
        "created_at": room.created_at,
    }