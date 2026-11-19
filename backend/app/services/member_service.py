
from sqlalchemy.orm import Session

from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate


def create_member(
    db: Session,
    member_data: MemberCreate,
):
    member = Member(
        name=member_data.name,
        room_id=member_data.room_id,
        user_id=None,
        role="member",
        is_active=True,
        is_irregular=False,
        total_tasks_completed=0,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def get_member(
    db: Session,
    member_id: int,
):
    return (
        db.query(Member)
        .filter(Member.id == member_id)
        .first()
    )


def get_room_members(
    db: Session,
    room_id: int,
):
    return (
        db.query(Member)
        .filter(
            Member.room_id == room_id,
            Member.is_active.is_(True),
        )
        .order_by(Member.id)
        .all()
    )


def update_member(
    db: Session,
    member: Member,
    member_data: MemberUpdate,
):
    update_data = member_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)

    return member


def deactivate_member(
    db: Session,
    member: Member,
):
    member.is_active = False

    db.commit()
    db.refresh(member)

    return member
