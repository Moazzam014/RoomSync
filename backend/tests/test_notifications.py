def test_notifications_require_authentication(client, member_one):
    response = client.get(
        f"/notifications/member/{member_one.id}"
    )
    assert response.status_code == 401


def test_user_can_view_own_notifications(
    client, member_one, notification_one, token_one
):
    response = client.get(
        f"/notifications/member/{member_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == notification_one.id


def test_user_cannot_view_other_users_notifications(
    client, member_one, token_two
):
    response = client.get(
        f"/notifications/member/{member_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_user_cannot_mark_other_users_notification_read(
    client, notification_one, token_two
):
    response = client.patch(
        f"/notifications/{notification_one.id}/read",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_user_can_mark_own_notification_read(
    client, notification_one, token_one
):
    response = client.patch(
        f"/notifications/{notification_one.id}/read",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["is_read"] is True