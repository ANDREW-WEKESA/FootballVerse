import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [active, setActive] = useState("Home");
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    name: "",
    country: "",
    position: "",
    biography: "",
    goals: 0,
    trophies: 0
  });

  const loadPlayers = async () => {
    try {
      const response = await fetch(`${API}/players`);
      setPlayers(await response.json());
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadPlayers();
  }, []);

  const createPlayer = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API}/players`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          ...form,
          goals: Number(form.goals),
          trophies: Number(form.trophies)
        })
      });

      if (!response.ok) throw new Error("Could not create player");

      setForm({
        name: "",
        country: "",
        position: "",
        biography: "",
        goals: 0,
        trophies: 0
      });

      setShowCreate(false);
      loadPlayers();
    } catch (e) {
      alert(e.message);
    }
  };

  if (selectedPlayer) {
    return (
      <div className="app">
        <nav>
          <div className="logo" onClick={() => setSelectedPlayer(null)}>
            ? FootballVerse
          </div>
        </nav>

        <main>
          <button className="secondary" onClick={() => setSelectedPlayer(null)}>
            ? Back to Players
          </button>

          <section className="player-hero">
            <span className="tag">FOOTBALLVERSE PLAYER</span>
            <h1>{selectedPlayer.name}</h1>
            <p>
              {selectedPlayer.country} · {selectedPlayer.position}
            </p>
          </section>

          <section className="stats">
            <div>
              <strong>{selectedPlayer.goals ?? 0}</strong>
              <span>Goals</span>
            </div>

            <div>
              <strong>{selectedPlayer.trophies ?? 0}</strong>
              <span>Trophies</span>
            </div>

            <div>
              <strong>{selectedPlayer.country || "—"}</strong>
              <span>Country</span>
            </div>

            <div>
              <strong>{selectedPlayer.position || "—"}</strong>
              <span>Position</span>
            </div>
          </section>

          <section className="profile-section">
            <h2>?? About the Player</h2>
            <p>
              {selectedPlayer.biography ||
                "FootballVerse biography coming soon."}
            </p>
          </section>

          <section className="feature-grid">
            <div>
              <h3>? Career</h3>
              <p>
                Clubs, seasons, international career and major career events.
              </p>
            </div>

            <div>
              <h3>?? Achievements</h3>
              <p>
                Trophies, awards, records and historic accomplishments.
              </p>
            </div>

            <div>
              <h3>?? Timeline</h3>
              <p>
                Follow the most important moments throughout the player's life.
              </p>
            </div>

            <div>
              <h3>?? Animated Stories</h3>
              <p>
                Turn this player's football journey into animated episodes.
              </p>
            </div>
          </section>
        </main>

        <footer>? FootballVerse · Football knowledge brought to life</footer>
      </div>
    );
  }

  return (
    <div className="app">
      <nav>
        <div className="logo" onClick={() => setActive("Home")}>
          ? FootballVerse
        </div>

        <div className="nav-links">
          <button onClick={() => setActive("Home")}>Home</button>
          <button className="active">Players</button>
          <button onClick={() => setActive("Clubs")}>Clubs</button>
          <button onClick={() => setActive("Competitions")}>Competitions</button>
          <button onClick={() => setActive("Stories")}>Stories</button>
          <button onClick={() => setActive("Animation Studio")}>
            Animation Studio
          </button>
        </div>
      </nav>

      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALL KNOWLEDGE</span>
          <h1>Players</h1>
          <p>
            Explore the people who made football history.
          </p>

          <button
            className="primary"
            onClick={() => setShowCreate(!showCreate)}
          >
            + Add Player
          </button>
        </section>

        {showCreate && (
          <section className="creator">
            <h2>Create Player Profile</h2>

            <form onSubmit={createPlayer}>
              <label>
                Player Name
                <input
                  required
                  value={form.name}
                  onChange={e => setForm({...form, name: e.target.value})}
                  placeholder="Player name"
                />
              </label>

              <label>
                Country
                <input
                  value={form.country}
                  onChange={e => setForm({...form, country: e.target.value})}
                  placeholder="Country"
                />
              </label>

              <label>
                Position
                <input
                  value={form.position}
                  onChange={e => setForm({...form, position: e.target.value})}
                  placeholder="Forward, Midfielder, Defender..."
                />
              </label>

              <label>
                Biography
                <textarea
                  rows="5"
                  value={form.biography}
                  onChange={e => setForm({...form, biography: e.target.value})}
                  placeholder="Player biography..."
                />
              </label>

              <label>
                Goals
                <input
                  type="number"
                  min="0"
                  value={form.goals}
                  onChange={e => setForm({...form, goals: e.target.value})}
                />
              </label>

              <label>
                Trophies
                <input
                  type="number"
                  min="0"
                  value={form.trophies}
                  onChange={e => setForm({...form, trophies: e.target.value})}
                />
              </label>

              <button className="primary" type="submit">
                Save Player
              </button>
            </form>
          </section>
        )}

        <div className="grid">
          {players.map((player, index) => (
            <article
              className="card player-card"
              key={player.id ?? index}
              onClick={() => setSelectedPlayer(player)}
            >
              <span className="tag">PLAYER</span>
              <h2>{player.name}</h2>
              <p>{player.country} · {player.position}</p>

              <div className="player-mini-stats">
                <span>? {player.goals ?? 0} goals</span>
                <span>?? {player.trophies ?? 0} trophies</span>
              </div>

              <button className="secondary">
                View Profile ?
              </button>
            </article>
          ))}

          {!players.length && (
            <div className="empty">
              <h2>No players yet</h2>
              <p>Add the first player to the FootballVerse knowledge base.</p>
            </div>
          )}
        </div>
      </main>

      <footer>
        ? FootballVerse · Football knowledge brought to life
      </footer>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
