import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Nav() {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAdmin, logout } = useAuth();

  const isPlayersActive =
    location.pathname === "/" || location.pathname.startsWith("/players");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav>
      <Link to="/" className="logo" style={{ textDecoration: "none", color: "inherit" }}>
        ⚽ FootballVerse
      </Link>

      <div className="nav-links">
        <Link to="/" className={isPlayersActive ? "active" : ""} style={{ textDecoration: "none" }}>
          Players
        </Link>
        <Link to="/stories" className={location.pathname === "/stories" ? "active" : ""} style={{ textDecoration: "none" }}>
          Stories
        </Link>

        {isAdmin ? (
          <>
            <Link to="/dashboard" className={location.pathname === "/dashboard" ? "active" : ""} style={{ textDecoration: "none" }}>
              Dashboard
            </Link>
            <Link to="/studio" className={location.pathname.startsWith("/studio") ? "active" : ""} style={{ textDecoration: "none" }}>
              Story Studio
            </Link>
            <button onClick={handleLogout} style={{ border: "1px solid #31533a", background: "transparent", color: "#9dac9f", padding: "9px 12px", borderRadius: "8px" }}>
              Sign out
            </button>
          </>
        ) : (
          <Link to="/login" className={location.pathname === "/login" ? "active" : ""} style={{ textDecoration: "none" }}>
            Sign in
          </Link>
        )}
      </div>
    </nav>
  );
}
