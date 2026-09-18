from sqlalchemy.orm import Session

from app.engine.eligibility_engine import get_eligible_members
from app.engine.fairness_engine import rank_members_by_fairness


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

    ranked_members = rank_members_by_fairness(
        eligible_members
    )

    return ranked_members[0]