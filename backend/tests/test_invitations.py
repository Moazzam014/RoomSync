
from app.core.datetime_utils import utcnow_naive
from app.models.member import Member
from app.models.room_invitation import RoomInvitation


def create_invitation(
    db_session,
    room_id,
    inviter_id,
    invitee_id,
    invitation_status="pending",
):
    invitation = RoomInvitation(
        room_id=room_id,
        inviter_id=inviter_id,
        invitee_id=invitee_id,
        status=invitation_status,
        created_at=utcnow_naive(),
    )

    db_session.add(invitation)
    db_session.flush()

    return invitation


def test_invitations_require_authentication(client, room_one):
    response = client.post(
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": "test_user_two",
        },
    )

    assert response.status_code == 401


def test_room_owner_can_send_invitation(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_one,
):
    response = client.post(
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": user_two.username,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 201
    assert response.json()["room_id"] == room_one.id
    assert response.json()["inviter_id"] == user_one.id
    assert response.json()["invitee_id"] == user_two.id
    assert response.json()["status"] == "pending"


def test_regular_member_cannot_send_invitation(
    client,
    db_session,
    room_one,
    member_one,
    user_two,
    token_two,
):
    regular_member = Member(
        name="Test User Two",
        room_id=room_one.id,
        user_id=user_two.id,
        role="member",
        is_active=True,
    )

    db_session.add(regular_member)
    db_session.flush()

    response = client.post(
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": "test_user_three",
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 403


def test_non_member_cannot_send_invitation(
    client,
    room_one,
    user_two,
    token_two,
):
    response = client.post(
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": user_two.username,
        },
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 404


def test_owner_cannot_invite_self(
    client,
    room_one,
    member_one,
    user_one,
    token_one,
):
    response = client.post(
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": user_one.username,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 400


def test_duplicate_pending_invitation_is_rejected(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_one,
):
    create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

    response = client.post(
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": user_two.username,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invitation already pending."


def test_invitation_recipient_can_view_pending_invitations(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_two,
):
    create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

    response = client.get(
        "/invitations/me",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["invitee_id"] == user_two.id


def test_invitation_recipient_can_accept_invitation(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_two,
):
    invitation = create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

    response = client.patch(
        f"/invitations/{invitation.id}/accept",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert response.json()["responded_at"] is not None

    membership = (
        db_session.query(Member)
        .filter(
            Member.room_id == room_one.id,
            Member.user_id == user_two.id,
        )
        .first()
    )

    assert membership is not None
    assert membership.is_active is True
    assert membership.role == "member"


def test_other_user_cannot_accept_invitation(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_one,
):
    invitation = create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

    response = client.patch(
        f"/invitations/{invitation.id}/accept",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 403


def test_invitation_recipient_can_decline_invitation(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_two,
):
    invitation = create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

    response = client.patch(
        f"/invitations/{invitation.id}/decline",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "declined"
    assert response.json()["responded_at"] is not None


def test_other_user_cannot_decline_invitation(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_one,
):
    invitation = create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

    response = client.patch(
        f"/invitations/{invitation.id}/decline",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 403


def test_invitation_allows_more_than_seven_members(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
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
        "/invitations/",
        json={
            "room_id": room_one.id,
            "invitee_username": user_two.username,
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_accepting_invitation_allows_more_than_seven_members(
    client,
    db_session,
    room_one,
    member_one,
    user_one,
    user_two,
    token_two,
):
    invitation = create_invitation(
        db_session=db_session,
        room_id=room_one.id,
        inviter_id=user_one.id,
        invitee_id=user_two.id,
    )

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

    response = client.patch(
        f"/invitations/{invitation.id}/accept",
        headers={"Authorization": f"Bearer {token_two}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"

    accepted_member = (
        db_session.query(Member)
        .filter(
            Member.room_id == room_one.id,
            Member.user_id == user_two.id,
            Member.is_active.is_(True),
        )
        .first()
    )

    assert accepted_member is not None
