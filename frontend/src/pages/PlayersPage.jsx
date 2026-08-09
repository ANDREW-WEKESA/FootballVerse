import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

const API = "http://127.0.0.1:8000";

export default function PlayersPage() {
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  const loadPlayers = async () => {
    try {
      const response = await fetch(`${API}/players`);
      const data = await response.json();
      setPlayers(data.value || data || []);
    } catch (error) {
      console.error("Failed to load players:", error);
    }
  };

  useEffect(() => {
    loadPlayers();
  }, []);

  return (
    <div className="app">
      <Nav />

      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALL KNOWLEDGE</span>
          <h1>Players</h1>
          <p>Explore the people who made football history.</p>
        </section>

        <div className="grid">
          {players.map((player) => (
            <article
              className="card player-card"
              key={player.id}
              onClick={() => navigate(`/players/${player.id}`)}
            >
              {player.image_url && (
                <img
                  className="player-card-image"
                  src={player.image_url}
                  alt={player.full_name}
                />
              )}

              <span className="tag">PLAYER</span>

              <h2>{player.full_name}</h2>

              <p>
                {player.nationality || "Unknown"} ·{" "}
                {player.position || "Footballer"}
              </p>

              <div className="player-mini-stats">
                <span>⚽ {player.goals ?? 0} goals</span>
                <span>🏆 {player.trophies ?? 0} trophies</span>
              </div>

              <button className="secondary">
                View Football History →
              </button>
            </article>
          ))}

          {!players.length && (
            <div className="empty">
              <h2>No players yet</h2>
              <p>
                Import a football player into the FootballVerse knowledge base.
              </p>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
