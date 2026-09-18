import {
  Bell,
  CheckCircle2,
  ClipboardList,
  LayoutDashboard,
  Users,
  Zap,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000";

function DashboardPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [room, setRoom] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const [roomResponse, tasksResponse, membersResponse] =
          await Promise.all([
            fetch(`${API_URL}/rooms/${roomId}`),
            fetch(`${API_URL}/tasks/room/${roomId}`),
            fetch(`${API_URL}/members/room/${roomId}`),
          ]);

        if (!roomResponse.ok) {
          throw new Error("Room could not be loaded.");
        }

        if (!tasksResponse.ok) {
          throw new Error("Tasks could not be loaded.");
        }

        if (!membersResponse.ok) {
          throw new Error("Members could not be loaded.");
        }

        const roomData = await roomResponse.json();
        const tasksData = await tasksResponse.json();
        const membersData = await membersResponse.json();

        setRoom(roomData);
        setTasks(tasksData);
        setMembers(membersData);
      } catch (err) {
        console.error(err);
        setError(err.message || "Something went wrong.");
      } finally {
        setLoading(false);
      }
    }

    if (roomId) {
      loadDashboard();
    }
  }, [roomId]);

  const completedTasks = tasks.filter(
    (task) => task.is_completed === true
  );

  const activeMembers = members.filter(
    (member) => member.is_active !== false
  );

  const completionPercentage =
    tasks.length > 0
      ? Math.round((completedTasks.length / tasks.length) * 100)
      : 0;

  if (loading) {
    return (
      <main className="dashboard-page">
        <section className="dashboard-main">
          <div className="dashboard-panel">
            <h2>Loading RoomSync...</h2>
            <p>Getting your room data.</p>
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
            <h2>Unable to load dashboard</h2>
            <p>{error}</p>

            <button
              className="primary-button"
              onClick={() => navigate("/")}
              style={{ marginTop: "20px" }}
            >
              Back to Home
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
          {/* OVERVIEW */}
          <button
            className="dashboard-nav-item active"
            onClick={() => navigate(`/dashboard/${roomId}`)}
          >
            <LayoutDashboard size={19} />
            Overview
          </button>

          {/* TASKS */}
          <button className="dashboard-nav-item">
            <ClipboardList size={19} />
            Tasks
          </button>

          {/* MEMBERS */}
          <button
            className="dashboard-nav-item"
            onClick={() => navigate(`/dashboard/${roomId}/members`)}
          >
            <Users size={19} />
            Members
          </button>

          {/* SMART FLOW */}
          <button className="dashboard-nav-item">
            <Zap size={19} />
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
            <span className="eyebrow">
              ROOM {roomId} · TODAY
            </span>

            <h1>Good evening 👋</h1>

            <p>
              Here's what's happening in{" "}
              {room?.name || "your room"}.
            </p>
          </div>

          <button className="notification-button">
            <Bell size={20} />
            <span />
          </button>
        </header>

        {/* STATS */}
        <div className="dashboard-stats">
          {/* TODAY'S TASKS */}
          <div className="dashboard-stat">
            <span>Today's tasks</span>

            <strong>
              {String(tasks.length).padStart(2, "0")}
            </strong>

            <small>
              {tasks.length === 0
                ? "No tasks yet"
                : `${tasks.length - completedTasks.length} remaining`}
            </small>
          </div>

          {/* COMPLETED */}
          <div className="dashboard-stat">
            <span>Completed</span>

            <strong>
              {String(completedTasks.length).padStart(2, "0")}
            </strong>

            <small>
              {tasks.length === 0
                ? "No tasks yet"
                : `${completionPercentage}% complete`}
            </small>
          </div>

          {/* MEMBERS */}
          <div className="dashboard-stat">
            <span>Members online</span>

            <strong>
              {String(activeMembers.length).padStart(2, "0")}
            </strong>

            <small>
              {members.length === 0
                ? "No members yet"
                : `${members.length} member${
                    members.length === 1 ? "" : "s"
                  } in room`}
            </small>
          </div>

          {/* FAIRNESS */}
          <div className="dashboard-stat">
            <span>Fairness score</span>

            <strong>—</strong>

            <small>
              {members.length > 0
                ? "Calculated by Smart Flow"
                : "Not enough data"}
            </small>
          </div>
        </div>

        {/* LOWER GRID */}
        <div className="dashboard-grid">
          {/* TASK WORKFLOW */}
          <section className="dashboard-panel tasks-panel">
            <div className="panel-header">
              <div>
                <span className="panel-eyebrow">
                  TODAY
                </span>

                <h2>Task workflow</h2>
              </div>

              <button className="text-button">
                View all
              </button>
            </div>

            {tasks.length === 0 ? (
              <div
                style={{
                  textAlign: "center",
                  padding: "55px 20px",
                  color: "#777",
                }}
              >
                <ClipboardList
                  size={38}
                  style={{ marginBottom: "12px" }}
                />

                <h3
                  style={{
                    margin: "0 0 6px",
                    color: "#101114",
                  }}
                >
                  No tasks yet
                </h3>

                <p style={{ margin: 0 }}>
                  Create your first task to get started.
                </p>
              </div>
            ) : (
              tasks.slice(0, 5).map((task) => {
                const isCompleted =
                  task.is_completed === true;

                return (
                  <div
                    className="dashboard-task"
                    key={task.id}
                  >
                    <div className="task-left">
                      <div
                        className={`task-check ${
                          isCompleted
                            ? "done"
                            : "pending"
                        }`}
                      >
                        {isCompleted ? (
                          <CheckCircle2 size={18} />
                        ) : (
                          <ClipboardList size={18} />
                        )}
                      </div>

                      <div>
                        <strong>{task.name}</strong>

                        <span>
                          {task.description ||
                            "No description"}
                        </span>
                      </div>
                    </div>

                    <span
                      className={
                        isCompleted
                          ? "completed-tag"
                          : "assigned-tag"
                      }
                    >
                      {isCompleted
                        ? "Completed"
                        : "Active"}
                    </span>
                  </div>
                );
              })
            )}
          </section>

          {/* SMART FLOW */}
          <section className="dashboard-panel flow-panel">
            <div className="panel-header">
              <div>
                <span className="panel-eyebrow">
                  SMART FLOW
                </span>

                <h2>Fairness</h2>
              </div>

              <Zap size={20} />
            </div>

            <div className="fairness-circle">
              <strong>—</strong>
              <span>/100</span>
            </div>

            <p>
              {members.length === 0
                ? "Add members to start the Smart Flow."
                : "Fairness will be calculated from actual task assignments and completion history."}
            </p>

            <div className="fairness-bar">
              <span
                style={{
                  width: "0%",
                }}
              />
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

export default DashboardPage;