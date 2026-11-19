
from types import SimpleNamespace

from app.engine.fairness_engine import (
    calculate_fairness_score,
    rank_members_by_fairness,
)


def test_member_with_fewer_completed_tasks_gets_lower_score():
    member_one = SimpleNamespace(
        total_tasks_completed=2,
        is_irregular=False,
    )
    member_two = SimpleNamespace(
        total_tasks_completed=5,
        is_irregular=False,
    )

    assert calculate_fairness_score(member_one) == 2
    assert calculate_fairness_score(member_two) == 5


def test_irregular_member_gets_100_point_penalty():
    member = SimpleNamespace(
        total_tasks_completed=2,
        is_irregular=True,
    )

    assert calculate_fairness_score(member) == 102


def test_regular_member_gets_priority_over_irregular_member():
    regular_member = SimpleNamespace(
        total_tasks_completed=5,
        is_irregular=False,
    )
    irregular_member = SimpleNamespace(
        total_tasks_completed=0,
        is_irregular=True,
    )

    ranked = rank_members_by_fairness(
        [irregular_member, regular_member]
    )

    assert ranked[0] is regular_member
    assert ranked[1] is irregular_member


def test_members_are_ranked_by_fairness_score():
    member_one = SimpleNamespace(
        total_tasks_completed=8,
        is_irregular=False,
    )
    member_two = SimpleNamespace(
        total_tasks_completed=2,
        is_irregular=False,
    )
    member_three = SimpleNamespace(
        total_tasks_completed=5,
        is_irregular=False,
    )

    ranked = rank_members_by_fairness(
        [member_one, member_two, member_three]
    )

    assert ranked == [
        member_two,
        member_three,
        member_one,
    ]


def test_none_completed_tasks_is_treated_as_zero():
    member = SimpleNamespace(
        total_tasks_completed=None,
        is_irregular=False,
    )

    assert calculate_fairness_score(member) == 0
