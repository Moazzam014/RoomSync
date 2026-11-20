
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.task_exemption import TaskExemption


def get_eligible_members(
    db: Session,
    room_id: int,
    task_id: int,
):
    members = (
        db.query(Member)
        .filter(
            Member.room_id == room_id,
            Member.is_active.is_(True),
        )
        .all()
    )

    exemptions = (
        db.query(TaskExemption)
        .filter(
            TaskExemption.task_id == task_id,
            TaskExemption.is_active.is_(True),
        )
        .all()
    )

    exempted_member_ids = {
        exemption.member_id
        for exemption in exemptions
    }

    return [
        member
        for member in members
        if member.id not in exempted_member_ids
    ]
