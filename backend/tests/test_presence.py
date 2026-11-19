from app.models.presence import Presence


def test_presence_requires_authentication(client, member_one):
    response = client.get(
        f"/presence/member/{member_one.id}"
    )
    assert response.status_code == 401


def test_user_can_view_own_presence(
    client, db_session, member_one, token_one
):
    presence = Presence(
        member_id=member_one.id,
        is_present=True,
    )
    db_session.add(presence)
    db_session.flush()

    response = client.get(
        f"/presence/member/{member_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["is_present"] is True


def test_user_cannot_view_other_users_presence(
    client, member_one, token_two
):
    response = client.get(
        f"/presence/member/{member_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_user_can_update_own_presence(
    client, member_one, token_one
):
    response = client.post(
        "/presence/",
        json={
            "member_id": member_one.id,
            "is_present": True,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 201
    assert response.json()["is_present"] is True


def test_user_cannot_update_other_users_presence(
    client, member_one, token_two
):
    response = client.post(
        "/presence/",
        json={
            "member_id": member_one.id,
            "is_present": False,
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403