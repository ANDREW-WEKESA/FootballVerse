import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

const API = "http://127.0.0.1:8000";

export default function PlayerDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [history, setHistory] = useState(null);
  const [timeline, setTimeline] = useState(null);
  const [story, setStory] = useState(null);
  const [goals, setGoals] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    const loadPlayer = async () => {
      setLoading(true);
      try {
        // Load basic player info first
        const playersResponse = await fetch(`${API}/players`);
        const playersData = await playersResponse.json();
        const players = playersData.value || playersData || [];
        const player = players.find((p) => String(p.id) === String(id));
        if (player) setSelectedPlayer(player);

        // Load all detail data in parallel
        const [historyResponse, timelineResponse, storyResponse, goalsResponse] =
          await Promise.all([
            fetch(`${API}/players/${id}/history`),
            fetch(`${API}/players/${id}/timeline`),
            fetch(`${API}/players/${id}/story`),
            fetch(`${API}/players/${id}/goals`),
          ]);

        const historyData = await historyResponse.json();
        const timelineData = await timelineResponse.json();
        const storyData = await storyResponse.json();
        const goalsData = await goalsResponse.json();

        setHistory(historyData);
        setTimeline(timelineData);
        setStory(storyData);
        setGoals(goalsData);
      } catch (error) {
        console.error("Failed to load player data:", error);
      } finally {
        setLoading(false);
      }
    };

    loadPlayer();
  }, [id]);

  const player = history?.player || selectedPlayer;

  return (
    <div className="app">
      <Nav />

      <main>
        <button className="secondary" onClick={() => navigate("/")}>
          ← Back to Players
        </button>

        {player && (
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
                <small>Born: {player.date_of_birth}</small>
              )}
            </div>
          </section>
        )}

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
          <button
            className={activeTab === "goals" ? "tab active" : "tab"}
            onClick={() => setActiveTab("goals")}
          >
            Goals
          </button>
        </div>

        {loading && (
          <section className="loading">
            Loading FootballVerse history...
          </section>
        )}

        {!loading && activeTab === "overview" && player && (
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
              <h2>👤 About the Player</h2>
              <p>
                {player.biography ||
                  `FootballVerse records the football journey of ${player.full_name}.`}
              </p>
            </section>

            <section className="feature-grid">
              <div>
                <h3>📊 Career</h3>
                <p>{history?.season_stats?.length ?? 0} recorded season statistics.</p>
              </div>
              <div>
                <h3>🏆 Honours</h3>
                <p>{history?.honours?.length ?? 0} recorded honours and achievements.</p>
              </div>
              <div>
                <h3>📅 Timeline</h3>
                <p>{timeline?.career_timeline?.length ?? 0} career seasons recorded.</p>
              </div>
              <div>
                <h3>🎬 Animated Story</h3>
                <p>
                  FootballVerse can transform this football history into storytelling episodes.
                </p>
              </div>
            </section>
          </>
        )}

        {!loading && activeTab === "career" && (
          <section className="content-section">
            <h2>📊 Career History</h2>

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
            <h2>📅 Career Timeline</h2>

            <div className="timeline-list">
              {timeline?.career_timeline?.map((event, index) => (
                <article className="timeline-card" key={index}>
                  <span className="year">{event.season}</span>
                  <div>
                    <h3>{event.teams?.join(", ") || "Football"}</h3>
                    <p>{event.leagues?.join(" · ")}</p>
                    <div className="mini-stats">
                      <span>Appearances: {event.appearances}</span>
                      <span>Goals: {event.goals}</span>
                      <span>Minutes: {event.minutes}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>

            <h2 className="section-title">🏆 Honours Timeline</h2>

            <div className="timeline-list">
              {timeline?.honours_timeline?.map((honour, index) => (
                <article className="honour-card" key={index}>
                  {honour.trophy_url && (
                    <img src={honour.trophy_url} alt={honour.honour} />
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
            <h1>{story?.title || `The Story of ${player?.full_name}`}</h1>
            <p className="story-intro">
              {story?.intro ||
                `Follow the football journey of ${player?.full_name}.`}
            </p>

            <div className="story-events">
              {story?.events?.map((event, index) => (
                <article className="story-event" key={index}>
                  <span className="year">{event.year}</span>
                  <div>
                    <span className="event-type">{event.type}</span>
                    <h3>{event.title}</h3>
                    <p>{event.description}</p>
                  </div>
                </article>
              ))}
            </div>

            <div className="story-footer">
              {story?.event_count ?? 0} historical events available for storytelling.
            </div>
          </section>
        )}

        {!loading && activeTab === "goals" && (
          <section className="content-section">
            <h2>⚽ Goals</h2>

            {(!goals || !goals.length) ? (
              <div className="empty" style={{ border: "1px dashed #31533a", borderRadius: "14px", padding: "40px", textAlign: "center" }}>
                <p style={{ color: "#aebbb1" }}>No goals recorded yet.</p>
              </div>
            ) : (
              <div className="timeline-list">
                {goals.map((goal, index) => (
                  <article className="timeline-card" key={goal.id ?? index}>
                    <span className="year">#{goal.goal_number}</span>
                    <div>
                      <h3>
                        {goal.team} vs {goal.opponent}
                      </h3>
                      <p>
                        {goal.competition} · {goal.date}
                      </p>
                      <div className="mini-stats">
                        <span>Minute: {goal.minute ?? "—"}</span>
                        <span>Score: {goal.score ?? "—"}</span>
                        <span>Type: {goal.goal_type ?? "—"}</span>
                      </div>
                      {goal.description && (
                        <p style={{ marginTop: "8px", color: "#aebbb1" }}>
                          {goal.description}
                        </p>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        )}
      </main>

      <Footer />
    </div>
  );
}
