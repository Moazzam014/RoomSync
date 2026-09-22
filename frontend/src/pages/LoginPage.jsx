import { useState } from "react";
import {
  ArrowRight,
  LockKeyhole,
  UserRound,
} from "lucide-react";
import {
  Link,
  useNavigate,
} from "react-router-dom";

import { login } from "../services/authService";

function LoginPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");

      const data = await login(
        form.username.trim(),
        form.password
      );

      localStorage.setItem(
        "roomsync_token",
        data.access_token
      );

      if (data.user) {
        localStorage.setItem(
          "roomsync_user",
          JSON.stringify(data.user)
        );
      }

      navigate("/start", {
        replace: true,
      });
    } catch (err) {
      console.error("Login error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to login. Please check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-card">

        <div className="auth-brand">
          <div className="brand-mark">
            R
          </div>

          <span>
            RoomSync
          </span>
        </div>

        <div className="auth-heading">
          <span className="eyebrow">
            WELCOME BACK
          </span>

          <h1>
            Sign in to RoomSync
          </h1>

          <p>
            Manage your rooms, tasks and
            team workflow.
          </p>
        </div>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="auth-form"
        >

          <label>
            Username

            <div className="auth-input">
              <UserRound size={18} />

              <input
                type="text"
                placeholder="Enter username"
                value={form.username}
                onChange={(event) =>
                  setForm({
                    ...form,
                    username:
                      event.target.value,
                  })
                }
                autoComplete="username"
                required
              />
            </div>
          </label>

          <label>
            Password

            <div className="auth-input">
              <LockKeyhole size={18} />

              <input
                type="password"
                placeholder="Enter password"
                value={form.password}
                onChange={(event) =>
                  setForm({
                    ...form,
                    password:
                      event.target.value,
                  })
                }
                autoComplete="current-password"
                required
              />
            </div>
          </label>

          <button
            className="auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign in"}

            {!loading && (
              <ArrowRight size={18} />
            )}
          </button>

        </form>

        <p className="auth-footer">
          Don't have an account?{" "}
          <Link to="/register">
            Create one
          </Link>
        </p>

      </div>
    </main>
  );
}

export default LoginPage;