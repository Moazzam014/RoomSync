import {
  ArrowLeft,
  MoreHorizontal,
  UserPlus,
  Users,
  UserCheck,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000";

function MembersPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [members, setMembers] = useState([]);
  const [room, setRoom] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMembers() {
      try {
        setLoading(true);

        const [membersResponse, roomResponse] =
          await Promise.all([
            fetch(`${API_URL}/members/room/${roomId}`),
            fetch(`${API_URL}/rooms/${roomId}`),
          ]);

        if (!membersResponse.ok) {
          throw new Error("Members could not be loaded.");
        }

        const membersData = await membersResponse.json();

        let roomData = null;

        if (roomResponse.ok) {
          roomData = await roomResponse.json();
        }

        setMembers(membersData);
        setRoom(roomData);
      } catch (err) {
        console.error(err);
        setError(
          err.message || "Something went wrong."
        );
      } finally {
        setLoading(false);
      }
    }

    if (roomId) {
      loadMembers();
    }
  }, [roomId]);

  const activeMembers = members.filter(
    (member) => member.is_active !== false
  );

  const irregularMembers = members.filter(
    (member) => member.is_irregular === true
  );

  if (loading) {
    return (
      <main className="dashboard-page">
        <section className="dashboard-main">
          <div className="dashboard-panel">
            <h2>Loading members...</h2>
            <p>Getting your room members.</p>
          </div>
        </section>
      </main>
    );
  }

  if (error) {
    return (
      <main className="dashboard-page">
        <section className="dashboard-main">
          <div className="dashboard-panel">
            <h2>Unable to load members</h2>
            <p>{error}</p>

            <button
              className="primary-button"
              onClick={() =>
                navigate(`/dashboard/${roomId}`)
              }
              style={{ marginTop: "20px" }}
            >
              Back to Dashboard
            </button>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="dashboard-page">
      {/* SIDEBAR */}
      <aside className="dashboard-sidebar">
        <div className="brand dashboard-brand">
          <div className="brand-mark">R</div>
          <span>RoomSync</span>
        </div>

        <nav className="dashboard-nav">
          <button
            className="dashboard-nav-item"
            onClick={() =>
              navigate(`/dashboard/${roomId}`)
            }
          >
            <Users size={19} />
            Overview
          </button>

          <button className="dashboard-nav-item">
            <UserCheck size={19} />
            Tasks
          </button>

          <button className="dashboard-nav-item active">
            <Users size={19} />
            Members
          </button>

          <button className="dashboard-nav-item">
            <UserCheck size={19} />
            Smart Flow
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="room-mini">
            <span>ROOM</span>
            <strong>
              {room?.name || `Room ${roomId}`}
            </strong>
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <section className="dashboard-main">
        <header className="dashboard-header">
          <div>
            <button
              className="back-button"
              onClick={() =>
                navigate(`/dashboard/${roomId}`)
              }
              style={{
                marginBottom: "15px",
              }}
            >
              <ArrowLeft size={16} />
              Back to overview
            </button>

            <span className="eyebrow">
              ROOM MEMBERS
            </span>

            <h1>Members</h1>

            <p>
              Manage the people participating in{" "}
              {room?.name || "your room"}.
            </p>
          </div>

          <button className="primary-button">
            <UserPlus size={18} />
            Add member
          </button>
        </header>

        {/* MEMBER STATS */}
        <div className="dashboard-stats">
          <div className="dashboard-stat">
            <span>Total members</span>

            <strong>
              {String(members.length).padStart(2, "0")}
            </strong>

            <small>
              People in this room
            </small>
          </div>

          <div className="dashboard-stat">
            <span>Active</span>

            <strong>
              {String(activeMembers.length).padStart(
                2,
                "0"
              )}
            </strong>

            <small>
              Currently active
            </small>
          </div>

          <div className="dashboard-stat">
            <span>Irregular</span>

            <strong>
              {String(irregularMembers.length).padStart(
                2,
                "0"
              )}
            </strong>

            <small>
              Special scheduling
            </small>
          </div>

          <div className="dashboard-stat">
            <span>Room capacity</span>

            <strong>
              {members.length}/7
            </strong>

            <small>
              RoomSync supports 4–7 members
            </small>
          </div>
        </div>

        {/* MEMBERS PANEL */}
        <section
          className="dashboard-panel"
          style={{ marginTop: "18px" }}
        >
          <div className="panel-header">
            <div>
              <span className="panel-eyebrow">
                PEOPLE
              </span>

              <h2>Room members</h2>
            </div>

            <span
              style={{
                color: "#777",
                fontSize: "12px",
              }}
            >
              {members.length} member
              {members.length === 1 ? "" : "s"}
            </span>
          </div>

          {members.length === 0 ? (
            <div
              style={{
                textAlign: "center",
                padding: "70px 20px",
                color: "#777",
              }}
            >
              <div
                style={{
                  width: "58px",
                  height: "58px",
                  margin: "0 auto 15px",
                  display: "grid",
                  placeItems: "center",
                  borderRadius: "16px",
                  background: "#f0edff",
                  color: "#7657ff",
                }}
              >
                <Users size={28} />
              </div>

              <h3
                style={{
                  margin: "0 0 7px",
                  color: "#101114",
                }}
              >
                No members yet
              </h3>

              <p style={{ margin: 0 }}>
                Add members to start your shared
                workflow.
              </p>
            </div>
          ) : (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                marginTop: "18px",
              }}
            >
              {members.map((member, index) => {
                const isActive =
                  member.is_active !== false;

                return (
                  <div
                    key={member.id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      padding: "16px",
                      border: "1px solid #e5e5e8",
                      borderRadius: "14px",
                      background: "#fff",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "13px",
                      }}
                    >
                      <div
                        style={{
                          width: "42px",
                          height: "42px",
                          display: "grid",
                          placeItems: "center",
                          borderRadius: "12px",
                          background: "#f0edff",
                          color: "#7657ff",
                          fontWeight: "700",
                        }}
                      >
                        {member.name
                          ?.charAt(0)
                          ?.toUpperCase() || "M"}
                      </div>

                      <div>
                        <strong
                          style={{
                            display: "block",
                            fontSize: "14px",
                          }}
                        >
                          {member.name}
                        </strong>

                        <span
                          style={{
                            display: "block",
                            marginTop: "3px",
                            color: "#888",
                            fontSize: "11px",
                          }}
                        >
                          {member.total_tasks_completed ||
                            0}{" "}
                          tasks completed
                        </span>
                      </div>
                    </div>

                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "12px",
                      }}
                    >
                      <span
                        style={{
                          padding: "6px 9px",
                          borderRadius: "8px",
                          background: isActive
                            ? "#e9f9f0"
                            : "#f1f1f3",
                          color: isActive
                            ? "#15945b"
                            : "#777",
                          fontSize: "9px",
                          fontWeight: "700",
                        }}
                      >
                        {isActive
                          ? "ACTIVE"
                          : "INACTIVE"}
                      </span>

                      <button
                        style={{
                          width: "34px",
                          height: "34px",
                          display: "grid",
                          placeItems: "center",
                          borderRadius: "9px",
                          background: "#f7f7f8",
                          color: "#777",
                        }}
                      >
                        <MoreHorizontal size={18} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

export default MembersPage;