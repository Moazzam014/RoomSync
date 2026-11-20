import { useCallback, useEffect, useState } from "react";
import {
  ArrowRight,
  Plus,
  RefreshCw,
  Users,
  Mail,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { getRooms } from "../services/roomService";

function MyRoomsPage() {
  const navigate = useNavigate();

  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchRooms = useCallback(async () => {
    try {
      setError("");

      const data = await getRooms();

      setRooms(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("My rooms error:", err);

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
    <main className="my-rooms-page">
      <div className="my-rooms-shell">

        <header className="my-rooms-header">
          <div>
            <span className="my-rooms-eyebrow">
              ROOMSYNC
            </span>

            <h1>My Rooms</h1>

            <p>
              Select a room to continue
              working with your team.
            </p>
          </div>

          <button
            type="button"
            className="my-rooms-refresh"
            onClick={loadRooms}
            disabled={loading}
          >
            <RefreshCw size={17} />
            Refresh
          </button>
        </header>

        {error && (
          <div className="my-rooms-error">
            {error}
          </div>
        )}

        <div className="my-rooms-actions">

          <button
            type="button"
            className="my-room-action primary"
            onClick={() => navigate("/create-room")}
          >
            <Plus size={19} />

            <div>
              <strong>Create a Room</strong>
              <span>Start a new team workspace</span>
            </div>

            <ArrowRight size={18} />
          </button>

          <button
            type="button"
            className="my-room-action"
            onClick={() => navigate("/invitations")}
          >
            <Mail size={19} />

            <div>
              <strong>Invitations</strong>
              <span>View and accept room invitations</span>
            </div>

            <ArrowRight size={18} />
          </button>

        </div>

        <section className="my-rooms-section">

          <div className="my-rooms-section-heading">
            <div>
              <h2>Existing Rooms</h2>

              <p>
                Open one of your available rooms.
              </p>
            </div>

            <span className="room-count">
              {rooms.length}{" "}
              {rooms.length === 1 ? "Room" : "Rooms"}
            </span>
          </div>

          {loading ? (
            <div className="my-rooms-empty">
              <RefreshCw
                size={25}
                className="rooms-spin"
              />

              <h3>Loading rooms...</h3>
            </div>
          ) : rooms.length === 0 ? (
            <div className="my-rooms-empty">

              <div className="empty-room-icon">
                <Users size={28} />
              </div>

              <h3>No rooms found</h3>

              <p>
                Create a room or accept an invitation
                to get started.
              </p>

              <div className="empty-room-actions">

                <button
                  type="button"
                  onClick={() => navigate("/create-room")}
                >
                  <Plus size={17} />
                  Create Room
                </button>

                <button
                  type="button"
                  onClick={() => navigate("/invitations")}
                >
                  <Mail size={17} />
                  Invitations
                </button>

              </div>
            </div>
          ) : (
            <div className="my-rooms-grid">

              {rooms.map((room) => (
                <button
                  type="button"
                  className="my-room-card"
                  key={room.id}
                  onClick={() =>
                    navigate(`/dashboard/${room.id}`)
                  }
                >
                  <div className="my-room-card-top">

                    <div className="my-room-icon">
                      {room.name?.charAt(0).toUpperCase() || "R"}
                    </div>

                    <ArrowRight
                      size={19}
                      className="my-room-arrow"
                    />

                  </div>

                  <div className="my-room-card-content">
                    <h3>
                      {room.name || `Room #${room.id}`}
                    </h3>

                    {room.description && (
                      <p>{room.description}</p>
                    )}
                  </div>

                  <div className="my-room-card-footer">
                    <span>
                      <Users size={14} />
                      Open Room
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

export default MyRoomsPage;