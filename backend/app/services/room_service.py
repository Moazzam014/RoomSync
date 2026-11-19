
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.room import Room
from app.models.user import User
from app.schemas.room import RoomCreate, RoomUpdate


def create_room(
    db: Session,
    room_data: RoomCreate,
    current_user: User,
) -> Room:
    new_room = Room(
        name=room_data.name,
        description=room_data.description,
    )

    db.add(new_room)
    db.flush()

    creator_member = Member(
        name=current_user.full_name or current_user.username,
        room_id=new_room.id,
        user_id=current_user.id,
        role="owner",
        is_active=True,
        is_irregular=False,
        total_tasks_completed=0,
    )

    db.add(creator_member)
    db.commit()
    db.refresh(new_room)

    return new_room


def get_room(
    db: Session,
    room_id: int,
) -> Room | None:
    return (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )


def get_active_member(
    db: Session,
    room_id: int,
    user_id: int,
) -> Member | None:
    return (
        db.query(Member)
        .filter(
            Member.room_id == room_id,
            Member.user_id == user_id,
            Member.is_active.is_(True),
        )
        .first()
    )


def get_user_rooms(
    db: Session,
    user_id: int,
) -> list[Room]:
    return (
        db.query(Room)
        .join(Member, Member.room_id == Room.id)
        .filter(
            Member.user_id == user_id,
            Member.is_active.is_(True),
        )
        .order_by(Room.created_at.desc())
        .all()
    )


def get_all_rooms(
    db: Session,
) -> list[Room]:
    return (
        db.query(Room)
        .order_by(Room.created_at.desc())
        .all()
    )


def update_room(
    db: Session,
    room: Room,
    room_data: RoomUpdate,
) -> Room:
    update_data = room_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)

    return room


def delete_room(
    db: Session,
    room: Room,
) -> None:
    db.delete(room)
    db.commit()
