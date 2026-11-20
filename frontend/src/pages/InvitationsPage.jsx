import { useCallback, useEffect, useState } from "react";
import {
  ArrowLeft,
  Bell,
  Check,
  RefreshCw,
  UserRound,
  X,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import {
  acceptInvitation,
  declineInvitation,
  getMyInvitations,
} from "../services/invitationService";

function InvitationsPage() {
  const navigate = useNavigate();

  const [invitations, setInvitations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const fetchInvitations = useCallback(async () => {
    try {
      setError("");

      const data = await getMyInvitations();

      setInvitations(
        Array.isArray(data) ? data : []
      );
    } catch (err) {
      console.error("Invitations page error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to load invitations."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  const loadInvitations = async () => {
    setLoading(true);
    await fetchInvitations();
  };

  useEffect(() => {
    fetchInvitations();
  }, [fetchInvitations]);

  const handleAccept = async (invitationId) => {
    try {
      setProcessingId(invitationId);
      setError("");
      setSuccess("");

      const invitation =
        await acceptInvitation(invitationId);

      setSuccess("Invitation accepted successfully.");

      await fetchInvitations();

      if (invitation?.room_id) {
        navigate(`/dashboard/${invitation.room_id}`);
      }
    } catch (err) {
      console.error("Accept invitation error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to accept invitation."
      );
    } finally {
      setProcessingId(null);
    }
  };

  const handleDecline = async (invitationId) => {
    try {
      setProcessingId(invitationId);
      setError("");
      setSuccess("");

      await declineInvitation(invitationId);

      setSuccess("Invitation declined.");

      await fetchInvitations();
    } catch (err) {
      console.error("Decline invitation error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to decline invitation."
      );
    } finally {
      setProcessingId(null);
    }
  };

  return (
    <main className="invitations-page">
      <div className="invitations-shell">

        <header className="invitations-header">

          <div>
            <button
              type="button"
              className="invitations-back"
              onClick={() => navigate("/start")}
            >
              <ArrowLeft size={17} />
              Overview
            </button>

            <span className="invitations-eyebrow">
              ROOMSYNC
            </span>

            <h1>Invitations</h1>

            <p>
              View and manage invitations to
              join team workspaces.
            </p>
          </div>

          <button
            type="button"
            className="invitations-refresh"
            onClick={loadInvitations}
            disabled={loading}
          >
            <RefreshCw
              size={16}
              className={loading ? "invitations-spin" : ""}
            />
            Refresh
          </button>

        </header>

        {error && (
          <div className="invitations-message error">
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
          <div className="invitations-message success">
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

        <section className="invitations-card">

          <div className="invitations-card-heading">

            <div className="invitations-icon">
              <Bell size={20} />
            </div>

            <div>
              <h2>Pending Invitations</h2>

              <p>
                Invitations waiting for your response.
              </p>
            </div>

            <span className="invitations-count">
              {invitations.length}
            </span>

          </div>

          {loading ? (
            <div className="invitations-empty">
              <RefreshCw
                size={27}
                className="invitations-spin"
              />

              <h3>Loading invitations...</h3>
            </div>
          ) : invitations.length === 0 ? (
            <div className="invitations-empty">

              <div className="invitations-empty-icon">
                <Check size={27} />
              </div>

              <h3>No pending invitations</h3>

              <p>
                You're all caught up. New room invitations
                will appear here.
              </p>

              <button
                type="button"
                onClick={() => navigate("/start")}
              >
                Back to Overview
              </button>

            </div>
          ) : (
            <div className="invitations-list">

              {invitations.map((invitation) => {
                const busy =
                  processingId === invitation.id;

                return (
                  <article
                    className="invitation-row"
                    key={invitation.id}
                  >
                    <div className="invitation-avatar">
                      <UserRound size={19} />
                    </div>

                    <div className="invitation-info">
                      <strong>Room Invitation</strong>

                      <span>
                        Room #{invitation.room_id}
                      </span>

                      <small>
                        Invitation #{invitation.id}
                      </small>
                    </div>

                    <div className="invitation-actions">

                      <button
                        type="button"
                        className="invitation-accept"
                        disabled={busy}
                        onClick={() =>
                          handleAccept(invitation.id)
                        }
                      >
                        {busy ? (
                          <RefreshCw
                            size={15}
                            className="invitations-spin"
                          />
                        ) : (
                          <Check size={15} />
                        )}
                        Accept
                      </button>

                      <button
                        type="button"
                        className="invitation-decline"
                        disabled={busy}
                        onClick={() =>
                          handleDecline(invitation.id)
                        }
                      >
                        <X size={15} />
                        Decline
                      </button>

                    </div>
                  </article>
                );
              })}

            </div>
          )}

        </section>
      </div>
    </main>
  );
}

export default InvitationsPage;