import React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

import PlayersPage from "./pages/PlayersPage";
import PlayerDetailPage from "./pages/PlayerDetailPage";
import StoriesPage from "./pages/StoriesPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import StoryStudioPage from "./pages/StoryStudioPage";
import ProductionPage from "./pages/ProductionPage";
import ProductionStudioPage from "./pages/ProductionStudioPage";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<PlayersPage />} />
        <Route path="/players/:id" element={<PlayerDetailPage />} />
        <Route path="/stories" element={<StoriesPage />} />
        <Route path="/login" element={<LoginPage />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/production"
          element={
            <ProtectedRoute>
              <ProductionPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/production/studio"
          element={
            <ProtectedRoute>
              <ProductionStudioPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/studio/:id"
          element={
            <ProtectedRoute>
              <StoryStudioPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/studio/new"
          element={
            <ProtectedRoute>
              <StoryStudioPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthProvider>
  );
}
