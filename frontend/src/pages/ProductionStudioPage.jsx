import React, { useMemo, useState } from "react";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

const PIPELINE = [
  { id: "draft", label: "Draft", icon: "??" },
  { id: "scripted", label: "Scripted", icon: "??" },
  { id: "scenes", label: "Scenes Ready", icon: "??" },
  { id: "voice", label: "Voice", icon: "???" },
  { id: "rendering", label: "Rendering", icon: "??" },
  { id: "rendered", label: "Rendered", icon: "???" },
  { id: "published", label: "Published", icon: "??" },
];

const INITIAL_SCENES = [
  {
    id: 1,
    title: "Opening Hook",
    duration: 8,
    narration: "Every football legend has a moment that changes everything.",
    visual: "Cinematic football stadium at night, dramatic lights, crowd anticipation.",
    camera: "Slow push-in",
    emotion: "Epic",
  },
  {
    id: 2,
    title: "The Beginning",
    duration: 12,
    narration: "Before the trophies and headlines, there was only a dream.",
    visual: "Young footballer walking onto a neighborhood pitch at sunset.",
    camera: "Wide establishing shot",
    emotion: "Inspirational",
  },
];

function Field({ label, value, onChange, placeholder, textarea = false }) {
  const props = {
    value,
    onChange: (e) => onChange(e.target.value),
    placeholder,
  };

  return (
    <label className="studio-field">
      <span>{label}</span>
      {textarea ? <textarea {...props} rows={5} /> : <input {...props} />}
    </label>
  );
}

export default function ProductionStudioPage() {
  const [activeTab, setActiveTab] = useState("story");
  const [status, setStatus] = useState("draft");
  const [story, setStory] = useState({
    title: "The Moment That Changed Football",
    category: "Football History",
    description: "A cinematic football story designed for short-form documentary content.",
    hook: "One moment. One decision. A completely different football history.",
    ending: "And that is why football remembers the moments that ordinary people forget.",
  });

  const [scenes, setScenes] = useState(INITIAL_SCENES);
  const [selectedScene, setSelectedScene] = useState(1);
  const [characters, setCharacters] = useState([
    { id: 1, name: "Main Player", role: "Protagonist", emotion: "Determined" },
    { id: 2, name: "Coach", role: "Mentor", emotion: "Serious" },
  ]);

  const [characterForm, setCharacterForm] = useState({
    name: "",
    role: "Character",
    emotion: "Neutral",
  });

  const scene = useMemo(
    () => scenes.find((item) => item.id === selectedScene) || scenes[0],
    [scenes, selectedScene]
  );

  const updateScene = (field, value) => {
    setScenes((current) =>
      current.map((item) =>
        item.id === selectedScene ? { ...item, [field]: value } : item
      )
    );
  };

  const addScene = () => {
    const nextId = Math.max(...scenes.map((item) => item.id), 0) + 1;
    const next = {
      id: nextId,
      title: `Scene ${nextId}`,
      duration: 10,
      narration: "",
      visual: "",
      camera: "Medium shot",
      emotion: "Neutral",
    };
    setScenes([...scenes, next]);
    setSelectedScene(nextId);
    setActiveTab("scenes");
  };

  const removeScene = () => {
    if (scenes.length <= 1) return;
    const remaining = scenes.filter((item) => item.id !== selectedScene);
    setScenes(remaining);
    setSelectedScene(remaining[0].id);
  };

  const addCharacter = () => {
    if (!characterForm.name.trim()) return;
    const nextId = Math.max(...characters.map((item) => item.id), 0) + 1;
    setCharacters([...characters, { ...characterForm, id: nextId }]);
    setCharacterForm({ name: "", role: "Character", emotion: "Neutral" });
  };

  const saveDraft = () => {
    localStorage.setItem(
      "footballverse-production-studio",
      JSON.stringify({ story, scenes, characters, status })
    );
    alert("Production project saved locally.");
  };

  return (
    <div className="app">
      <Nav />

      <main className="studio-page">
        <section className="studio-hero">
          <div>
            <span className="tag">FOOTBALLVERSE STUDIO</span>
            <h1>Production Workspace</h1>
            <p>
              Turn football history into structured stories, scenes, characters
              and production-ready animation instructions.
            </p>
          </div>

          <div className="studio-actions">
            <button className="secondary" onClick={saveDraft}>
              Save Project
            </button>
            <button className="studio-primary" onClick={() => setStatus("scripted")}>
              Continue Production ?
            </button>
          </div>
        </section>

        <section className="pipeline">
          {PIPELINE.map((item, index) => {
            const activeIndex = PIPELINE.findIndex((x) => x.id === status);
            return (
              <div
                key={item.id}
                className={`pipeline-step ${
                  index <= activeIndex ? "complete" : ""
                } ${item.id === status ? "current" : ""}`}
                onClick={() => setStatus(item.id)}
              >
                <span>{item.icon}</span>
                <strong>{item.label}</strong>
              </div>
            );
          })}
        </section>

        <section className="studio-layout">
          <aside className="studio-sidebar">
            <h3>Production</h3>

            {[
              ["story", "??", "Story"],
              ["script", "??", "Script"],
              ["scenes", "??", "Scenes"],
              ["characters", "??", "Characters"],
              ["visuals", "??", "Visual Direction"],
              ["audio", "???", "Audio"],
            ].map(([id, icon, label]) => (
              <button
                key={id}
                className={activeTab === id ? "studio-nav active" : "studio-nav"}
                onClick={() => setActiveTab(id)}
              >
                <span>{icon}</span>
                {label}
              </button>
            ))}

            <div className="sidebar-divider" />

            <div className="project-stat">
              <span>Scenes</span>
              <strong>{scenes.length}</strong>
            </div>

            <div className="project-stat">
              <span>Characters</span>
              <strong>{characters.length}</strong>
            </div>

            <div className="project-stat">
              <span>Est. Runtime</span>
              <strong>{scenes.reduce((sum, item) => sum + Number(item.duration || 0), 0)}s</strong>
            </div>
          </aside>

          <section className="studio-editor">
            {activeTab === "story" && (
              <>
                <div className="editor-heading">
                  <div>
                    <span className="editor-kicker">01 / STORY</span>
                    <h2>Story Foundation</h2>
                  </div>
                </div>

                <div className="editor-grid">
                  <Field
                    label="Story title"
                    value={story.title}
                    onChange={(value) => setStory({ ...story, title: value })}
                    placeholder="Enter story title"
                  />

                  <Field
                    label="Category"
                    value={story.category}
                    onChange={(value) => setStory({ ...story, category: value })}
                    placeholder="Football History"
                  />
                </div>

                <Field
                  label="Description"
                  value={story.description}
                  onChange={(value) => setStory({ ...story, description: value })}
                  placeholder="Describe the story"
                  textarea
                />

                <Field
                  label="Opening hook"
                  value={story.hook}
                  onChange={(value) => setStory({ ...story, hook: value })}
                  placeholder="The first sentence should make people stop scrolling."
                  textarea
                />

                <Field
                  label="Ending"
                  value={story.ending}
                  onChange={(value) => setStory({ ...story, ending: value })}
                  placeholder="How should the story conclude?"
                  textarea
                />
              </>
            )}

            {activeTab === "script" && (
              <>
                <div className="editor-heading">
                  <div>
                    <span className="editor-kicker">02 / SCRIPT</span>
                    <h2>Script Editor</h2>
                  </div>
                  <span className="status-pill">{status.toUpperCase()}</span>
                </div>

                <div className="script-card">
                  <span>HOOK</span>
                  <h3>{story.hook}</h3>
                </div>

                <Field
                  label="Narrator script"
                  value={story.description}
                  onChange={(value) => setStory({ ...story, description: value })}
                  placeholder="Write the full narration..."
                  textarea
                />

                <div className="script-tip">
                  ?? Keep narration conversational. Short sentences work better
                  for animated football storytelling.
                </div>
              </>
            )}

            {activeTab === "scenes" && (
              <>
                <div className="editor-heading">
                  <div>
                    <span className="editor-kicker">03 / SCENES</span>
                    <h2>Scene Builder</h2>
                  </div>

                  <div className="scene-actions">
                    <button className="secondary" onClick={removeScene}>
                      Remove
                    </button>
                    <button className="studio-primary" onClick={addScene}>
                      + Add Scene
                    </button>
                  </div>
                </div>

                <div className="scene-list">
                  {scenes.map((item, index) => (
                    <button
                      key={item.id}
                      className={
                        selectedScene === item.id
                          ? "scene-item selected"
                          : "scene-item"
                      }
                      onClick={() => setSelectedScene(item.id)}
                    >
                      <span className="scene-number">
                        {String(index + 1).padStart(2, "0")}
                      </span>
                      <span>
                        <strong>{item.title || "Untitled scene"}</strong>
                        <small>{item.duration}s � {item.emotion}</small>
                      </span>
                    </button>
                  ))}
                </div>

                {scene && (
                  <div className="scene-editor">
                    <div className="scene-header">
                      <span>SCENE {String(scene.id).padStart(2, "0")}</span>
                      <strong>{scene.duration}s</strong>
                    </div>

                    <Field
                      label="Scene title"
                      value={scene.title}
                      onChange={(value) => updateScene("title", value)}
                    />

                    <Field
                      label="Narration / dialogue"
                      value={scene.narration}
                      onChange={(value) => updateScene("narration", value)}
                      textarea
                    />

                    <Field
                      label="Visual direction"
                      value={scene.visual}
                      onChange={(value) => updateScene("visual", value)}
                      textarea
                    />

                    <div className="editor-grid">
                      <Field
                        label="Camera"
                        value={scene.camera}
                        onChange={(value) => updateScene("camera", value)}
                      />

                      <Field
                        label="Emotion"
                        value={scene.emotion}
                        onChange={(value) => updateScene("emotion", value)}
                      />
                    </div>

                    <label className="studio-field">
                      <span>Duration: {scene.duration}s</span>
                      <input
                        type="range"
                        min="3"
                        max="60"
                        value={scene.duration}
                        onChange={(e) =>
                          updateScene("duration", Number(e.target.value))
                        }
                      />
                    </label>
                  </div>
                )}
              </>
            )}

            {activeTab === "characters" && (
              <>
                <div className="editor-heading">
                  <div>
                    <span className="editor-kicker">04 / CHARACTERS</span>
                    <h2>Character Library</h2>
                  </div>
                </div>

                <div className="character-grid">
                  {characters.map((character) => (
                    <article className="character-card" key={character.id}>
                      <div className="character-avatar">?</div>
                      <div>
                        <h3>{character.name}</h3>
                        <p>{character.role}</p>
                        <span>{character.emotion}</span>
                      </div>
                    </article>
                  ))}
                </div>

                <div className="add-character">
                  <h3>Add character</h3>

                  <div className="editor-grid">
                    <Field
                      label="Name"
                      value={characterForm.name}
                      onChange={(value) =>
                        setCharacterForm({ ...characterForm, name: value })
                      }
                      placeholder="e.g. Lionel Messi"
                    />

                    <Field
                      label="Role"
                      value={characterForm.role}
                      onChange={(value) =>
                        setCharacterForm({ ...characterForm, role: value })
                      }
                      placeholder="Protagonist"
                    />
                  </div>

                  <Field
                    label="Default emotion"
                    value={characterForm.emotion}
                    onChange={(value) =>
                      setCharacterForm({ ...characterForm, emotion: value })
                    }
                    placeholder="Determined"
                  />

                  <button className="studio-primary" onClick={addCharacter}>
                    Add Character
                  </button>
                </div>
              </>
            )}

            {activeTab === "visuals" && (
              <>
                <div className="editor-heading">
                  <div>
                    <span className="editor-kicker">05 / VISUALS</span>
                    <h2>Cartoon & Visual Direction</h2>
                  </div>
                </div>

                <div className="visual-presets">
                  {[
                    ["??", "Football Cartoon", "Expressive 2D football animation"],
                    ["??", "Cinematic", "Dramatic documentary visuals"],
                    ["??", "Sports Documentary", "Editorial historical style"],
                    ["??", "Comedy", "Exaggerated humorous animation"],
                  ].map(([icon, title, description]) => (
                    <button key={title} className="visual-preset">
                      <span>{icon}</span>
                      <strong>{title}</strong>
                      <small>{description}</small>
                    </button>
                  ))}
                </div>

                <Field
                  label="Global visual prompt"
                  value="Stylized football documentary, expressive cartoon characters, dramatic stadium lighting, cinematic composition."
                  onChange={() => {}}
                  textarea
                />
              </>
            )}

            {activeTab === "audio" && (
              <>
                <div className="editor-heading">
                  <div>
                    <span className="editor-kicker">06 / AUDIO</span>
                    <h2>Narration & Audio</h2>
                  </div>
                </div>

                <div className="audio-panel">
                  <div className="audio-icon">???</div>
                  <div>
                    <h3>AI Narration</h3>
                    <p>Prepare your script for voice generation.</p>
                  </div>
                  <span className="coming">READY FOR INTEGRATION</span>
                </div>

                <div className="editor-grid">
                  <Field label="Voice style" value="Documentary" onChange={() => {}} />
                  <Field label="Language" value="English" onChange={() => {}} />
                </div>
              </>
            )}
          </section>
        </section>
      </main>

      <Footer />
    </div>
  );
}
