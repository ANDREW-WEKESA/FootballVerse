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

  useEffect(() => {
    Promise.all([
      fetch(`${API}/stories`).then(r => r.json()),
      fetch(`${API}/players`).then(r => r.json()),
      fetch(`${API}/clubs`).then(r => r.json()),
      fetch(`${API}/media`).then(r => r.json())
    ])
      .then(([s, p, c, m]) => {
        setStories(s);
        setPlayers(p);
        setClubs(c);
        setMedia(m);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="app">
      <header>
        <div>
          <h1>? FootballVerse</h1>
          <p>Football stories, history, players and moments.</p>
        </div>
        <span className="status">? API ONLINE</span>
      </header>

      <main>
        <section className="hero">
          <h2>Welcome to FootballVerse</h2>
          <p>
            Discover football history and turn legendary moments into
            engaging stories, cartoons and animated content.
          </p>
        </section>

        <section className="stats">
          <div><strong>{stories.length}</strong><span>Stories</span></div>
          <div><strong>{players.length}</strong><span>Players</span></div>
          <div><strong>{clubs.length}</strong><span>Clubs</span></div>
          <div><strong>{media.length}</strong><span>Media</span></div>
        </section>

        {loading ? (
          <p className="loading">Loading FootballVerse...</p>
        ) : (
          <>
            <section>
              <h2>?? Football Stories</h2>
              <div className="grid">
                {stories.length ? stories.map((story, i) => (
                  <article className="card" key={story.id ?? i}>
                    <span className="tag">{story.category ?? "Football"}</span>
                    <h3>{story.title ?? "Untitled Story"}</h3>
                    <p>{story.description ?? "No description available."}</p>
                    {story.duration && <small>{story.duration} minutes</small>}
                  </article>
                )) : <p>No stories available yet.</p>}
              </div>
            </section>

            <section>
              <h2>? Players</h2>
              <div className="grid">
                {players.length ? players.map((player, i) => (
                  <article className="card" key={player.id ?? i}>
                    <h3>{player.name}</h3>
                    <p>{player.country} · {player.position}</p>
                    <small>Goals: {player.goals ?? 0} · Trophies: {player.trophies ?? 0}</small>
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
                    <small>Founded: {club.founded ?? "N/A"} · Trophies: {club.trophies ?? 0}</small>
                  </article>
                )) : <p>No clubs available yet.</p>}
              </div>
            </section>
          </>
        )}
      </main>

      <footer>
        FootballVerse © 2026 · Football storytelling & animation platform
      </footer>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
