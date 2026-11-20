import { useCallback, useEffect, useState } from "react";
import {
  ArrowLeft,
  Bell,
  CheckCircle2,
  ClipboardList,
  LayoutDashboard,
  RefreshCw,
  ShieldCheck,
  UserPlus,
  Users,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import { getRoom } from "../services/roomService";
import { getRoomMembers } from "../services/memberService";
import { getRoomTasks } from "../services/taskService";
import { getRoomWorkflow } from "../services/workflowService";
import LogoutButton from "../components/common/LogoutButton";

function DashboardPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [room, setRoom] = useState(null);
  const [members, setMembers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [rotations, setRotations] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchDashboard = useCallback(async () => {
    try {
      setError("");

      const [
        roomResult,
        membersResult,
        tasksResult,
        workflowResult,
      ] = await Promise.all([
        getRoom(roomId),
        getRoomMembers(roomId),
        getRoomTasks(roomId),
        getRoomWorkflow(roomId),
      ]);

      setRoom(roomResult);

      setMembers(
        Array.isArray(membersResult)
          ? membersResult
          : []
      );

      setTasks(
        Array.isArray(tasksResult)
          ? tasksResult
          : []
      );

      setRotations(
        Array.isArray(workflowResult?.rotations)
          ? workflowResult.rotations
          : []
      );
    } catch (err) {
      console.error("Dashboard loading error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to load this room."
      );
    } finally {
      setLoading(false);
    }
  }, [roomId]);

  const loadDashboard = async () => {
    setLoading(true);
    await fetchDashboard();
  };

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  const completedTasks = rotations.filter(
    (rotation) => rotation.is_completed
  ).length;

  const pendingTasks = rotations.filter(
    (rotation) => !rotation.is_completed
  ).length;

  // Workflow rotations are returned newest first.
  // Keep the latest rotation for each task.
  const latestRotationByTask = new Map();

  rotations.forEach((rotation) => {
    if (!latestRotationByTask.has(rotation.task_id)) {
      latestRotationByTask.set(
        rotation.task_id,
        rotation
      );
    }
  });

  const recentTasks = tasks.slice(0, 5);

  if (loading) {
    return (
      <main className="dashboard-page">
        <div className="dashboard-loading">
          <RefreshCw
            size={24}
            className="dashboard-spin"
          />

          <span>Loading room dashboard...</span>
        </div>
      </main>
    );
  }

  return (
    <main className="dashboard-page">
      <div className="dashboard-shell">

        <aside className="dashboard-sidebar">

          <div className="dashboard-brand">
            <div className="dashboard-brand-mark">
              R
            </div>

            <div>
              <strong>RoomSync</strong>
              <span>Team Workspace</span>
            </div>
          </div>

          <nav className="dashboard-nav">

            <button
              type="button"
              className="dashboard-nav-item active"
            >
              <LayoutDashboard size={18} />
              <span>Dashboard</span>
            </button>

            <button
              type="button"
              className="dashboard-nav-item"
              onClick={() =>
                navigate(`/dashboard/${roomId}/members`)
              }
            >
              <Users size={18} />
              <span>Members</span>
            </button>

            <button
              type="button"
              className="dashboard-nav-item"
              onClick={() =>
                navigate(`/dashboard/${roomId}/tasks`)
              }
            >
              <ClipboardList size={18} />
              <span>Tasks</span>
            </button>

            <button
              type="button"
              className="dashboard-nav-item"
              onClick={() => navigate("/invitations")}
            >
              <Bell size={18} />
              <span>Invitations</span>
            </button>

          </nav>

          <div className="dashboard-sidebar-bottom">

            <button
              type="button"
              className="dashboard-nav-item"
              onClick={() => navigate("/start")}
            >
              <ArrowLeft size={18} />
              <span>Overview</span>
            </button>

            <LogoutButton />

          </div>
        </aside>

        <section className="dashboard-main">

          <header className="dashboard-topbar">
            <div>
              <span className="dashboard-eyebrow">
                ROOM DASHBOARD
              </span>

              <h1>
                {room?.name || `Room #${roomId}`}
              </h1>

              <p>
                Manage your team, tasks and workflow
                from one place.
              </p>
            </div>

            <button
              type="button"
              className="dashboard-refresh-button"
              onClick={loadDashboard}
              disabled={loading}
            >
              <RefreshCw size={17} />
              Refresh
            </button>
          </header>

          {error && (
            <div className="dashboard-error">
              {error}

              <button
                type="button"
                onClick={loadDashboard}
              >
                Try Again
              </button>
            </div>
          )}

          <section className="dashboard-room-card">
            <div className="dashboard-room-left">
              <div className="dashboard-room-icon">
                <ShieldCheck size={25} />
              </div>

              <div>
                <span>Active Workspace</span>

                <h2>
                  {room?.name || `Room #${roomId}`}
                </h2>

                <p>
                  {room?.description ||
                    "Your RoomSync team workspace is ready."}
                </p>
              </div>
            </div>

            <button
              type="button"
              className="dashboard-manage-button"
              onClick={() =>
                navigate(`/dashboard/${roomId}/members`)
              }
            >
              <UserPlus size={17} />
              Manage Team
            </button>
          </section>

          <section className="dashboard-stats">

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                <Users size={20} />
              </div>

              <div>
                <span>Team Members</span>
                <strong>{members.length}</strong>
              </div>
            </div>

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                <ClipboardList size={20} />
              </div>

              <div>
                <span>Total Tasks</span>
                <strong>{tasks.length}</strong>
              </div>
            </div>

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                <CheckCircle2 size={20} />
              </div>

              <div>
                <span>Completed Rotations</span>
                <strong>{completedTasks}</strong>
              </div>
            </div>

            <div className="dashboard-stat-card">
              <div className="dashboard-stat-icon">
                <ClipboardList size={20} />
              </div>

              <div>
                <span>Pending Rotations</span>
                <strong>{pendingTasks}</strong>
              </div>
            </div>

          </section>

          <section className="dashboard-section">

            <div className="dashboard-section-heading">
              <div>
                <span>WORKSPACE</span>
                <h2>Quick Actions</h2>
              </div>
            </div>

            <div className="dashboard-actions-grid">

              <button
                type="button"
                className="dashboard-action-card"
                onClick={() =>
                  navigate(`/dashboard/${roomId}/members`)
                }
              >
                <div className="dashboard-action-icon">
                  <Users size={21} />
                </div>

                <div>
                  <strong>Manage Members</strong>
                  <span>Invite and manage teammates.</span>
                </div>

                <ArrowLeft
                  size={17}
                  className="dashboard-action-arrow"
                />
              </button>

              <button
                type="button"
                className="dashboard-action-card"
                onClick={() =>
                  navigate(`/dashboard/${roomId}/tasks`)
                }
              >
                <div className="dashboard-action-icon">
                  <ClipboardList size={21} />
                </div>

                <div>
                  <strong>Manage Tasks</strong>
                  <span>Create and manage room tasks.</span>
                </div>

                <ArrowLeft
                  size={17}
                  className="dashboard-action-arrow"
                />
              </button>

              <button
                type="button"
                className="dashboard-action-card"
                onClick={() => navigate("/invitations")}
              >
                <div className="dashboard-action-icon">
                  <Bell size={21} />
                </div>

                <div>
                  <strong>Invitations</strong>
                  <span>View pending invitations.</span>
                </div>

                <ArrowLeft
                  size={17}
                  className="dashboard-action-arrow"
                />
              </button>

              <button
                type="button"
                className="dashboard-action-card"
                onClick={() => navigate("/start")}
              >
                <div className="dashboard-action-icon">
                  <ArrowLeft size={21} />
                </div>

                <div>
                  <strong>Overview</strong>
                  <span>
                    Return to your workspace overview.
                  </span>
                </div>

                <ArrowLeft
                  size={17}
                  className="dashboard-action-arrow"
                />
              </button>

            </div>
          </section>

          <section className="dashboard-section">

            <div className="dashboard-section-heading">
              <div>
                <span>TASK OVERVIEW</span>
                <h2>Recent Tasks</h2>
              </div>

              <button
                type="button"
                className="dashboard-view-all"
                onClick={() =>
                  navigate(`/dashboard/${roomId}/tasks`)
                }
              >
                View all
              </button>
            </div>

            {recentTasks.length === 0 ? (
              <div className="dashboard-empty">
                <ClipboardList size={30} />

                <h3>No tasks yet</h3>

                <p>
                  Create your first task for this room.
                </p>

                <button
                  type="button"
                  onClick={() =>
                    navigate(`/dashboard/${roomId}/tasks`)
                  }
                >
                  Create Task
                </button>
              </div>
            ) : (
              <div className="dashboard-task-list">

                {recentTasks.map((task) => {
                  const latestRotation =
                    latestRotationByTask.get(task.id);

                  const isCompleted =
                    latestRotation?.is_completed === true;

                  const status = latestRotation
                    ? isCompleted
                      ? "Completed"
                      : "Pending"
                    : "Not assigned";

                  return (
                    <div
                      className="dashboard-task-row"
                      key={task.id}
                    >
                      <div className="dashboard-task-main">

                        <div className="dashboard-task-dot">
                          {isCompleted ? (
                            <CheckCircle2 size={17} />
                          ) : (
                            <ClipboardList size={17} />
                          )}
                        </div>

                        <div>
                          <strong>
                            {task.name || `Task #${task.id}`}
                          </strong>

                          <span>
                            {task.description || "Room task"}
                          </span>
                        </div>

                      </div>

                      <span
                        className={`dashboard-task-status ${
                          isCompleted
                            ? "completed"
                            : "pending"
                        }`}
                      >
                        {status}
                      </span>
                    </div>
                  );
                })}

              </div>
            )}

          </section>
        </section>
      </div>
    </main>
  );
}

export default DashboardPage;