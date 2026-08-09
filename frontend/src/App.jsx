import React from "react";
import { Routes, Route } from "react-router-dom";
import PlayersPage from "./pages/PlayersPage";
import PlayerDetailPage from "./pages/PlayerDetailPage";
import StoriesPage from "./pages/StoriesPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<PlayersPage />} />
      <Route path="/players/:id" element={<PlayerDetailPage />} />
      <Route path="/stories" element={<StoriesPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
    </Routes>
  );
}
