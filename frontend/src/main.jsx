import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [active, setActive] = useState("Home");
  const [data, setData] = useState({
    players: [],
    clubs: [],
    competitions: [],
    achievements: [],
    stories: []
  });

  const load = async () => {
    try {
      const endpoints = ["players", "clubs", "competitions", "achievements", "stories"];
      const results = await Promise.all(
        endpoints.map(x => fetch(`${API}/${x}`).then(r => r.json()))
      );

      setData({
        players: results[0],
        clubs: results[1],
        competitions: results[2],
        achievements: results[3],
        stories: results[4]
      });
    } catch (e) {
      console.error("FootballVerse API:", e);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const sections = {
    Players: data.players,
    Clubs: data.clubs,
    Competitions: data.competitions,
    Achievements: data.achievements,
    Stories: data.stories
  };

  return (
    <div className="app">

      <nav>
        <div className="logo" onClick={() => setActive("Home")}>
          ? FootballVerse
        </div>

        <div className="nav-links">
          {["Home", "Players", "Clubs", "Competitions", "Achievements", "Stories", "Animation Studio"]
            .map(item => (
              <button
                key={item}
                className={active === item ? "active" : ""}
                onClick={() => setActive(item)}
              >
                {item}
              </button>
            ))}
        </div>
      </nav>

      <main>

        {active === "Home" && (
          <>
            <section className="hero">
              <span className="tag">THE FOOTBALL KNOWLEDGE UNIVERSE</span>
              <h1>Football has a story.</h1>
              <h1>We bring it to life.</h1>

              <p>
                FootballVerse is a football knowledge and entertainment
                platform where players, clubs, competitions, achievements
                and historic moments become engaging stories and,
                eventually, animated experiences.
              </p>

              <button className="primary" onClick={() => setActive("Players")}>
                Explore Football ?
              </button>
            </section>

            <section className="stats">
              <div><strong>{data.players.length}</strong><span>Players</span></div>
              <div><strong>{data.clubs.length}</strong><span>Clubs</span></div>
              <div><strong>{data.competitions.length}</strong><span>Competitions</span></div>
              <div><strong>{data.stories.length}</strong><span>Stories</span></div>
            </section>

            <section className="vision">
              <h2>?? More than statistics.</h2>
              <p>
                Learn football history through stories, timelines,
                achievements, memorable moments, humor and animation.
              </p>

              <div className="feature-grid">
                <div>
                  <h3>?? Knowledge</h3>
                  <p>Discover the people, clubs and events that shaped football.</p>
                </div>

                <div>
                  <h3>?? Stories</h3>
                  <p>Turn important football moments into compelling stories.</p>
                </div>

                <div>
                  <h3>?? Animation</h3>
                  <p>Experience football stories through stylized animated content.</p>
                </div>

                <div>
                  <h3>??????????? Every Generation</h3>
                  <p>Content designed to be enjoyable for children, teenagers and adults.</p>
                </div>
              </div>
            </section>
          </>
        )}

        {active !== "Home" && active !== "Animation Studio" && (
          <section>
            <div className="page-heading">
              <span className="tag">{active.toUpperCase()}</span>
              <h1>{active}</h1>
              <p>Explore the FootballVerse knowledge universe.</p>
            </div>

            <div className="grid">
              {(sections[active] || []).map((item, index) => (
                <article className="card" key={item.id ?? index}>
                  <span className="tag">{active}</span>
                  <h3>
                    {item.name || item.title || item.player || "Football Item"}
                  </h3>

                  <p>
                    {item.description ||
                     item.country ||
                     item.position ||
                     "Football knowledge coming soon."}
                  </p>

                  {item.goals !== undefined && (
                    <small>? Goals: {item.goals}</small>
                  )}

                  {item.trophies !== undefined && (
                    <small> ?? Trophies: {item.trophies}</small>
                  )}
                </article>
              ))}

              {(!sections[active] || sections[active].length === 0) && (
                <div className="empty">
                  <h2>Nothing here yet.</h2>
                  <p>
                    This section is ready for FootballVerse data.
                    We will build it step by step.
                  </p>
                </div>
              )}
            </div>
          </section>
        )}

        {active === "Animation Studio" && (
          <section className="studio">
            <span className="tag">COMING NEXT</span>
            <h1>?? Animation Studio</h1>

            <p>
              This will become the creative engine of FootballVerse.
            </p>

            <div className="feature-grid">
              <div>
                <h3>?? Cartoon Characters</h3>
                <p>Stylized characters for football storytelling.</p>
              </div>

              <div>
                <h3>??? Narration</h3>
                <p>Turn written stories into narrated experiences.</p>
              </div>

              <div>
                <h3>??? Scenes</h3>
                <p>Build stories scene by scene.</p>
              </div>

              <div>
                <h3>?? Humor</h3>
                <p>Make football history entertaining for every generation.</p>
              </div>
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

createRoot(document.getElementById("root")).render(<App />);
