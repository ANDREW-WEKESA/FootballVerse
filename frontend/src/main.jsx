import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [history, setHistory] = useState(null);
  const [timeline, setTimeline] = useState(null);
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

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

  const openPlayer = async (player) => {
    setSelectedPlayer(player);
    setHistory(null);
    setTimeline(null);
    setStory(null);
    setActiveTab("overview");
    setLoading(true);

    try {
      const [historyResponse, timelineResponse, storyResponse] =
        await Promise.all([
          fetch(`${API}/players/${player.id}/history`),
          fetch(`${API}/players/${player.id}/timeline`),
          fetch(`${API}/players/${player.id}/story`)
        ]);

      const historyData = await historyResponse.json();
      const timelineData = await timelineResponse.json();
      const storyData = await storyResponse.json();

      setHistory(historyData);
      setTimeline(timelineData);
      setStory(storyData);
    } catch (error) {
      console.error("Failed to load player data:", error);
    } finally {
      setLoading(false);
    }
  };

  const closePlayer = () => {
    setSelectedPlayer(null);
    setHistory(null);
    setTimeline(null);
    setStory(null);
  };

  if (selectedPlayer) {
    const player = history?.player || selectedPlayer;

    return (
      <div className="app">
        <nav>
          <div className="logo" onClick={closePlayer}>
            ? FootballVerse
          </div>

          <div className="nav-links">
            <button onClick={closePlayer}>Players</button>
            <button>Clubs</button>
            <button>Competitions</button>
            <button>Stories</button>
            <button>Animation Studio</button>
          </div>
        </nav>

        <main>
          <button className="secondary" onClick={closePlayer}>
            ? Back to Players
          </button>

          <section className="player-hero">
            {player.image_url && (
              <img
                className="player-image"
                src={player.image_url}
                alt={player.full_name}
              />
            )}

            <div>
              <span className="tag">FOOTBALLVERSE PLAYER</span>

              <h1>{player.full_name}</h1>

              <p>
                {player.nationality || "Unknown nationality"} ·{" "}
                {player.position || "Footballer"}
              </p>

              {player.date_of_birth && (
                <small>
                  Born: {player.date_of_birth}
                </small>
              )}
            </div>
          </section>

          <div className="tabs">
            <button
              className={activeTab === "overview" ? "tab active" : "tab"}
              onClick={() => setActiveTab("overview")}
            >
              Overview
            </button>

            <button
              className={activeTab === "career" ? "tab active" : "tab"}
              onClick={() => setActiveTab("career")}
            >
              Career
            </button>

            <button
              className={activeTab === "timeline" ? "tab active" : "tab"}
              onClick={() => setActiveTab("timeline")}
            >
              Timeline
            </button>

            <button
              className={activeTab === "story" ? "tab active" : "tab"}
              onClick={() => setActiveTab("story")}
            >
              Story
            </button>
          </div>

          {loading && (
            <section className="loading">
              Loading FootballVerse history...
            </section>
          )}

          {!loading && activeTab === "overview" && (
            <>
              <section className="stats">
                <div>
                  <strong>{player.goals ?? 0}</strong>
                  <span>Goals</span>
                </div>

                <div>
                  <strong>{player.assists ?? 0}</strong>
                  <span>Assists</span>
                </div>

                <div>
                  <strong>{player.trophies ?? 0}</strong>
                  <span>Trophies</span>
                </div>

                <div>
                  <strong>{player.appearances ?? 0}</strong>
                  <span>Appearances</span>
                </div>
              </section>

              <section className="profile-section">
                <h2>?? About the Player</h2>

                <p>
                  {player.biography ||
                    `FootballVerse records the football journey of ${player.full_name}.`}
                </p>
              </section>

              <section className="feature-grid">
                <div>
                  <h3>? Career</h3>
                  <p>
                    {history?.season_stats?.length ?? 0} recorded season
                    statistics.
                  </p>
                </div>

                <div>
                  <h3>?? Honours</h3>
                  <p>
                    {history?.honours?.length ?? 0} recorded honours and
                    achievements.
                  </p>
                </div>

                <div>
                  <h3>?? Timeline</h3>
                  <p>
                    {timeline?.career_timeline?.length ?? 0} career seasons
                    recorded.
                  </p>
                </div>

                <div>
                  <h3>?? Animated Story</h3>
                  <p>
                    FootballVerse can transform this football history into
                    storytelling episodes.
                  </p>
                </div>
              </section>
            </>
          )}

          {!loading && activeTab === "career" && (
            <section className="content-section">
              <h2>? Career History</h2>

              {!history?.season_stats?.length && (
                <p>No season statistics available.</p>
              )}

              <div className="timeline-list">
                {history?.season_stats?.map((stat) => (
                  <article className="timeline-card" key={stat.id}>
                    <span className="year">{stat.season}</span>

                    <div>
                      <h3>{stat.team}</h3>

                      <p>{stat.league}</p>

                      <strong>
                        {stat.statistic}: {stat.value}
                      </strong>
                    </div>

                    {stat.team_badge_url && (
                      <img
                        className="badge"
                        src={stat.team_badge_url}
                        alt={stat.team}
                      />
                    )}
                  </article>
                ))}
              </div>
            </section>
          )}

          {!loading && activeTab === "timeline" && (
            <section className="content-section">
              <h2>?? Career Timeline</h2>

              <div className="timeline-list">
                {timeline?.career_timeline?.map((event, index) => (
                  <article className="timeline-card" key={index}>
                    <span className="year">{event.season}</span>

                    <div>
                      <h3>
                        {event.teams?.join(", ") || "Football"}
                      </h3>

                      <p>
                        {event.leagues?.join(" · ")}
                      </p>

                      <div className="mini-stats">
                        <span>Appearances: {event.appearances}</span>
                        <span>Goals: {event.goals}</span>
                        <span>Minutes: {event.minutes}</span>
                      </div>
                    </div>
                  </article>
                ))}
              </div>

              <h2 className="section-title">?? Honours Timeline</h2>

              <div className="timeline-list">
                {timeline?.honours_timeline?.map((honour, index) => (
                  <article className="honour-card" key={index}>
                    {honour.trophy_url && (
                      <img
                        src={honour.trophy_url}
                        alt={honour.honour}
                      />
                    )}

                    <div>
                      <span className="year">{honour.season}</span>
                      <h3>{honour.honour}</h3>
                      <p>{honour.team}</p>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          )}

          {!loading && activeTab === "story" && (
            <section className="story-section">
              <span className="tag">FOOTBALLVERSE STORY</span>

              <h1>{story?.title || `The Story of ${player.full_name}`}</h1>

              <p className="story-intro">
                {story?.intro ||
                  `Follow the football journey of ${player.full_name}.`}
              </p>

              <div className="story-events">
                {story?.events?.map((event, index) => (
                  <article className="story-event" key={index}>
                    <span className="year">{event.year}</span>

                    <div>
                      <span className="event-type">
                        {event.type}
                      </span>

                      <h3>{event.title}</h3>

                      <p>{event.description}</p>
                    </div>
                  </article>
                ))}
              </div>

              <div className="story-footer">
                {story?.event_count ?? 0} historical events available
                for storytelling.
              </div>
            </section>
          )}
        </main>

        <footer>
          ? FootballVerse · Football knowledge brought to life
        </footer>
      </div>
    );
  }

  return (
    <div className="app">
      <nav>
        <div className="logo">
          ? FootballVerse
        </div>

        <div className="nav-links">
          <button>Home</button>
          <button className="active">Players</button>
          <button>Clubs</button>
          <button>Competitions</button>
          <button>Stories</button>
          <button>Animation Studio</button>
        </div>
      </nav>

      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALL KNOWLEDGE</span>

          <h1>Players</h1>

          <p>
            Explore the people who made football history.
          </p>
        </section>

        <div className="grid">
          {players.map((player) => (
            <article
              className="card player-card"
              key={player.id}
              onClick={() => openPlayer(player)}
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
                <span>? {player.goals ?? 0} goals</span>
                <span>?? {player.trophies ?? 0} trophies</span>
              </div>

              <button className="secondary">
                View Football History ?
              </button>
            </article>
          ))}

          {!players.length && (
            <div className="empty">
              <h2>No players yet</h2>
              <p>
                Import a football player into the FootballVerse
                knowledge base.
              </p>
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
