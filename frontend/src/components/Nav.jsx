import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Nav() {
  const location = useLocation();

  const isPlayersActive =
    location.pathname === "/" ||
    location.pathname.startsWith("/players");

  return (
    <nav>
      <Link to="/" className="logo" style={{ textDecoration: "none", color: "inherit" }}>
        ⚽ FootballVerse
      </Link>

      <div className="nav-links">
        <Link
          to="/"
          className={isPlayersActive ? "active" : ""}
          style={{ textDecoration: "none" }}
        >
          Players
        </Link>
        <Link
          to="/stories"
          className={location.pathname === "/stories" ? "active" : ""}
          style={{ textDecoration: "none" }}
        >
          Stories
        </Link>
        <Link
          to="/dashboard"
          className={location.pathname === "/dashboard" ? "active" : ""}
          style={{ textDecoration: "none" }}
        >
          Dashboard
        </Link>
      </div>
    </nav>
  );
}
