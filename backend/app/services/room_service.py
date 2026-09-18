from sqlalchemy.orm import Session

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate


def create_room(
    db: Session,
    room_data: RoomCreate
) -> Room:

    new_room = Room(
        name=room_data.name,
        description=room_data.description
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


def get_room(
    db: Session,
    room_id: int
) -> Room | None:

    return (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )


def get_all_rooms(
    db: Session
) -> list[Room]:

    return (
        db.query(Room)
        .order_by(Room.created_at.desc())
        .all()
    )


def update_room(
    db: Session,
    room: Room,
    room_data: RoomUpdate
) -> Room:

    update_data = room_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)

    return room


def delete_room(
    db: Session,
    room: Room
) -> None:

    db.delete(room)
    db.commit()