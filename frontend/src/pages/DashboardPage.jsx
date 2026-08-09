import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import { useAuth } from "../context/AuthContext";

const API = "http://127.0.0.1:8000";

const STATUS_COLORS = {
  draft: { bg: "#1a2e1a", color: "#72e582", border: "#2d5a2d" },
  rendered: { bg: "#1a1a2e", color: "#818cf8", border: "#2d2d5a" },
  published: { bg: "#1a2a1a", color: "#22c55e", border: "#166534" },
};

export default function DashboardPage() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const headers = { Authorization: `Bearer ${token}` };

  const loadStories = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/stories`, { headers });
      if (!res.ok) throw new Error("Failed to load stories");
      const data = await res.json();
      setStories(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadStories(); }, []);

  const handlePublish = async (id) => {
    await fetch(`${API}/stories/${id}`, {
      method: "PUT",
      headers: { ...headers, "Content-Type": "application/json" },
      body: JSON.stringify({ status: "published" }),
    });
    loadStories();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this story? This cannot be undone.")) return;
    await fetch(`${API}/stories/${id}`, { method: "DELETE", headers });
    loadStories();
  };

  return (
    <div className="app">
      <Nav />
      <main>
        <section className="page-heading">
          <span className="tag">ADMIN</span>
          <h1>Dashboard</h1>
          <p>Manage your FootballVerse stories.</p>
        </section>

        <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "24px" }}>
          <Link to="/studio/new" style={{ textDecoration: "none", padding: "12px 20px", borderRadius: "9px", background: "#22c55e", color: "#06100a", fontWeight: "800", fontSize: "0.95rem" }}>
            + New Story
          </Link>
        </div>

        {loading && <div className="loading">Loading stories...</div>}

        {error && (
          <div style={{ padding: "20px", borderRadius: "12px", background: "#2a0e0e", border: "1px solid #7a2020", color: "#f87171", marginBottom: "20px" }}>
            {error} —{" "}
            <button onClick={loadStories} style={{ background: "none", border: "none", color: "#f87171", textDecoration: "underline", cursor: "pointer" }}>
              Retry
            </button>
          </div>
        )}

        {!loading && !error && stories.length === 0 && (
          <div className="empty">
            <div style={{ fontSize: "3rem", marginBottom: "16px" }}>🎬</div>
            <h2>No stories yet</h2>
            <p>Create your first football story in Story Studio.</p>
            <Link to="/studio/new" style={{ display: "inline-block", marginTop: "16px", padding: "12px 20px", borderRadius: "9px", background: "#22c55e", color: "#06100a", fontWeight: "800", textDecoration: "none" }}>
              Create first story
            </Link>
          </div>
        )}

        {!loading && stories.length > 0 && (
          <div style={{ display: "grid", gap: "14px" }}>
            {stories.map((story) => {
              const sc = STATUS_COLORS[story.status] || STATUS_COLORS.draft;
              return (
                <div key={story.id} style={{ display: "flex", alignItems: "center", gap: "20px", padding: "20px 24px", borderRadius: "14px", background: "#0c1b11", border: "1px solid #23452c", flexWrap: "wrap" }}>
                  <div style={{ flex: 1, minWidth: "200px" }}>
                    <h3 style={{ margin: "0 0 6px" }}>{story.title}</h3>
                    <p style={{ color: "#9eada2", margin: 0, fontSize: "0.9rem" }}>
                      {story.created_at ? new Date(story.created_at).toLocaleDateString() : "—"}
                    </p>
                  </div>

                  <span style={{ padding: "5px 12px", borderRadius: "20px", fontSize: "0.75rem", fontWeight: "800", letterSpacing: "0.06em", background: sc.bg, color: sc.color, border: `1px solid ${sc.border}` }}>
                    {story.status.toUpperCase()}
                  </span>

                  <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                    <button onClick={() => navigate(`/studio/${story.id}`)} className="secondary" style={{ fontSize: "0.85rem", padding: "8px 14px" }}>
                      Edit
                    </button>
                    {story.status === "rendered" && (
                      <button onClick={() => handlePublish(story.id)} style={{ padding: "8px 14px", borderRadius: "8px", background: "#166534", border: "1px solid #22c55e", color: "#22c55e", cursor: "pointer", fontSize: "0.85rem" }}>
                        Publish
                      </button>
                    )}
                    <button onClick={() => handleDelete(story.id)} style={{ padding: "8px 14px", borderRadius: "8px", background: "#2a0e0e", border: "1px solid #7a2020", color: "#f87171", cursor: "pointer", fontSize: "0.85rem" }}>
                      Delete
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
