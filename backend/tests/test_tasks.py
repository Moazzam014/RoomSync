
from app.models.member import Member
from app.models.task import Task


def create_test_task(db_session, room_id):
    task = Task(
        room_id=room_id,
        name="Test Cleaning",
        description="Automated test task",
        frequency="daily",
        is_active=True,
    )

    db_session.add(task)
    db_session.flush()

    return task


def add_regular_member(db_session, user, room):
    member = Member(
        name="Test User Two",
        room_id=room.id,
        user_id=user.id,
        role="member",
        is_active=True,
    )

    db_session.add(member)
    db_session.flush()

    return member


def test_tasks_require_authentication(client, room_one):
    response = client.get(f"/tasks/room/{room_one.id}")

    assert response.status_code == 401


def test_user_can_view_room_tasks(
    client, db_session, room_one, member_one, token_one
):
    task = create_test_task(db_session, room_one.id)

    response = client.get(
        f"/tasks/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == task.name


def test_non_member_cannot_view_room_tasks(
    client, room_one, token_two
):
    response = client.get(
        f"/tasks/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_user_can_create_room_task(
    client, room_one, member_one, token_one
):
    response = client.post(
        "/tasks/",
        json={
            "name": "Test Cleaning",
            "description": "Automated task",
            "frequency": "daily",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Cleaning"
    assert response.json()["room_id"] == room_one.id
    assert response.json()["is_active"] is True


def test_non_member_cannot_create_room_task(
    client, room_one, token_two
):
    response = client.post(
        "/tasks/",
        json={
            "name": "Unauthorized Task",
            "description": "Should not be created",
            "frequency": "daily",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_regular_member_cannot_create_room_task(
    client, db_session, room_one, user_two, token_two
):
    add_regular_member(db_session, user_two, room_one)

    response = client.post(
        "/tasks/",
        json={
            "name": "Unauthorized Task",
            "description": "Member cannot create tasks",
            "frequency": "daily",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_user_cannot_access_task_from_other_room(
    client, db_session, room_one, token_two
):
    task = create_test_task(db_session, room_one.id)

    response = client.get(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_owner_can_update_task(
    client, db_session, room_one, member_one, token_one
):
    task = create_test_task(db_session, room_one.id)

    response = client.patch(
        f"/tasks/{task.id}",
        json={
            "name": "Updated Cleaning",
            "frequency": "weekly",
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Cleaning"
    assert response.json()["frequency"] == "weekly"


def test_regular_member_cannot_update_task(
    client, db_session, room_one, user_two, token_two
):
    add_regular_member(db_session, user_two, room_one)
    task = create_test_task(db_session, room_one.id)

    response = client.patch(
        f"/tasks/{task.id}",
        json={"name": "Unauthorized Update"},
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_owner_can_deactivate_task(
    client, db_session, room_one, member_one, token_one
):
    task = create_test_task(db_session, room_one.id)

    response = client.delete(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_regular_member_cannot_deactivate_task(
    client, db_session, room_one, user_two, token_two
):
    add_regular_member(db_session, user_two, room_one)
    task = create_test_task(db_session, room_one.id)

    response = client.delete(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_task_name_cannot_be_empty(
    client, room_one, member_one, token_one
):
    response = client.post(
        "/tasks/",
        json={
            "name": "   ",
            "description": "Invalid task",
            "frequency": "daily",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 422


def test_task_frequency_cannot_be_empty(
    client, room_one, member_one, token_one
):
    response = client.post(
        "/tasks/",
        json={
            "name": "Cleaning",
            "frequency": "   ",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 422


def test_task_patch_requires_at_least_one_field(
    client, db_session, room_one, member_one, token_one
):
    task = create_test_task(db_session, room_one.id)

    response = client.patch(
        f"/tasks/{task.id}",
        json={},
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 422


def test_task_patch_cannot_change_is_active(
    client, db_session, room_one, member_one, token_one
):
    task = create_test_task(db_session, room_one.id)

    response = client.patch(
        f"/tasks/{task.id}",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 422
