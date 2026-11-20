
def calculate_fairness_score(member, pending_tasks=0):
    """
    Lower score means the member has received less total workload.

    Total workload includes:
    - Completed tasks
    - Pending assignments
    - Irregular member penalty
    """

    completed_tasks = member.total_tasks_completed or 0

    irregular_penalty = 100 if member.is_irregular else 0

    return (
        completed_tasks
        + pending_tasks
        + irregular_penalty
    )


def rank_members_by_fairness(members, pending_counts=None):
    """
    Rank eligible members by total workload.

    pending_counts maps member IDs to their incomplete
    rotation counts.

    Existing callers can still use this function with
    only the members argument.
    """

    pending_counts = pending_counts or {}

    return sorted(
        members,
        key=lambda member: (
            calculate_fairness_score(
                member,
                pending_counts.get(
                    getattr(member, "id", None),
                    0,
                ),
            ),
            getattr(member, "id", 0) or 0,
        ),
    )
