from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.presence import Presence
from app.schemas.presence import PresenceCreate, PresenceResponse


router = APIRouter(
    prefix="/presence",
    tags=["Presence"],
)


def get_db():
    return SessionLocal()


@router.post(
    "/",
    response_model=PresenceResponse,
    status_code=201,
)
def create_presence(presence_data: PresenceCreate):
    db: Session = get_db()

    try:
        presence = Presence(
            member_id=presence_data.member_id,
            is_present=presence_data.is_present,
        )

        db.add(presence)
        db.commit()
        db.refresh(presence)

        return presence

    finally:
        db.close()


@router.get(
    "/member/{member_id}",
    response_model=list[PresenceResponse],
)
def get_member_presence(member_id: int):
    db: Session = get_db()

    try:
        return (
            db.query(Presence)
            .filter(Presence.member_id == member_id)
            .order_by(Presence.recorded_at.desc())
            .all()
        )

    finally:
        db.close()