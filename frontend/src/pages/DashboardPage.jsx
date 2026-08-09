import React from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

export default function DashboardPage() {
  return (
    <div className="app">
      <Nav />

      <main>
        <section className="page-heading">
          <span className="tag">FOOTBALLVERSE</span>
          <h1>Dashboard</h1>
          <p>Your FootballVerse command centre.</p>
        </section>

        <div
          style={{
            padding: "80px 40px",
            borderRadius: "20px",
            background: "#0c1b11",
            border: "1px dashed #31533a",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "4rem", marginBottom: "20px" }}>📊</div>
          <h2 style={{ fontSize: "2rem", marginBottom: "12px" }}>Coming Soon</h2>
          <p style={{ color: "#9eada2", fontSize: "1.1rem", maxWidth: "500px", margin: "0 auto" }}>
            The Dashboard will give you a full overview of your FootballVerse
            knowledge base — players, stats, stories, and more.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
