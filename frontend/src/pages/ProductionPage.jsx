import React from "react";
import { Link } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

const cards = [
  ["??", "Production Studio", "Build stories from script to animation-ready scenes.", "/production"],
  ["?", "Football Archive", "Explore players, clubs and verified football evidence.", "/players"],
  ["??", "Story Library", "Manage your documentary and entertainment stories.", "/stories"],
];

export default function ProductionPage() {
  return (
    <div className="app">
      <Nav />
      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALLVERSE</span>
          <h1>Production Center</h1>
          <p>Your command center for turning football knowledge into content.</p>
        </section>

        <div className="production-cards">
          {cards.map(([icon, title, description, path]) => (
            <Link className="production-card" to={path} key={title}>
              <span>{icon}</span>
              <h2>{title}</h2>
              <p>{description}</p>
              <strong>Open ?</strong>
            </Link>
          ))}
        </div>

        <section className="vision-panel">
          <span className="tag">THE PIPELINE</span>
          <h2>Research ? Story ? Animation ? Audience</h2>
          <p>
            FootballVerse is being built as a complete storytelling pipeline,
            not just a football database.
          </p>
          <div className="vision-flow">
            <span>Research</span><b>?</b>
            <span>Script</span><b>?</b>
            <span>Scenes</span><b>?</b>
            <span>Cartoon</span><b>?</b>
            <span>Voice</span><b>?</b>
            <span>Video</span>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}

