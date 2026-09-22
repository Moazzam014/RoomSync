import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import "./App.css";

import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import StartPage from "./pages/StartPage";
import CreateRoomPage from "./pages/CreateRoomPage";
import MyRoomsPage from "./pages/MyRoomsPage";
import DashboardPage from "./pages/DashboardPage";
import MembersPage from "./pages/MembersPage";
import TasksPage from "./pages/TasksPage";
import InvitationsPage from "./pages/InvitationsPage";

function isLoggedIn() {
  return Boolean(
    localStorage.getItem("roomsync_token")
  );
}

function ProtectedRoute({ children }) {
  if (!isLoggedIn()) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  return children;
}

function PublicRoute({ children }) {
  if (isLoggedIn()) {
    return (
      <Navigate
        to="/start"
        replace
      />
    );
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* =========================
            PUBLIC ROUTES
        ========================= */}

        <Route
          path="/"
          element={
            <PublicRoute>
              <LandingPage />
            </PublicRoute>
          }
        />

        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />

        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* =========================
            MAIN OVERVIEW
        ========================= */}

        <Route
          path="/start"
          element={
            <ProtectedRoute>
              <StartPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            MY ROOMS
        ========================= */}

        <Route
          path="/rooms"
          element={
            <ProtectedRoute>
              <MyRoomsPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            CREATE ROOM
        ========================= */}

        <Route
          path="/create-room"
          element={
            <ProtectedRoute>
              <CreateRoomPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            ROOM DASHBOARD
        ========================= */}

        <Route
          path="/dashboard/:roomId"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            ROOM MEMBERS
        ========================= */}

        <Route
          path="/dashboard/:roomId/members"
          element={
            <ProtectedRoute>
              <MembersPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            ROOM TASKS
        ========================= */}

        <Route
          path="/dashboard/:roomId/tasks"
          element={
            <ProtectedRoute>
              <TasksPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            INVITATIONS
        ========================= */}

        <Route
          path="/invitations"
          element={
            <ProtectedRoute>
              <InvitationsPage />
            </ProtectedRoute>
          }
        />

        {/* =========================
            FALLBACK
        ========================= */}

        <Route
          path="*"
          element={
            <Navigate
              to={
                isLoggedIn()
                  ? "/start"
                  : "/"
              }
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;