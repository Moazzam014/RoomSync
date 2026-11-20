
import pytest

from app.models.member import Member
from app.models.rotation import Rotation
from app.models.task import Task


@pytest.fixture
def task_one(db_session, room_one):
    task = Task(
        room_id=room_one.id,
        name="Clean Kitchen",
        description="Clean the kitchen area",
        frequency="daily",
        is_active=True,
    )
    db_session.add(task)
    db_session.flush()
    return task


@pytest.fixture
def member_two(db_session, user_two, room_one):
    member = Member(
        name="Test User Two",
        room_id=room_one.id,
        user_id=user_two.id,
        is_active=True,
        total_tasks_completed=5,
    )
    db_session.add(member)
    db_session.flush()
    return member


@pytest.fixture
def rotation_one(db_session, room_one, task_one, member_one):
    rotation = Rotation(
        room_id=room_one.id,
        task_id=task_one.id,
        member_id=member_one.id,
        status="assigned",
        assignment_reason="Test assignment",
        is_completed=False,
    )
    db_session.add(rotation)
    db_session.flush()
    return rotation


def test_workflow_requires_authentication(client, room_one):
    response = client.get(
        f"/workflow/room/{room_one.id}"
    )

    assert response.status_code == 401


def test_member_can_view_room_workflow(
    client, room_one, task_one, member_one, token_one
):
    response = client.get(
        f"/workflow/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["room_id"] == room_one.id
    assert len(response.json()["tasks"]) == 1


def test_non_member_cannot_view_room_workflow(
    client, room_one, user_two, token_two
):
    response = client.get(
        f"/workflow/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_member_can_view_active_rotations(
    client, room_one, rotation_one, token_one
):
    response = client.get(
        f"/workflow/room/{room_one.id}/active",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["is_completed"] is False


def test_task_assignment_uses_fairness_ranking(
    client,
    db_session,
    room_one,
    task_one,
    member_one,
    member_two,
    token_one,
):
    member_one.total_tasks_completed = 0
    member_two.total_tasks_completed = 5
    db_session.flush()

    response = client.post(
        f"/workflow/room/{room_one.id}/task/{task_one.id}/assign",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["task_id"] == task_one.id
    assert response.json()["member_id"] == member_one.id
    assert response.json()["status"] == "assigned"


def test_non_member_cannot_assign_task(
    client, room_one, task_one, token_two
):
    response = client.post(
        f"/workflow/room/{room_one.id}/task/{task_one.id}/assign",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_regular_member_can_trigger_task_assignment(
    client,
    db_session,
    room_one,
    task_one,
    member_one,
    member_two,
    token_two,
):
    member_one.total_tasks_completed = 10
    member_two.total_tasks_completed = 0
    db_session.flush()

    response = client.post(
        f"/workflow/room/{room_one.id}/task/{task_one.id}/assign",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 200
    assert response.json()["member_id"] == member_two.id


def test_pending_assignments_affect_fairness(
    client,
    db_session,
    room_one,
    task_one,
    member_one,
    member_two,
    token_one,
):
    member_one.total_tasks_completed = 0
    member_two.total_tasks_completed = 0

    workload_task = Task(
        room_id=room_one.id,
        name="Existing Workload",
        description="Task used to test pending workload",
        frequency="daily",
        is_active=True,
    )

    db_session.add(workload_task)
    db_session.flush()

    # Member one has two pending assignments.
    for _ in range(2):
        db_session.add(
            Rotation(
                room_id=room_one.id,
                task_id=workload_task.id,
                member_id=member_one.id,
                status="assigned",
                is_completed=False,
            )
        )

    # Member two has one pending assignment.
    db_session.add(
        Rotation(
            room_id=room_one.id,
            task_id=workload_task.id,
            member_id=member_two.id,
            status="assigned",
            is_completed=False,
        )
    )

    db_session.flush()

    response = client.post(
        f"/workflow/room/{room_one.id}/task/{task_one.id}/assign",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["member_id"] == member_two.id


def test_repeated_assignment_does_not_create_duplicate_rotation(
    client,
    db_session,
    room_one,
    task_one,
    member_one,
    token_one,
):
    url = (
        f"/workflow/room/{room_one.id}/task/{task_one.id}/assign"
    )

    headers = {
        "Authorization": f"Bearer {token_one}"
    }

    first_response = client.post(
        url,
        headers=headers,
    )

    second_response = client.post(
        url,
        headers=headers,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert (
        first_response.json()["id"]
        == second_response.json()["id"]
    )

    active_count = (
        db_session.query(Rotation)
        .filter(
            Rotation.room_id == room_one.id,
            Rotation.task_id == task_one.id,
            Rotation.is_completed.is_(False),
        )
        .count()
    )

    assert active_count == 1


def test_member_can_complete_own_assigned_rotation(
    client, rotation_one, member_one, token_one
):
    response = client.patch(
        f"/workflow/rotation/{rotation_one.id}/complete",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["is_completed"] is True
    assert response.json()["status"] == "completed"
    assert response.json()["completed_at"] is not None


def test_member_cannot_complete_another_members_rotation(
    client,
    db_session,
    room_one,
    task_one,
    member_one,
    member_two,
    token_one,
):
    rotation = Rotation(
        room_id=room_one.id,
        task_id=task_one.id,
        member_id=member_two.id,
        status="assigned",
        is_completed=False,
    )

    db_session.add(rotation)
    db_session.flush()

    response = client.patch(
        f"/workflow/rotation/{rotation.id}/complete",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 403


def test_non_member_cannot_complete_rotation(
    client, rotation_one, token_two
):
    response = client.patch(
        f"/workflow/rotation/{rotation_one.id}/complete",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_completing_rotation_twice_does_not_double_count(
    client, db_session, rotation_one, member_one, token_one
):
    headers = {
        "Authorization": f"Bearer {token_one}"
    }

    url = (
        f"/workflow/rotation/{rotation_one.id}/complete"
    )

    first_response = client.patch(
        url,
        headers=headers,
    )

    assert first_response.status_code == 200

    db_session.refresh(member_one)

    assert member_one.total_tasks_completed == 1

    second_response = client.patch(
        url,
        headers=headers,
    )

    assert second_response.status_code == 200

    db_session.refresh(member_one)

    assert member_one.total_tasks_completed == 1
