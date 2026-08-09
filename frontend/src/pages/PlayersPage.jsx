import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

const API = "http://127.0.0.1:8000";

function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}

export default function PlayersPage() {
  const [players, setPlayers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const debouncedSearch = useDebounce(search, 300);

  const loadPlayers = useCallback(async (query) => {
    setLoading(true);
    try {
      const url = query && query.length >= 2
        ? `${API}/players?search=${encodeURIComponent(query)}`
        : `${API}/players`;
      const res = await fetch(url);
      const data = await res.json();
      setPlayers(data.value || data || []);
    } catch {
      setPlayers([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadPlayers(debouncedSearch); }, [debouncedSearch, loadPlayers]);

  return (
    <div className="app">
      <Nav />
      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALL KNOWLEDGE</span>
          <h1>Players</h1>
          <p>Explore the people who made football history.</p>
        </section>

        <div style={{ marginBottom: "28px" }}>
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search players by name..."
            style={{ width: "100%", maxWidth: "420px", padding: "12px 16px", borderRadius: "10px", background: "#0c1b11", border: "1px solid #31533a", color: "#f3f7f4", fontSize: "1rem", outline: "none" }}
          />
        </div>

        {loading && <div className="loading">Loading players...</div>}

        {!loading && (
          <div className="grid">
            {players.map((player) => (
              <article className="card player-card" key={player.id} onClick={() => navigate(`/players/${player.id}`)}>
                {player.image_url && (
                  <img className="player-card-image" src={player.image_url} alt={player.full_name} />
                )}
                <span className="tag">PLAYER</span>
                <h2>{player.full_name}</h2>
                <p>{player.nationality || "Unknown"} · {player.position || "Footballer"}</p>
                <div className="player-mini-stats">
                  <span>⚽ {player.goals ?? 0} goals</span>
                  <span>🏆 {player.trophies ?? 0} trophies</span>
                </div>
                <button className="secondary">View Football History →</button>
              </article>
            ))}

            {players.length === 0 && (
              <div className="empty">
                <h2>{search ? `No players found for "${search}"` : "No players yet"}</h2>
                <p>{search ? "Try a different search term." : "Import a football player into the FootballVerse knowledge base."}</p>
              </div>
            )}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
