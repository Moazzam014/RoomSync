import { ArrowRight, CheckCircle2, Sparkles, Users, Zap } from "lucide-react";
import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <main className="landing-page">
      <nav className="navbar">
        <div className="brand">
          <div className="brand-mark">R</div>
          <span>RoomSync</span>
        </div>

        <button
          className="nav-button"
          onClick={() => navigate("/create-room")}
        >
          Get Started
        </button>
      </nav>

      <section className="hero">
        <div className="hero-badge">
          <Sparkles size={16} />
          Intelligent room workflow
        </div>

        <h1>
          Your room.
          <br />
          <span>Perfectly synced.</span>
        </h1>

        <p className="hero-description">
          Manage members, tasks, presence and daily responsibilities
          with a workflow that keeps everyone fairly involved.
        </p>

        <div className="hero-actions">
          <button
            className="primary-button"
            onClick={() => navigate("/create-room")}
          >
            Create a Room
            <ArrowRight size={18} />
          </button>

          <button className="secondary-button">
            See how it works
          </button>
        </div>

        <div className="feature-row">
          <div className="feature-card">
            <div className="feature-icon">
              <Users size={20} />
            </div>

            <div>
              <strong>4–7 Members</strong>
              <span>Built for groups</span>
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <Zap size={20} />
            </div>

            <div>
              <strong>Smart Assignment</strong>
              <span>Fair task rotation</span>
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <CheckCircle2 size={20} />
            </div>

            <div>
              <strong>Live Progress</strong>
              <span>Stay accountable</span>
            </div>
          </div>
        </div>
      </section>

      <section className="preview-section">
        <div className="preview-window">
          <div className="window-top">
            <div className="window-dots">
              <span />
              <span />
              <span />
            </div>

            <div className="window-title">
              Room 302 · Today
            </div>
          </div>

          <div className="preview-content">
            <div className="preview-sidebar">
              <div className="mini-logo">R</div>

              <div className="sidebar-line active" />
              <div className="sidebar-line" />
              <div className="sidebar-line" />
              <div className="sidebar-line" />
            </div>

            <div className="preview-main">
              <div className="preview-heading">
                <div>
                  <small>GOOD MORNING</small>
                  <h3>Room 302</h3>
                </div>

                <div className="status-pill">
                  ● 4 members active
                </div>
              </div>

              <div className="preview-grid">
                <div className="preview-stat">
                  <span>Today's Tasks</span>
                  <strong>08</strong>
                </div>

                <div className="preview-stat">
                  <span>Completed</span>
                  <strong>05</strong>
                </div>

                <div className="preview-stat">
                  <span>Fairness</span>
                  <strong>94%</strong>
                </div>
              </div>

              <div className="task-preview">
                <div>
                  <span className="task-status" />
                  <div>
                    <strong>Room Cleaning</strong>
                    <small>Assigned to Unique</small>
                  </div>
                </div>

                <span className="task-badge">
                  Assigned
                </span>
              </div>

              <div className="task-preview">
                <div>
                  <span className="task-status completed" />
                  <div>
                    <strong>Kitchen Cleanup</strong>
                    <small>Completed by Member 2</small>
                  </div>
                </div>

                <span className="task-badge done">
                  Done
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default LandingPage;