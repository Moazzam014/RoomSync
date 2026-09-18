import { ArrowLeft, ArrowRight, Home, Sparkles } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createRoom } from "../services/roomService";

function CreateRoomPage() {
  const navigate = useNavigate();

  const [roomName, setRoomName] = useState("");
  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCreateRoom = async (event) => {
    event.preventDefault();

    setError("");

    if (!roomName.trim()) {
      setError("Please enter a room name.");
      return;
    }

    setLoading(true);

    try {
      const room = await createRoom({
        name: roomName.trim(),
        description: description.trim() || null,
      });

      navigate(`/dashboard/${room.id}`);
    } catch (err) {
      console.error("Create room error:", err);

      if (err.response?.data?.detail) {
        setError(
          typeof err.response.data.detail === "string"
            ? err.response.data.detail
            : "Unable to create room."
        );
      } else {
        setError(
          "Unable to connect to RoomSync backend. Make sure the backend is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="create-room-page">
      <nav className="navbar">
        <div className="brand">
          <div className="brand-mark">R</div>
          <span>RoomSync</span>
        </div>

        <button
          className="nav-button"
          onClick={() => navigate("/")}
        >
          Home
        </button>
      </nav>

      <section className="create-room-container">
        <button
          className="back-button"
          onClick={() => navigate("/")}
        >
          <ArrowLeft size={17} />
          Back
        </button>

        <div className="create-room-card">
          <div className="create-room-icon">
            <Home size={25} />
          </div>

          <div className="create-room-badge">
            <Sparkles size={15} />
            Start your workspace
          </div>

          <h1>
            Create your
            <span> RoomSync room.</span>
          </h1>

          <p className="create-room-description">
            Set up your shared space and let RoomSync handle
            members, tasks and fair task rotation.
          </p>

          <form onSubmit={handleCreateRoom}>
            <div className="form-group">
              <label htmlFor="roomName">
                Room name
              </label>

              <input
                id="roomName"
                type="text"
                placeholder="e.g. Room 302"
                value={roomName}
                onChange={(event) =>
                  setRoomName(event.target.value)
                }
                maxLength={100}
                disabled={loading}
                autoFocus
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">
                Description
                <span>Optional</span>
              </label>

              <textarea
                id="description"
                placeholder="e.g. Shared room for our college group"
                value={description}
                onChange={(event) =>
                  setDescription(event.target.value)
                }
                maxLength={255}
                rows={4}
                disabled={loading}
              />
            </div>

            {error && (
              <div className="form-error">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="primary-button create-room-submit"
              disabled={loading}
            >
              {loading ? (
                "Creating room..."
              ) : (
                <>
                  Create Room
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>

          <div className="create-room-note">
            <div className="note-dot" />

            <p>
              You can add your members and daily tasks
              after creating the room.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default CreateRoomPage;