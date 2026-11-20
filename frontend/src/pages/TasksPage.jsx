import { useCallback, useEffect, useState } from "react";
import {
  ArrowLeft,
  CheckCircle2,
  ClipboardList,
  Loader2,
  Plus,
  RefreshCw,
  Trash2,
  X,
} from "lucide-react";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import { getRoom } from "../services/roomService";
import {
  createTask,
  deactivateTask,
  getRoomTasks,
} from "../services/taskService";

function TasksPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [room, setRoom] = useState(null);
  const [tasks, setTasks] = useState([]);

  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    name: "",
    description: "",
    frequency: "daily",
  });

  const getErrorMessage = (err) => {
    const detail = err?.response?.data?.detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          if (typeof item === "string") {
            return item;
          }

          if (typeof item?.msg === "string") {
            return item.msg;
          }

          return "Invalid request.";
        })
        .join(", ");
    }

    if (detail && typeof detail === "object") {
      return (
        detail.msg ||
        detail.message ||
        "Invalid request."
      );
    }

    return err?.message || "Something went wrong.";
  };

  const fetchData = useCallback(async () => {
    try {
      setError("");

      const [roomData, taskData] = await Promise.all([
        getRoom(roomId),
        getRoomTasks(roomId),
      ]);

      setRoom(roomData);

      setTasks(
        Array.isArray(taskData) ? taskData : []
      );
    } catch (err) {
      console.error("Tasks page error:", err);
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [roomId]);

  const loadData = async () => {
    setLoading(true);
    await fetchData();
  };

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleCreateTask = async (event) => {
    event.preventDefault();

    if (!form.name.trim()) {
      setError("Please enter a task name.");
      return;
    }

    try {
      setCreating(true);
      setError("");
      setSuccess("");

      await createTask({
        name: form.name.trim(),
        description: form.description.trim() || null,
        frequency: form.frequency,
        room_id: Number(roomId),
      });

      setForm({
        name: "",
        description: "",
        frequency: "daily",
      });

      setSuccess("Task created successfully.");

      await loadData();
    } catch (err) {
      console.error("Create task error:", err);
      setError(getErrorMessage(err));
    } finally {
      setCreating(false);
    }
  };

  const handleDeactivateTask = async (taskId) => {
    const confirmed = window.confirm(
      "Are you sure you want to remove this task?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingId(taskId);
      setError("");
      setSuccess("");

      await deactivateTask(taskId);

      setSuccess("Task removed successfully.");

      await loadData();
    } catch (err) {
      console.error("Deactivate task error:", err);
      setError(getErrorMessage(err));
    } finally {
      setDeletingId(null);
    }
  };

  const activeTasks = tasks.filter(
    (task) => task.is_active
  );

  return (
    <main className="tasks-page">
      <div className="tasks-shell">

        <header className="tasks-header">
          <div>
            <button
              type="button"
              className="tasks-back"
              onClick={() =>
                navigate(`/dashboard/${roomId}`)
              }
            >
              <ArrowLeft size={16} />
              Dashboard
            </button>

            <span className="tasks-eyebrow">
              ROOM WORKFLOW
            </span>

            <h1>{room?.name || "Tasks"}</h1>

            <p>
              Create and manage tasks for this
              RoomSync workspace.
            </p>
          </div>

          <button
            type="button"
            className="tasks-refresh"
            onClick={loadData}
            disabled={loading}
          >
            <RefreshCw
              size={16}
              className={loading ? "tasks-spin" : ""}
            />
            Refresh
          </button>
        </header>

        {error && (
          <div className="tasks-message tasks-error">
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
          <div className="tasks-message tasks-success">
            <CheckCircle2 size={16} />
            <span>{success}</span>

            <button
              type="button"
              onClick={() => setSuccess("")}
            >
              <X size={15} />
            </button>
          </div>
        )}

        <section className="tasks-stats">

          <div className="tasks-stat-card">
            <div className="tasks-stat-icon">
              <ClipboardList size={18} />
            </div>

            <div>
              <span>Total Tasks</span>
              <strong>{tasks.length}</strong>
            </div>
          </div>

          <div className="tasks-stat-card">
            <div className="tasks-stat-icon">
              <CheckCircle2 size={18} />
            </div>

            <div>
              <span>Active Tasks</span>
              <strong>{activeTasks.length}</strong>
            </div>
          </div>

          <div className="tasks-stat-card">
            <div className="tasks-stat-icon">
              <ClipboardList size={18} />
            </div>

            <div>
              <span>Frequency</span>
              <strong>
                {activeTasks.length > 0
                  ? "Scheduled"
                  : "None"}
              </strong>
            </div>
          </div>

        </section>

        <section className="tasks-create-card">

          <div className="tasks-card-heading">
            <div className="tasks-heading-icon">
              <Plus size={19} />
            </div>

            <div>
              <h2>Create a Task</h2>

              <p>
                Add a new task to this workspace.
              </p>
            </div>
          </div>

          <form
            className="tasks-form"
            onSubmit={handleCreateTask}
          >
            <div className="tasks-form-grid">

              <label>
                <span>Task Name</span>

                <input
                  type="text"
                  name="name"
                  placeholder="e.g. Prepare weekly report"
                  value={form.name}
                  onChange={handleChange}
                  disabled={creating}
                  required
                />
              </label>

              <label>
                <span>Frequency</span>

                <select
                  name="frequency"
                  value={form.frequency}
                  onChange={handleChange}
                  disabled={creating}
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="once">Once</option>
                </select>
              </label>

            </div>

            <label>
              <span>Description</span>

              <textarea
                name="description"
                placeholder="Describe what needs to be done..."
                value={form.description}
                onChange={handleChange}
                disabled={creating}
                rows={3}
              />
            </label>

            <button
              type="submit"
              className="tasks-create-button"
              disabled={creating}
            >
              {creating ? (
                <>
                  <Loader2
                    size={16}
                    className="tasks-spin"
                  />
                  Creating...
                </>
              ) : (
                <>
                  <Plus size={16} />
                  Create Task
                </>
              )}
            </button>
          </form>
        </section>

        <section className="tasks-list-card">

          <div className="tasks-card-heading">
            <div className="tasks-heading-icon">
              <ClipboardList size={19} />
            </div>

            <div>
              <h2>Room Tasks</h2>

              <p>
                Tasks currently configured for this room.
              </p>
            </div>

            <span className="tasks-count">
              {tasks.length}
            </span>
          </div>

          {loading ? (
            <div className="tasks-empty">
              <RefreshCw
                size={25}
                className="tasks-spin"
              />

              <h3>Loading tasks...</h3>
            </div>
          ) : tasks.length === 0 ? (
            <div className="tasks-empty">
              <div className="tasks-empty-icon">
                <ClipboardList size={27} />
              </div>

              <h3>No tasks yet</h3>

              <p>
                Create your first task using the
                form above.
              </p>
            </div>
          ) : (
            <div className="tasks-list">
              {tasks.map((task) => (
                <article
                  className="task-row"
                  key={task.id}
                >
                  <div className="task-row-icon">
                    <ClipboardList size={17} />
                  </div>

                  <div className="task-row-content">
                    <div className="task-row-title">
                      <h3>{task.name}</h3>

                      <span
                        className={
                          task.is_active
                            ? "task-status active"
                            : "task-status inactive"
                        }
                      >
                        {task.is_active
                          ? "Active"
                          : "Inactive"}
                      </span>
                    </div>

                    {task.description && (
                      <p>{task.description}</p>
                    )}

                    <div className="task-row-meta">
                      <span>
                        Frequency:{" "}
                        <strong>{task.frequency}</strong>
                      </span>

                      <span>Task #{task.id}</span>
                    </div>
                  </div>

                  {task.is_active && (
                    <button
                      type="button"
                      className="task-delete-button"
                      disabled={deletingId === task.id}
                      onClick={() =>
                        handleDeactivateTask(task.id)
                      }
                    >
                      {deletingId === task.id ? (
                        <Loader2
                          size={15}
                          className="tasks-spin"
                        />
                      ) : (
                        <Trash2 size={15} />
                      )}

                      Remove
                    </button>
                  )}
                </article>
              ))}
            </div>
          )}

        </section>
      </div>
    </main>
  );
}

export default TasksPage;