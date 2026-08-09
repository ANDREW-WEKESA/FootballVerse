import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const API = "http://127.0.0.1:8000";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Login failed");
        return;
      }
      login(data.access_token);
      navigate("/dashboard");
    } catch {
      setError("Could not reach the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app" style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <nav>
        <div className="logo">⚽ FootballVerse</div>
      </nav>

      <main style={{ display: "flex", alignItems: "center", justifyContent: "center", flex: 1 }}>
        <div style={{ width: "100%", maxWidth: "420px", padding: "40px", borderRadius: "20px", background: "#0c1b11", border: "1px solid #23452c" }}>
          <span className="tag">ADMIN ACCESS</span>
          <h1 style={{ fontSize: "2rem", margin: "16px 0 8px" }}>Sign in</h1>
          <p style={{ color: "#9eada2", marginBottom: "32px" }}>FootballVerse creator dashboard</p>

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: "20px" }}>
              <label style={{ display: "block", marginBottom: "8px", color: "#c6d4ca", fontSize: "0.9rem" }}>
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoFocus
                style={{ width: "100%", padding: "12px 14px", borderRadius: "9px", background: "#102116", border: "1px solid #31533a", color: "#f3f7f4", fontSize: "1rem", outline: "none" }}
                placeholder="admin@footballverse.com"
              />
            </div>

            <div style={{ marginBottom: "24px" }}>
              <label style={{ display: "block", marginBottom: "8px", color: "#c6d4ca", fontSize: "0.9rem" }}>
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ width: "100%", padding: "12px 14px", borderRadius: "9px", background: "#102116", border: "1px solid #31533a", color: "#f3f7f4", fontSize: "1rem", outline: "none" }}
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div style={{ padding: "12px 16px", borderRadius: "9px", background: "#2a0e0e", border: "1px solid #7a2020", color: "#f87171", marginBottom: "20px", fontSize: "0.9rem" }}>
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              style={{ width: "100%", padding: "14px", borderRadius: "9px", background: loading ? "#1e4a28" : "#22c55e", border: "none", color: "#06100a", fontWeight: "800", fontSize: "1rem", cursor: loading ? "not-allowed" : "pointer" }}
            >
              {loading ? "Signing in..." : "Sign in →"}
            </button>
          </form>
        </div>
      </main>

      <footer>⚽ FootballVerse · Football knowledge brought to life</footer>
    </div>
  );
}
