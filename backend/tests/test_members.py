
from app.models.member import Member


def add_regular_member(db_session, room_id, user_two):
    member = Member(
        name="Test User Two",
        room_id=room_id,
        user_id=user_two.id,
        role="member",
        is_active=True,
    )
    db_session.add(member)
    db_session.flush()
    return member


# Existing access tests


def test_members_require_authentication(client, room_one):
    response = client.get(f"/members/room/{room_one.id}")
    assert response.status_code == 401


def test_user_can_view_room_members(
    client, room_one, member_one, token_one
):
    response = client.get(
        f"/members/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_non_member_cannot_view_room_members(
    client, room_one, token_two
):
    response = client.get(
        f"/members/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_user_can_view_own_member_details(
    client, member_one, token_one
):
    response = client.get(
        f"/members/{member_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == member_one.id


def test_user_cannot_view_member_of_other_room(
    client, member_one, token_two
):
    response = client.get(
        f"/members/{member_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_non_member_cannot_create_room_member(
    client, room_one, token_two
):
    response = client.post(
        "/members/",
        json={
            "name": "Unauthorized Member",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


# Owner permission tests


def test_owner_can_create_room_member(
    client,
    room_one,
    member_one,
    token_one,
):
    response = client.post(
        "/members/",
        json={
            "name": "New Room Member",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "New Room Member"
    assert response.json()["role"] == "member"
    assert response.json()["room_id"] == room_one.id


def test_regular_member_cannot_create_room_member(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_two,
):
    add_regular_member(
        db_session=db_session,
        room_id=room_one.id,
        user_two=user_two,
    )

    response = client.post(
        "/members/",
        json={
            "name": "Unauthorized Member",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_owner_can_update_member_name(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_one,
):
    target_member = add_regular_member(
        db_session=db_session,
        room_id=room_one.id,
        user_two=user_two,
    )

    response = client.patch(
        f"/members/{target_member.id}",
        json={"name": "Updated Member Name"},
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Member Name"


def test_regular_member_cannot_update_member(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_two,
):
    add_regular_member(
        db_session=db_session,
        room_id=room_one.id,
        user_two=user_two,
    )

    response = client.patch(
        f"/members/{member_one.id}",
        json={"name": "Unauthorized Change"},
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_owner_can_remove_regular_member(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_one,
):
    target_member = add_regular_member(
        db_session=db_session,
        room_id=room_one.id,
        user_two=user_two,
    )

    response = client.delete(
        f"/members/{target_member.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == target_member.id

    db_session.refresh(target_member)
    assert target_member.is_active is False


def test_regular_member_cannot_remove_another_member(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_two,
):
    add_regular_member(
        db_session=db_session,
        room_id=room_one.id,
        user_two=user_two,
    )

    response = client.delete(
        f"/members/{member_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_owner_cannot_remove_themselves(
    client,
    room_one,
    member_one,
    token_one,
):
    response = client.delete(
        f"/members/{member_one.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "The room owner cannot be removed."
    )


def test_removed_member_loses_room_access(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_two,
    token_one,
):
    target_member = add_regular_member(
        db_session=db_session,
        room_id=room_one.id,
        user_two=user_two,
    )

    removal_response = client.delete(
        f"/members/{target_member.id}",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert removal_response.status_code == 200

    access_response = client.get(
        f"/members/room/{room_one.id}",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert access_response.status_code == 404


def test_manual_member_creation_allows_more_than_seven_members(
    client,
    db_session,
    room_one,
    member_one,
    token_one,
):
    for index in range(6):
        db_session.add(
            Member(
                name=f"Existing Member {index}",
                room_id=room_one.id,
                user_id=None,
                role="member",
                is_active=True,
            )
        )

    db_session.flush()

    response = client.post(
        "/members/",
        json={
            "name": "Extra Member",
            "room_id": room_one.id,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Extra Member"
    assert response.json()["room_id"] == room_one.id
