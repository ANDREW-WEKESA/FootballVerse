import React from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

export default function StoriesPage() {
  return (
    <div className="app">
      <Nav />

      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALLVERSE STORIES</span>
          <h1>Stories</h1>
          <p>Football journeys transformed into compelling narratives.</p>
        </section>

        <div
          style={{
            padding: "80px 40px",
            borderRadius: "20px",
            background: "linear-gradient(135deg, #102b17, #09170d)",
            border: "1px solid #2b5a36",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "4rem", marginBottom: "20px" }}>🎬</div>
          <h2 style={{ fontSize: "2rem", marginBottom: "12px" }}>Coming Soon</h2>
          <p style={{ color: "#9eada2", fontSize: "1.1rem", maxWidth: "500px", margin: "0 auto" }}>
            FootballVerse Stories will bring player journeys to life through
            animated, episodic storytelling. Stay tuned.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
