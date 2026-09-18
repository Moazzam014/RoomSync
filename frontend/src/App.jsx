import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";

import LandingPage from "./pages/LandingPage";
import CreateRoomPage from "./pages/CreateRoomPage";
import DashboardPage from "./pages/DashboardPage";
import MembersPage from "./pages/MembersPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/create-room" element={<CreateRoomPage />} />

        <Route
          path="/dashboard/:roomId"
          element={<DashboardPage />}
        />

        <Route
          path="/dashboard/:roomId/members"
          element={<MembersPage />}
        />

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;