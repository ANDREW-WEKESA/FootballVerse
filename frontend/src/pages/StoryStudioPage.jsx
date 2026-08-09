import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import { useAuth } from "../context/AuthContext";

const API = "http://127.0.0.1:8000";

export default function StoryStudioPage() {
  const { id } = useParams();
  const isEditing = !!id && id !== "new";
  const { token } = useAuth();
  const navigate = useNavigate();

  const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };

  const [players, setPlayers] = useState([]);
  const [clubs, setClubs] = useState([]);
  const [form, setForm] = useState({ title: "", player_id: "", club_id: "", script: "", narration_file: "", media_metadata: "{}", source_rights_metadata: "{}" });
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);
  const [rendering, setRendering] = useState(false);
  const [success, setSuccess] = useState("");
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(isEditing);

  useEffect(() => {
    fetch(`${API}/players`).then(r => r.json()).then(d => setPlayers(d.value || d || []));
    fetch(`${API}/clubs`).then(r => r.json()).then(d => setClubs(d || []));
    if (isEditing) {
      fetch(`${API}/stories/${id}`, { headers })
        .then(r => r.json())
        .then(d => {
          setStory(d);
          setForm({
            title: d.title || "",
            player_id: d.player_id || "",
            club_id: d.club_id || "",
            script: d.script || "",
            narration_file: d.narration_file || "",
            media_metadata: JSON.stringify(d.media_metadata || {}, null, 2),
            source_rights_metadata: JSON.stringify(d.source_rights_metadata || {}, null, 2),
          });
          setLoading(false);
        });
    }
  }, [id]);

  const set = (field) => (e) => setForm(f => ({ ...f, [field]: e.target.value }));

  const validate = () => {
    const e = {};
    if (!form.title.trim()) e.title = "Title is required";
    if (!form.player_id && !form.club_id) e.subject = "Select a player or club";
    try { JSON.parse(form.media_metadata); } catch { e.media_metadata = "Must be valid JSON"; }
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    setSuccess("");
    try {
      const body = {
        title: form.title,
        player_id: form.player_id ? parseInt(form.player_id) : null,
        club_id: form.club_id ? parseInt(form.club_id) : null,
        script: form.script,
        narration_file: form.narration_file,
        media_metadata: JSON.parse(form.media_metadata || "{}"),
        source_rights_metadata: JSON.parse(form.source_rights_metadata || "{}"),
      };
      const res = await fetch(
        isEditing ? `${API}/stories/${id}` : `${API}/stories`,
        { method: isEditing ? "PUT" : "POST", headers, body: JSON.stringify(body) }
      );
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Save failed");
      setStory(data);
      setSuccess(isEditing ? "Story saved." : "Story created.");
      if (!isEditing) navigate(`/studio/${data.id}`);
    } catch (err) {
      setErrors({ api: err.message });
    } finally {
      setSaving(false);
    }
  };

  const handleRender = async () => {
    setRendering(true);
    setSuccess("");
    try {
      const res = await fetch(`${API}/stories/${id}/render`, { method: "POST", headers });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Render failed");
      setStory(s => ({ ...s, status: "rendered" }));
      setSuccess("Render triggered successfully.");
    } catch (err) {
      setErrors({ render: err.message });
    } finally {
      setRendering(false);
    }
  };

  const inputStyle = { width: "100%", padding: "11px 14px", borderRadius: "9px", background: "#102116", border: "1px solid #31533a", color: "#f3f7f4", fontSize: "0.95rem", outline: "none", boxSizing: "border-box" };
  const labelStyle = { display: "block", marginBottom: "8px", color: "#c6d4ca", fontSize: "0.9rem" };
  const fieldStyle = { marginBottom: "22px" };
  const errStyle = { color: "#f87171", fontSize: "0.82rem", marginTop: "5px" };

  if (loading) return (
    <div className="app"><Nav /><main><div className="loading">Loading story...</div></main><Footer /></div>
  );

  return (
    <div className="app">
      <Nav />
      <main>
        <section className="page-heading">
          <span className="tag">STORY STUDIO</span>
          <h1>{isEditing ? "Edit Story" : "New Story"}</h1>
          <p>Write, attach media, and produce football narratives.</p>
        </section>

        {/* Parody disclaimer */}
        <div style={{ padding: "14px 18px", borderRadius: "10px", background: "#1a1a0e", border: "1px solid #5a5a00", color: "#d4d472", fontSize: "0.88rem", marginBottom: "30px" }}>
          ⚠️ <strong>Disclaimer:</strong> Story Studio content is fictional, comedic, and parody in nature. It does not represent real events or real individuals. Add appropriate disclaimers before publishing.
        </div>

        {/* Status bar for existing stories */}
        {story && (
          <div style={{ display: "flex", alignItems: "center", gap: "16px", padding: "16px 20px", borderRadius: "12px", background: "#0c1b11", border: "1px solid #23452c", marginBottom: "28px", flexWrap: "wrap" }}>
            <span style={{ color: "#9eada2", fontSize: "0.9rem" }}>Status:</span>
            <span style={{ padding: "4px 12px", borderRadius: "20px", background: "#183e22", color: "#72e582", fontWeight: "800", fontSize: "0.8rem" }}>{story.status?.toUpperCase()}</span>
            {story.status === "draft" && (
              <button onClick={handleRender} disabled={rendering} style={{ marginLeft: "auto", padding: "10px 18px", borderRadius: "8px", background: rendering ? "#1e4a28" : "#166534", border: "1px solid #22c55e", color: "#22c55e", cursor: rendering ? "not-allowed" : "pointer", fontWeight: "700" }}>
                {rendering ? "Rendering..." : "▶ Trigger Render"}
              </button>
            )}
            {story.status === "rendered" && (
              <a href={`${API}/stories/${id}/download`} style={{ marginLeft: "auto", padding: "10px 18px", borderRadius: "8px", background: "#1e3a5a", border: "1px solid #3b82f6", color: "#93c5fd", fontWeight: "700", textDecoration: "none" }}>
                ⬇ Download Video
              </a>
            )}
            {errors.render && <span style={errStyle}>{errors.render}</span>}
          </div>
        )}

        {success && (
          <div style={{ padding: "12px 16px", borderRadius: "9px", background: "#0f2d16", border: "1px solid #22c55e", color: "#22c55e", marginBottom: "20px", fontSize: "0.9rem" }}>
            ✓ {success}
          </div>
        )}

        {errors.api && (
          <div style={{ padding: "12px 16px", borderRadius: "9px", background: "#2a0e0e", border: "1px solid #7a2020", color: "#f87171", marginBottom: "20px", fontSize: "0.9rem" }}>
            {errors.api}
          </div>
        )}

        <form onSubmit={handleSave} style={{ maxWidth: "760px" }}>
          <div style={fieldStyle}>
            <label style={labelStyle}>Title *</label>
            <input style={{ ...inputStyle, borderColor: errors.title ? "#7a2020" : "#31533a" }} value={form.title} onChange={set("title")} placeholder="e.g. The Rise of a Legend" />
            {errors.title && <p style={errStyle}>{errors.title}</p>}
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "22px" }}>
            <div>
              <label style={labelStyle}>Player</label>
              <select style={{ ...inputStyle, borderColor: errors.subject ? "#7a2020" : "#31533a" }} value={form.player_id} onChange={set("player_id")}>
                <option value="">— Select player —</option>
                {players.map(p => <option key={p.id} value={p.id}>{p.full_name}</option>)}
              </select>
            </div>
            <div>
              <label style={labelStyle}>Club</label>
              <select style={{ ...inputStyle, borderColor: errors.subject ? "#7a2020" : "#31533a" }} value={form.club_id} onChange={set("club_id")}>
                <option value="">— Select club —</option>
                {clubs.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          {errors.subject && <p style={{ ...errStyle, marginTop: "-14px", marginBottom: "16px" }}>{errors.subject}</p>}

          <div style={fieldStyle}>
            <label style={labelStyle}>Script / Narration</label>
            <textarea style={{ ...inputStyle, height: "180px", resize: "vertical", fontFamily: "inherit" }} value={form.script} onChange={set("script")} placeholder="Write the story script here..." />
          </div>

          <div style={fieldStyle}>
            <label style={labelStyle}>Narration file (path or filename)</label>
            <input style={inputStyle} value={form.narration_file} onChange={set("narration_file")} placeholder="e.g. narration/messi-story.mp3" />
          </div>

          <div style={fieldStyle}>
            <label style={labelStyle}>Media metadata (JSON)</label>
            <textarea style={{ ...inputStyle, height: "100px", resize: "vertical", fontFamily: "monospace", fontSize: "0.85rem", borderColor: errors.media_metadata ? "#7a2020" : "#31533a" }} value={form.media_metadata} onChange={set("media_metadata")} />
            {errors.media_metadata && <p style={errStyle}>{errors.media_metadata}</p>}
          </div>

          <div style={fieldStyle}>
            <label style={labelStyle}>Source & rights metadata (JSON)</label>
            <textarea style={{ ...inputStyle, height: "80px", resize: "vertical", fontFamily: "monospace", fontSize: "0.85rem" }} value={form.source_rights_metadata} onChange={set("source_rights_metadata")} />
          </div>

          <div style={{ display: "flex", gap: "12px" }}>
            <button type="submit" disabled={saving} style={{ padding: "13px 24px", borderRadius: "9px", background: saving ? "#1e4a28" : "#22c55e", border: "none", color: "#06100a", fontWeight: "800", fontSize: "1rem", cursor: saving ? "not-allowed" : "pointer" }}>
              {saving ? "Saving..." : isEditing ? "Save changes" : "Create story"}
            </button>
            <button type="button" onClick={() => navigate("/dashboard")} className="secondary">
              Cancel
            </button>
          </div>
        </form>
      </main>
      <Footer />
    </div>
  );
}
