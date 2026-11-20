import { useCallback, useEffect, useState } from "react";
import {
  ArrowRight,
  Bell,
  DoorOpen,
  Plus,
  RefreshCw,
  Users,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { getRooms } from "../services/roomService";
import { getStoredUser } from "../services/authService";

function StartPage() {
  const navigate = useNavigate();

  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const currentUser = getStoredUser();

  const fetchRooms = useCallback(async () => {
    try {
      setError("");

      const data = await getRooms();

      setRooms(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Start page rooms error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to load your rooms."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  const loadRooms = async () => {
    setLoading(true);
    await fetchRooms();
  };

  useEffect(() => {
    fetchRooms();
  }, [fetchRooms]);

  return (
    <main className="start-page">
      <div className="start-shell">

        <header className="start-header">

          <div className="start-brand">
            <div className="start-brand-mark">
              R
            </div>

            <div>
              <strong>RoomSync</strong>
              <span>Team Workspace</span>
            </div>
          </div>

          <div className="start-user-area">

            <button
              type="button"
              className="start-invitations-button"
              onClick={() => navigate("/invitations")}
            >
              <Bell size={16} />
              Invitations
            </button>

            <div className="start-user">
              <div className="start-user-avatar">
                {(
                  currentUser?.full_name ||
                  currentUser?.username ||
                  "U"
                ).charAt(0).toUpperCase()}
              </div>

              <div>
                <strong>
                  {currentUser?.full_name ||
                    currentUser?.username ||
                    "User"}
                </strong>

                <span>
                  @{currentUser?.username || "user"}
                </span>
              </div>
            </div>

          </div>
        </header>

        <section className="start-welcome">

          <div>
            <span className="start-eyebrow">
              WORKSPACE
            </span>

            <h1>
              Welcome back
              {currentUser?.full_name
                ? `, ${currentUser.full_name.split(" ")[0]}`
                : ""}
              .
            </h1>

            <p>
              Create a new workspace or continue
              working in one of your existing rooms.
            </p>
          </div>

          <button
            type="button"
            className="start-refresh"
            onClick={loadRooms}
            disabled={loading}
          >
            <RefreshCw
              size={16}
              className={loading ? "start-spin" : ""}
            />
            Refresh
          </button>

        </section>

        <section className="start-actions">

          <button
            type="button"
            className="start-action-card start-action-primary"
            onClick={() => navigate("/create-room")}
          >
            <div className="start-action-icon">
              <Plus size={22} />
            </div>

            <div className="start-action-content">
              <strong>Create a Room</strong>

              <span>
                Start a new RoomSync workspace
                and invite your teammates.
              </span>

              <small>
                Create room
                <ArrowRight size={14} />
              </small>
            </div>
          </button>

          <button
            type="button"
            className="start-action-card"
            onClick={() => navigate("/invitations")}
          >
            <div className="start-action-icon">
              <Users size={22} />
            </div>

            <div className="start-action-content">
              <strong>Join a Room</strong>

              <span>
                Check your invitations and join
                a room created by someone else.
              </span>

              <small>
                View invitations
                <ArrowRight size={14} />
              </small>
            </div>
          </button>

        </section>

        <section className="start-rooms-section">

          <div className="start-section-header">

            <div>
              <span className="start-section-eyebrow">
                YOUR WORKSPACES
              </span>

              <h2>Existing Rooms</h2>

              <p>
                Open a room you already belong to
                and continue working.
              </p>
            </div>

            <div className="start-room-count">
              {rooms.length}{" "}
              {rooms.length === 1 ? "Room" : "Rooms"}
            </div>

          </div>

          {error && (
            <div className="start-error">
              {error}
            </div>
          )}

          {loading ? (
            <div className="start-empty">
              <RefreshCw
                size={25}
                className="start-spin"
              />

              <h3>Loading your rooms...</h3>

              <p>
                Checking your existing workspaces.
              </p>
            </div>
          ) : rooms.length === 0 ? (
            <div className="start-empty">

              <div className="start-empty-icon">
                <DoorOpen size={27} />
              </div>

              <h3>No rooms yet</h3>

              <p>
                Create your first room or accept
                an invitation from a teammate.
              </p>

              <div className="start-empty-buttons">

                <button
                  type="button"
                  onClick={() => navigate("/create-room")}
                >
                  <Plus size={16} />
                  Create Room
                </button>

                <button
                  type="button"
                  onClick={() => navigate("/invitations")}
                >
                  <Bell size={16} />
                  Invitations
                </button>

              </div>
            </div>
          ) : (
            <div className="start-rooms-grid">

              {rooms.map((room) => (
                <button
                  type="button"
                  className="start-room-card"
                  key={room.id}
                  onClick={() =>
                    navigate(`/dashboard/${room.id}`)
                  }
                >
                  <div className="start-room-top">

                    <div className="start-room-avatar">
                      {(room.name || "R")
                        .charAt(0)
                        .toUpperCase()}
                    </div>

                    <div className="start-room-open">
                      Open
                      <ArrowRight size={15} />
                    </div>

                  </div>

                  <div className="start-room-content">
                    <h3>
                      {room.name || `Room #${room.id}`}
                    </h3>

                    <p>
                      {room.description ||
                        "RoomSync team workspace"}
                    </p>
                  </div>

                  <div className="start-room-footer">
                    <span>
                      <Users size={14} />
                      Open workspace
                    </span>

                    <span>#{room.id}</span>
                  </div>

                </button>
              ))}

            </div>
          )}

        </section>
      </div>
    </main>
  );
}

export default StartPage;