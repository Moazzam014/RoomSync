import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("roomsync_token");
    localStorage.removeItem("roomsync_user");

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