
from app.models.task import Task


def test_tasks_require_authentication(client, room_one):
    response = client.get(
        f"/tasks/room/{room_one.id}"
    )

    assert response.status_code == 401


def test_user_can_view_room_tasks(
    client, db_session, room_one, member_one, token_one
):
    task = Task(
        room_id=room_one.id,
        name="Test Cleaning",
        description="Automated test task",
        frequency="daily",
        is_active=True,
    )

    db_session.add(task)
    db_session.flush()

    response = client.get(
        f"/tasks/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Cleaning"


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


def test_user_cannot_access_task_from_other_room(
    client, db_session, room_one, token_two
):
    task = Task(
        room_id=room_one.id,
        name="Private Task",
        description="Task belonging to another user's room",
        frequency="daily",
        is_active=True,
    )

    db_session.add(task)
    db_session.flush()

    response = client.get(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404
