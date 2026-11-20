import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { logout } from "../../services/authService";

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <button
      type="button"
      className="roomsync-logout-button"
      onClick={handleLogout}
    >
      <LogOut size={17} />
      <span>Logout</span>
    </button>
  );
}

export default LogoutButton;