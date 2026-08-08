import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [stories, setStories] = useState([]);
  const [players, setPlayers] = useState([]);
  const [clubs, setClubs] = useState([]);
  const [media, setMedia] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [saving, setSaving] = useState(false);

  const [form, setForm] = useState({
    title: "",
    category: "Football History",
    description: "",
    duration: 5
  });

  const loadData = async () => {
    try {
      const [s, p, c, m] = await Promise.all([
        fetch(`${API}/stories`).then(r => r.json()),
        fetch(`${API}/players`).then(r => r.json()),
        fetch(`${API}/clubs`).then(r => r.json()),
        fetch(`${API}/media`).then(r => r.json())
      ]);
      setStories(s);
      setPlayers(p);
      setClubs(c);
      setMedia(m);
    } catch (error) {
      console.error("API error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const createStory = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const response = await fetch(`${API}/stories`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          duration: Number(form.duration)
        })
      });

      if (!response.ok) {
        throw new Error("Failed to create story");
      }

      setForm({
        title: "",
        category: "Football History",
        description: "",
        duration: 5
      });

      setShowCreate(false);
      await loadData();
    } catch (error) {
      alert(error.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="app">
      <header>
        <div>
          <h1>? FootballVerse</h1>
          <p>Football stories, history, players and moments.</p>
        </div>

        <div className="header-actions">
          <span className="status">? API ONLINE</span>
          <button onClick={() => setShowCreate(true)}>
            + Create Story
          </button>
        </div>
      </header>

      <main>
        <section className="hero">
          <div>
            <span className="tag">FOOTBALL STORYTELLING STUDIO</span>
            <h2>Turn football history into stories.</h2>
            <p>
              Create, organize and eventually transform football stories
              into narrated, cartoon-style and animated content.
            </p>
            <button onClick={() => setShowCreate(true)}>
              Create Your First Story
            </button>
          </div>
        </section>

        <section className="stats">
          <div><strong>{stories.length}</strong><span>Stories</span></div>
          <div><strong>{players.length}</strong><span>Players</span></div>
          <div><strong>{clubs.length}</strong><span>Clubs</span></div>
          <div><strong>{media.length}</strong><span>Media</span></div>
        </section>

        {showCreate && (
          <section className="creator">
            <div className="creator-header">
              <div>
                <span className="tag">STORY CREATOR</span>
                <h2>Create a Football Story</h2>
              </div>
              <button className="secondary" onClick={() => setShowCreate(false)}>
                Close
              </button>
            </div>

            <form onSubmit={createStory}>
              <label>
                Story Title
                <input
                  required
                  value={form.title}
                  onChange={e => setForm({...form, title: e.target.value})}
                  placeholder="e.g. The Rise of African Football"
                />
              </label>

              <label>
                Category
                <select
                  value={form.category}
                  onChange={e => setForm({...form, category: e.target.value})}
                >
                  <option>Football History</option>
                  <option>Player Story</option>
                  <option>Club History</option>
                  <option>Match Story</option>
                  <option>Documentary</option>
                  <option>Motivational</option>
                  <option>Humor</option>
                </select>
              </label>

              <label>
                Description
                <textarea
                  required
                  rows="6"
                  value={form.description}
                  onChange={e => setForm({...form, description: e.target.value})}
                  placeholder="Tell the story..."
                />
              </label>

              <label>
                Duration (minutes)
                <input
                  type="number"
                  min="1"
                  value={form.duration}
                  onChange={e => setForm({...form, duration: e.target.value})}
                />
              </label>

              <button type="submit" disabled={saving}>
                {saving ? "Saving..." : "Save Story"}
              </button>
            </form>
          </section>
        )}

        <section>
          <div className="section-title">
            <h2>?? Football Stories</h2>
            <button className="secondary" onClick={loadData}>Refresh</button>
          </div>

          {loading ? (
            <p className="loading">Loading FootballVerse...</p>
          ) : (
            <div className="grid">
              {stories.length ? stories.map((story, i) => (
                <article className="card" key={story.id ?? i}>
                  <span className="tag">{story.category ?? "Football"}</span>
                  <h3>{story.title ?? "Untitled Story"}</h3>
                  <p>{story.description ?? "No description available."}</p>
                  {story.duration && (
                    <small>? {story.duration} minutes</small>
                  )}
                </article>
              )) : (
                <div className="empty">
                  <h3>No stories yet</h3>
                  <p>Create your first FootballVerse story.</p>
                  <button onClick={() => setShowCreate(true)}>
                    + Create Story
                  </button>
                </div>
              )}
            </div>
          )}
        </section>

        <section>
          <h2>? Players</h2>
          <div className="grid">
            {players.length ? players.map((player, i) => (
              <article className="card" key={player.id ?? i}>
                <h3>{player.name}</h3>
                <p>{player.country} · {player.position}</p>
                <small>
                  Goals: {player.goals ?? 0} · Trophies: {player.trophies ?? 0}
                </small>
              </article>
            )) : <p>No players available yet.</p>}
          </div>
        </section>

        <section>
          <h2>??? Clubs</h2>
          <div className="grid">
            {clubs.length ? clubs.map((club, i) => (
              <article className="card" key={club.id ?? i}>
                <h3>{club.name}</h3>
                <p>{club.country}</p>
                <small>
                  Founded: {club.founded ?? "N/A"} · Trophies: {club.trophies ?? 0}
                </small>
              </article>
            )) : <p>No clubs available yet.</p>}
          </div>
        </section>
      </main>

      <footer>
        FootballVerse © 2026 · Football storytelling & animation platform
      </footer>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
