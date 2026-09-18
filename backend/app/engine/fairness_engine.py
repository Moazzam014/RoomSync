def calculate_fairness_score(member):
    """
    Lower score means the member has received
    fewer completed tasks and should get priority.
    """

    completed_tasks = member.total_tasks_completed or 0

    irregular_penalty = 0

    if member.is_irregular:
        irregular_penalty = 100

    return completed_tasks + irregular_penalty


def rank_members_by_fairness(members):
    return sorted(
        members,
        key=calculate_fairness_score,
    )