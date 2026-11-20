
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.engine.eligibility_engine import get_eligible_members
from app.engine.fairness_engine import rank_members_by_fairness
from app.models.rotation import Rotation


def select_member(
    db: Session,
    room_id: int,
    task_id: int,
):
    eligible_members = get_eligible_members(
        db=db,
        room_id=room_id,
        task_id=task_id,
    )

    if not eligible_members:
        return None

    pending_rows = (
        db.query(
            Rotation.member_id,
            func.count(Rotation.id),
        )
        .filter(
            Rotation.room_id == room_id,
            Rotation.is_completed.is_(False),
        )
        .group_by(Rotation.member_id)
        .all()
    )

    pending_counts = {
        member_id: count
        for member_id, count in pending_rows
    }

    ranked_members = rank_members_by_fairness(
        eligible_members,
        pending_counts=pending_counts,
    )

    return ranked_members[0]
