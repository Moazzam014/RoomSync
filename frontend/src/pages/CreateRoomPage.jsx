import { useState } from "react";
import {
  ArrowLeft,
  Check,
  DoorOpen,
  Loader2,
  Sparkles,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { createRoom } from "../services/roomService";

function CreateRoomPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    description: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const roomName = form.name.trim();
    const description = form.description.trim();

    if (!roomName) {
      setError("Please enter a room name.");
      return;
    }

    if (roomName.length < 3) {
      setError(
        "Room name must be at least 3 characters."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      const room = await createRoom({
        name: roomName,
        description: description || null,
      });

      if (room?.id) {
        navigate(`/dashboard/${room.id}`, {
          replace: true,
        });
        return;
      }

      navigate("/start", {
        replace: true,
      });
    } catch (err) {
      console.error(
        "Create room error:",
        err
      );

      setError(
        err.response?.data?.detail ||
          "Unable to create room. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="create-room-page">
      <div className="create-room-shell">

        {/* HEADER */}

        <header className="create-room-header">

          <button
            type="button"
            className="create-room-back"
            onClick={() => navigate("/start")}
          >
            <ArrowLeft size={17} />
            Back to Overview
          </button>

          <div className="create-room-brand">
            <div className="create-room-brand-mark">
              R
            </div>

            <div>
              <strong>RoomSync</strong>
              <span>Team Workspace</span>
            </div>
          </div>

        </header>

        {/* CONTENT */}

        <section className="create-room-content">

          <div className="create-room-intro">

            <div className="create-room-icon">
              <DoorOpen size={27} />
            </div>

            <span className="create-room-eyebrow">
              NEW WORKSPACE
            </span>

            <h1>
              Create a Room
            </h1>

            <p>
              Set up a workspace for your team
              and invite members when you're ready.
            </p>

          </div>

          {/* FORM */}

          <form
            className="create-room-form"
            onSubmit={handleSubmit}
          >

            {error && (
              <div className="create-room-error">
                {error}
              </div>
            )}

            <div className="create-room-field">

              <label htmlFor="room-name">
                Room Name
              </label>

              <input
                id="room-name"
                name="name"
                type="text"
                placeholder="e.g. Project Alpha"
                value={form.name}
                onChange={handleChange}
                maxLength={100}
                autoFocus
                disabled={loading}
              />

              <span>
                Choose a clear name your team
                will recognize.
              </span>

            </div>

            <div className="create-room-field">

              <label htmlFor="room-description">
                Description
                <small>Optional</small>
              </label>

              <textarea
                id="room-description"
                name="description"
                placeholder="What is this room for?"
                value={form.description}
                onChange={handleChange}
                maxLength={500}
                rows={5}
                disabled={loading}
              />

              <span>
                Add a short description to give
                your teammates some context.
              </span>

            </div>

            {/* INFO */}

            <div className="create-room-info">

              <div className="create-room-info-icon">
                <Sparkles size={17} />
              </div>

              <div>
                <strong>
                  Your workspace starts here
                </strong>

                <p>
                  After creating the room, you can
                  invite registered RoomSync users
                  from the Members section.
                </p>
              </div>

            </div>

            {/* BUTTONS */}

            <div className="create-room-actions">

              <button
                type="button"
                className="create-room-cancel"
                onClick={() =>
                  navigate("/start")
                }
                disabled={loading}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="create-room-submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2
                      size={17}
                      className="create-room-spinner"
                    />
                    Creating...
                  </>
                ) : (
                  <>
                    <Check size={17} />
                    Create Room
                  </>
                )}
              </button>

            </div>

          </form>

        </section>

      </div>
    </main>
  );
}

export default CreateRoomPage;