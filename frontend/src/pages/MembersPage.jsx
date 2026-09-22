import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  Bell,
  Check,
  Mail,
  RefreshCw,
  Send,
  ShieldCheck,
  UserPlus,
  Users,
  X,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import { getRoom } from "../services/roomService";
import { getRoomMembers } from "../services/memberService";
import {
  acceptInvitation,
  declineInvitation,
  getMyInvitations,
  sendInvitation,
} from "../services/invitationService";

function MembersPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [room, setRoom] = useState(null);
  const [members, setMembers] = useState([]);
  const [invitations, setInvitations] = useState([]);

  const [username, setUsername] = useState("");

  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [processingId, setProcessingId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const currentUser = useMemo(() => {
    try {
      return JSON.parse(
        localStorage.getItem(
          "roomsync_user"
        ) || "null"
      );
    } catch {
      return null;
    }
  }, []);

  const loadMembers = async () => {
    try {
      const data =
        await getRoomMembers(roomId);

      setMembers(
        Array.isArray(data)
          ? data
          : []
      );
    } catch (err) {
      console.error(
        "Members loading error:",
        err
      );

      setMembers([]);
    }
  };

  const loadInvitations = async () => {
    try {
      const data =
        await getMyInvitations();

      setInvitations(
        Array.isArray(data)
          ? data
          : []
      );
    } catch (err) {
      console.error(
        "Invitations loading error:",
        err
      );

      setInvitations([]);
    }
  };

  const loadPage = async () => {
    try {
      setLoading(true);
      setError("");

      const roomData =
        await getRoom(roomId);

      setRoom(roomData);

      await Promise.all([
        loadMembers(),
        loadInvitations(),
      ]);
    } catch (err) {
      console.error(
        "Members page error:",
        err
      );

      setError(
        err.response?.data?.detail ||
          "Unable to load team members."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPage();
  }, [roomId]);

  const roomInvitations = invitations.filter(
    (invitation) =>
      Number(invitation.room_id) ===
        Number(roomId) &&
      invitation.status === "pending"
  );

  const handleSendInvitation = async (
    event
  ) => {
    event.preventDefault();

    const cleanUsername =
      username.trim();

    if (!cleanUsername) {
      setError(
        "Enter a username to send an invitation."
      );
      return;
    }

    try {
      setSending(true);
      setError("");
      setSuccess("");

      await sendInvitation({
        room_id: Number(roomId),
        invitee_username:
          cleanUsername,
      });

      setUsername("");

      setSuccess(
        `Invitation sent to @${cleanUsername}.`
      );

      await loadInvitations();
    } catch (err) {
      console.error(
        "Send invitation error:",
        err
      );

      setError(
        err.response?.data?.detail ||
          "Unable to send invitation."
      );
    } finally {
      setSending(false);
    }
  };

  const handleAccept = async (
    invitationId
  ) => {
    try {
      setProcessingId(invitationId);
      setError("");
      setSuccess("");

      await acceptInvitation(
        invitationId
      );

      setSuccess(
        "Invitation accepted successfully."
      );

      await Promise.all([
        loadMembers(),
        loadInvitations(),
      ]);
    } catch (err) {
      console.error(
        "Accept invitation error:",
        err
      );

      setError(
        err.response?.data?.detail ||
          "Unable to accept invitation."
      );
    } finally {
      setProcessingId(null);
    }
  };

  const handleDecline = async (
    invitationId
  ) => {
    try {
      setProcessingId(invitationId);
      setError("");
      setSuccess("");

      await declineInvitation(
        invitationId
      );

      setSuccess(
        "Invitation declined."
      );

      await loadInvitations();
    } catch (err) {
      console.error(
        "Decline invitation error:",
        err
      );

      setError(
        err.response?.data?.detail ||
          "Unable to decline invitation."
      );
    } finally {
      setProcessingId(null);
    }
  };

  if (loading) {
    return (
      <main className="members-page">
        <div className="members-loading">
          <RefreshCw
            size={23}
            className="members-spin"
          />
          Loading team members...
        </div>
      </main>
    );
  }

  return (
    <main className="members-page">
      <div className="members-shell">

        {/* HEADER */}

        <header className="members-header">

          <div>
            <button
              type="button"
              className="members-back"
              onClick={() =>
                navigate(
                  `/dashboard/${roomId}`
                )
              }
            >
              <ArrowLeft size={17} />
              Dashboard
            </button>

            <span className="members-eyebrow">
              TEAM MANAGEMENT
            </span>

            <h1>
              {room?.name ||
                `Room #${roomId}`}
            </h1>

            <p>
              Manage your team members and
              invite new teammates.
            </p>
          </div>

          <button
            type="button"
            className="members-refresh"
            onClick={loadPage}
          >
            <RefreshCw size={17} />
            Refresh
          </button>

        </header>

        {/* MESSAGES */}

        {error && (
          <div className="members-message members-message-error">
            <span>{error}</span>

            <button
              type="button"
              onClick={() => setError("")}
            >
              <X size={15} />
            </button>
          </div>
        )}

        {success && (
          <div className="members-message members-message-success">
            <Check size={16} />
            <span>{success}</span>

            <button
              type="button"
              onClick={() => setSuccess("")}
            >
              <X size={15} />
            </button>
          </div>
        )}

        {/* SUMMARY */}

        <section className="members-summary">

          <div className="members-summary-card">

            <div className="members-summary-icon">
              <Users size={21} />
            </div>

            <div>
              <span>
                TEAM MEMBERS
              </span>

              <strong>
                {members.length} / 7
              </strong>
            </div>

          </div>

          <div className="members-summary-card">

            <div className="members-summary-icon">
              <Mail size={21} />
            </div>

            <div>
              <span>
                PENDING INVITES
              </span>

              <strong>
                {roomInvitations.length}
              </strong>
            </div>

          </div>

          <div className="members-summary-card">

            <div className="members-summary-icon">
              <ShieldCheck size={21} />
            </div>

            <div>
              <span>
                ROOM CAPACITY
              </span>

              <strong>
                {Math.max(
                  7 - members.length,
                  0
                )}{" "}
                spots
              </strong>
            </div>

          </div>

        </section>

        {/* INVITE + MEMBERS */}

        <section className="members-layout">

          {/* INVITE */}

          <div className="members-card members-invite-card">

            <div className="members-card-heading">

              <div className="members-card-icon">
                <UserPlus size={20} />
              </div>

              <div>
                <h2>
                  Invite a Teammate
                </h2>

                <p>
                  Invite an existing
                  RoomSync user by username.
                </p>
              </div>

            </div>

            <form
              className="members-invite-form"
              onSubmit={
                handleSendInvitation
              }
            >

              <label htmlFor="invite-username">
                Username
              </label>

              <div className="members-input-row">

                <div className="members-input-wrap">
                  <span>@</span>

                  <input
                    id="invite-username"
                    type="text"
                    value={username}
                    onChange={(event) =>
                      setUsername(
                        event.target.value
                      )
                    }
                    placeholder="username"
                    disabled={sending}
                  />
                </div>

                <button
                  type="submit"
                  disabled={
                    sending ||
                    members.length >= 7
                  }
                >
                  {sending ? (
                    <>
                      <RefreshCw
                        size={16}
                        className="members-spin"
                      />
                      Sending
                    </>
                  ) : (
                    <>
                      <Send size={16} />
                      Send Invite
                    </>
                  )}
                </button>

              </div>

              {members.length >= 7 && (
                <span className="members-capacity-note">
                  This room has reached its
                  maximum capacity of 7 members.
                </span>
              )}

            </form>

          </div>

          {/* MEMBERS */}

          <div className="members-card">

            <div className="members-card-heading">

              <div className="members-card-icon">
                <Users size={20} />
              </div>

              <div>
                <h2>
                  Team Members
                </h2>

                <p>
                  People currently in this
                  workspace.
                </p>
              </div>

            </div>

            {members.length === 0 ? (
              <div className="members-empty">

                <Users size={29} />

                <h3>
                  No team members yet
                </h3>

                <p>
                  Invite teammates using
                  their RoomSync username.
                </p>

              </div>
            ) : (
              <div className="members-list">

                {members.map((member) => {

                  const memberName =
                    member.name ||
                    member.username ||
                    `Member #${member.id}`;

                  const isCurrentUser =
                    member.user_id &&
                    currentUser?.id &&
                    Number(
                      member.user_id
                    ) ===
                      Number(
                        currentUser.id
                      );

                  return (
                    <div
                      className="member-row"
                      key={member.id}
                    >

                      <div className="member-avatar">
                        {memberName
                          .charAt(0)
                          .toUpperCase()}
                      </div>

                      <div className="member-info">

                        <strong>
                          {memberName}
                        </strong>

                        <span>
                          {isCurrentUser
                            ? "You"
                            : member.user_id
                            ? "Room member"
                            : "Legacy member"}
                        </span>

                      </div>

                      <span
                        className={`member-status ${
                          member.is_active === false
                            ? "inactive"
                            : "active"
                        }`}
                      >
                        {member.is_active === false
                          ? "Inactive"
                          : "Active"}
                      </span>

                    </div>
                  );
                })}

              </div>
            )}

          </div>

        </section>

        {/* PENDING INVITATIONS */}

        <section className="members-card members-pending-card">

          <div className="members-card-heading">

            <div className="members-card-icon">
              <Bell size={20} />
            </div>

            <div>
              <h2>
                Pending Invitations
              </h2>

              <p>
                Invitations waiting for
                your response.
              </p>
            </div>

          </div>

          {roomInvitations.length === 0 ? (
            <div className="members-pending-empty">
              <Check size={20} />
              <span>
                No pending invitations for
                this room.
              </span>
            </div>
          ) : (
            <div className="members-invitation-list">

              {roomInvitations.map(
                (invitation) => {

                  const invitationId =
                    invitation.id;

                  const busy =
                    processingId ===
                    invitationId;

                  return (
                    <div
                      className="member-invitation-row"
                      key={invitationId}
                    >

                      <div className="member-invitation-icon">
                        <Mail size={17} />
                      </div>

                      <div className="member-invitation-info">

                        <strong>
                          Room invitation
                        </strong>

                        <span>
                          Invitation #{invitationId}
                        </span>

                      </div>

                      <div className="member-invitation-actions">

                        <button
                          type="button"
                          className="member-accept"
                          disabled={busy}
                          onClick={() =>
                            handleAccept(
                              invitationId
                            )
                          }
                        >
                          {busy ? (
                            <RefreshCw
                              size={15}
                              className="members-spin"
                            />
                          ) : (
                            <Check
                              size={15}
                            />
                          )}
                          Accept
                        </button>

                        <button
                          type="button"
                          className="member-decline"
                          disabled={busy}
                          onClick={() =>
                            handleDecline(
                              invitationId
                            )
                          }
                        >
                          <X size={15} />
                          Decline
                        </button>

                      </div>

                    </div>
                  );
                }
              )}

            </div>
          )}

        </section>

      </div>
    </main>
  );
}

export default MembersPage;