import { useState } from "react";
import { ArrowRight, Mail, UserRound } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { register } from "../services/authService";

function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");

      await register(form);

      navigate("/login");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to create your account."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="brand-mark">R</div>
          <span>RoomSync</span>
        </div>

        <div className="auth-heading">
          <span className="eyebrow">GET STARTED</span>
          <h1>Create your account</h1>
          <p>Join your room and sync your daily workflow.</p>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Full name
            <div className="auth-input">
              <UserRound size={18} />
              <input
                type="text"
                placeholder="Your full name"
                value={form.full_name}
                onChange={(e) =>
                  setForm({
                    ...form,
                    full_name: e.target.value,
                  })
                }
              />
            </div>
          </label>

          <label>
            Username
            <div className="auth-input">
              <UserRound size={18} />
              <input
                type="text"
                placeholder="Choose a username"
                value={form.username}
                onChange={(e) =>
                  setForm({
                    ...form,
                    username: e.target.value,
                  })
                }
                required
              />
            </div>
          </label>

          <label>
            Email
            <div className="auth-input">
              <Mail size={18} />
              <input
                type="email"
                placeholder="you@example.com"
                value={form.email}
                onChange={(e) =>
                  setForm({
                    ...form,
                    email: e.target.value,
                  })
                }
                required
              />
            </div>
          </label>

          <label>
            Password
            <div className="auth-input">
              <input
                type="password"
                placeholder="Minimum 6 characters"
                value={form.password}
                onChange={(e) =>
                  setForm({
                    ...form,
                    password: e.target.value,
                  })
                }
                required
              />
            </div>
          </label>

          <button
            className="auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading ? "Creating..." : "Create account"}
            {!loading && <ArrowRight size={18} />}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{" "}
          <Link to="/login">Sign in</Link>
        </p>
      </div>
    </main>
  );
}

export default RegisterPage;