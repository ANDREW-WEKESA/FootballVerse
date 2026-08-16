# FootballVerse Completion - Technical Design

## Overview

This document details the technical implementation approach for completing the four priority features of FootballVerse.

---

## Priority 1: Alembic Database Migrations

### Architecture

```
backend/
├── alembic/
│   ├── versions/          # Migration scripts
│   │   └── 001_initial_schema.py
│   ├── env.py            # Alembic environment config
│   └── script.py.mako    # Migration template
├── alembic.ini           # Alembic configuration
└── app/
    ├── main.py           # Modified: run migrations on startup
    └── database.py       # Modified: remove create_all()
```

### Implementation Approach

#### Step 1: Initialize Alembic
```bash
cd backend
alembic init alembic
```

#### Step 2: Configure `alembic.ini`
- Set `sqlalchemy.url` to read from environment variable
- Configure logging
- Set script location to `alembic/`

**File: `backend/alembic.ini`**
```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = 

[loggers]
keys = root,sqlalchemy,alembic

# ... standard config
```

#### Step 3: Configure `alembic/env.py`
- Import `Base` from `app.database`
- Set `target_metadata = Base.metadata`
- Read `DATABASE_URL` from environment
- Configure both online and offline migrations

**Key changes:**
```python
from app.database import Base
from app.config import DATABASE_URL  # or os.getenv()

target_metadata = Base.metadata

def run_migrations_online():
    connectable = create_engine(DATABASE_URL)
    # ... migration logic
```

#### Step 4: Create Initial Migration
```bash
alembic revision --autogenerate -m "Initial schema"
```

This will create `alembic/versions/001_xxxx_initial_schema.py` with:
- `upgrade()`: Creates all 8 tables
- `downgrade()`: Drops all tables

#### Step 5: Modify Startup to Run Migrations
**File: `backend/app/main.py`**

Remove:
```python
Base.metadata.create_all(engine)
```

Add migration runner in `lifespan`:
```python
from alembic import command
from alembic.config import Config

@asynccontextmanager
async def lifespan(app):
    # Run migrations
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

    # Ensure admin exists
    db = SessionLocal()
    try:
        ensure_admin_exists(db)
    finally:
        db.close()
    
    yield
```

#### Step 6: Add Migration Helper Script
**File: `backend/migrate.py`**
```python
#!/usr/bin/env python
"""Manual migration runner for development"""
import sys
from alembic import command
from alembic.config import Config

def main():
    alembic_cfg = Config("alembic.ini")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "upgrade":
            command.upgrade(alembic_cfg, "head")
        elif sys.argv[1] == "downgrade":
            command.downgrade(alembic_cfg, "-1")
        elif sys.argv[1] == "history":
            command.history(alembic_cfg)
    else:
        print("Usage: python migrate.py [upgrade|downgrade|history]")

if __name__ == "__main__":
    main()
```

### Testing Strategy
1. Backup existing `footballverse.db`
2. Test migration on backup: `alembic upgrade head`
3. Verify all tables exist with correct schema
4. Verify existing data preserved
5. Test downgrade: `alembic downgrade base`
6. Re-run upgrade, start app, verify functionality

### Error Handling
- Migration failures log detailed error with stack trace
- App exits with non-zero code on migration failure
- Missing `DATABASE_URL` handled by existing `database.py` logic

---

## Priority 2: Video Rendering Pipeline

### Architecture

```
backend/
├── app/
│   ├── main.py                    # Existing: render endpoint
│   ├── services/
│   │   ├── video_renderer.py     # NEW: Core rendering logic
│   │   ├── tts_service.py        # NEW: Text-to-speech
│   │   └── scene_generator.py    # NEW: Visual scene creation
│   └── models/
│       └── render_config.py      # NEW: Rendering configuration
├── static/
│   └── videos/                    # Output directory
├── temp/                          # NEW: Temporary files during render
└── requirements.txt               # Add: Pillow, gTTS, moviepy
```

### Technology Stack
- **Video Compilation**: `moviepy` (Python wrapper for ffmpeg)
- **Text-to-Speech**: `gTTS` (Google Text-to-Speech, free, good quality)
- **Image Generation**: `Pillow` (PIL) for title cards and overlays
- **Format**: MP4 with H.264 codec

### Implementation Approach

#### Step 1: Install Dependencies
**Add to `requirements.txt`:**
```
Pillow==11.1.0
gTTS==2.5.4
moviepy==1.0.3
```

#### Step 2: Create TTS Service
**File: `backend/app/services/tts_service.py`**
```python
from gtts import gTTS
import os
from pathlib import Path

class TTSService:
    """Text-to-speech narration generator"""
    
    def __init__(self, output_dir: str = "temp"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_narration(self, text: str, story_id: int) -> str:
        """Generate audio narration from script text"""
        if not text.strip():
            return None
        
        output_path = self.output_dir / f"narration_{story_id}.mp3"
        
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
            return str(output_path)
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds"""
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        return duration
```

#### Step 3: Create Scene Generator
**File: `backend/app/services/scene_generator.py`**
```python
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

class SceneGenerator:
    """Generate visual scenes for video"""
    
    def __init__(self, resolution=(1280, 720)):
        self.width, self.height = resolution
        self.output_dir = Path("temp")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_title_card(self, title: str, story_id: int) -> str:
        """Create opening title card"""
        img = Image.new('RGB', (self.width, self.height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Try to load font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 72)
            subtitle_font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Draw title (centered)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((self.width - text_width) // 2, 
                   (self.height - text_height) // 2 - 50)
        draw.text(position, title, fill='white', font=font)
        
        # Draw subtitle
        subtitle = "A FootballVerse Story"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_width = bbox[2] - bbox[0]
        sub_position = ((self.width - sub_width) // 2, 
                       position[1] + text_height + 30)
        draw.text(sub_position, subtitle, fill='#aaaaaa', font=subtitle_font)
        
        # Save
        output_path = self.output_dir / f"title_{story_id}.png"
        img.save(output_path)
        return str(output_path)
    
    def create_text_scene(self, text: str, story_id: int, scene_num: int) -> str:
        """Create scene with text overlay"""
        img = Image.new('RGB', (self.width, self.height), color='#16213e')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        # Wrap text to fit width
        margin = 100
        max_width = self.width - (2 * margin)
        wrapped_lines = textwrap.wrap(text, width=40)
        
        # Draw text lines
        y_offset = (self.height - len(wrapped_lines) * 60) // 2
        for line in wrapped_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (self.width - line_width) // 2
            draw.text((x, y_offset), line, fill='white', font=font)
            y_offset += 60
        
        output_path = self.output_dir / f"scene_{story_id}_{scene_num}.png"
        img.save(output_path)
        return str(output_path)
    
    def create_parody_disclaimer(self, story_id: int) -> str:
        """Create parody disclaimer card"""
        img = Image.new('RGB', (self.width, self.height), color='#000000')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        disclaimer = [
            "PARODY DISCLAIMER",
            "",
            "This content is a fictional parody for entertainment purposes.",
            "Any resemblance to actual events or persons is coincidental.",
            "Sources: TheSportsDB and publicly available football data."
        ]
        
        y_offset = 200
        for line in disclaimer:
            if line:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                x = (self.width - line_width) // 2
                draw.text((x, y_offset), line, fill='yellow' if 'PARODY' in line else 'white', font=font)
            y_offset += 50
        
        output_path = self.output_dir / f"disclaimer_{story_id}.png"
        img.save(output_path)
        return str(output_path)
```

#### Step 4: Create Video Renderer
**File: `backend/app/services/video_renderer.py`**
```python
from moviepy.editor import *
from pathlib import Path
import logging
from .tts_service import TTSService
from .scene_generator import SceneGenerator

logger = logging.getLogger(__name__)

class VideoRenderer:
    """Main video rendering orchestrator"""
    
    def __init__(self):
        self.tts = TTSService()
        self.scene_gen = SceneGenerator()
        self.output_dir = Path("static/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def render_story(self, story_id: int, title: str, script: str) -> dict:
        """
        Render a complete story video
        Returns: {"output_path": str, "duration": float, "file_size": int}
        """
        try:
            clips = []
            
            # 1. Title card (3 seconds)
            title_img = self.scene_gen.create_title_card(title, story_id)
            title_clip = ImageClip(title_img).set_duration(3)
            clips.append(title_clip)
            
            # 2. Parody disclaimer (5 seconds)
            disclaimer_img = self.scene_gen.create_parody_disclaimer(story_id)
            disclaimer_clip = ImageClip(disclaimer_img).set_duration(5)
            clips.append(disclaimer_clip)
            
            # 3. Generate narration
            narration_path = None
            if script.strip():
                narration_path = self.tts.generate_narration(script, story_id)
                audio_duration = self.tts.get_audio_duration(narration_path)
                
                # Create text scene for duration of narration
                script_img = self.scene_gen.create_text_scene(
                    script[:200] + "..." if len(script) > 200 else script,
                    story_id,
                    1
                )
                script_clip = ImageClip(script_img).set_duration(audio_duration)
                
                # Add audio to clip
                audio = AudioFileClip(narration_path)
                script_clip = script_clip.set_audio(audio)
                clips.append(script_clip)
            
            # 4. Concatenate all clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # 5. Export video
            output_filename = f"story_{story_id}_{int(time.time())}.mp4"
            output_path = self.output_dir / output_filename
            
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                bitrate='2000k',
                preset='medium'
            )
            
            # 6. Get file info
            file_size = output_path.stat().st_size
            duration = final_video.duration
            
            # 7. Cleanup
            final_video.close()
            self._cleanup_temp_files(story_id)
            
            return {
                "output_path": str(output_path),
                "duration": duration,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Video rendering failed for story {story_id}: {e}")
            self._cleanup_temp_files(story_id)
            raise
    
    def _cleanup_temp_files(self, story_id: int):
        """Clean up temporary files after rendering"""
        import glob
        patterns = [
            f"temp/narration_{story_id}.*",
            f"temp/title_{story_id}.*",
            f"temp/scene_{story_id}_*.*",
            f"temp/disclaimer_{story_id}.*"
        ]
        for pattern in patterns:
            for file in glob.glob(pattern):
                try:
                    Path(file).unlink()
                except:
                    pass
```

#### Step 5: Integrate with Endpoint
**Modify: `backend/app/main.py`**

Replace the placeholder render endpoint:
```python
from .services.video_renderer import VideoRenderer
import asyncio

# Initialize renderer
video_renderer = VideoRenderer()

@app.post("/stories/{story_id}/render", tags=["stories"], summary="Trigger render (admin)")
async def render_story(
    story_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story.status != "draft":
        raise HTTPException(status_code=409, detail="Only draft stories can be rendered")
    
    try:
        # Run rendering in thread pool to not block event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            video_renderer.render_story,
            story.id,
            story.title,
            story.script
        )
        
        # Update story
        story.status = "rendered"
        story.render_output_path = result["output_path"]
        db.commit()
        
        logger.info(f"Story {story_id} rendered successfully: {result['file_size_mb']}MB, {result['duration']}s")
        
        return {
            "status": "success",
            "story_id": story_id,
            "output_path": result["output_path"],
            "duration": result["duration"],
            "file_size_mb": result["file_size_mb"]
        }
        
    except Exception as e:
        logger.error(f"Render failed for story {story_id}: {e}")
        story.status = "draft"  # Revert status
        db.commit()
        raise HTTPException(status_code=500, detail=f"Rendering failed: {str(e)}")
```

### Testing Strategy
1. Create test story with simple script
2. Trigger render via API
3. Verify MP4 file created in `static/videos/`
4. Verify file size < 40MB
5. Verify video plays in browser
6. Test error handling (empty script, missing story, etc.)

### Performance Considerations
- Rendering runs in thread pool (async)
- Consider background task queue (Celery) for production
- Cache TTS results for identical scripts
- Optimize image generation (reuse templates)

---

## Priority 3: Frontend UI Completion

### Architecture

```
frontend/src/
├── pages/
│   ├── DashboardPage.jsx          # MODIFY: Complete implementation
│   ├── StoryStudioPage.jsx        # MODIFY: Complete implementation
│   ├── PlayersPage.jsx            # VERIFY: Add search debounce
│   └── PlayerDetailPage.jsx       # VERIFY: Timeline rendering
├── components/
│   ├── StoryForm.jsx              # NEW: Reusable story form
│   ├── StoryCard.jsx              # NEW: Story list item
│   ├── StatusBadge.jsx            # NEW: Status indicator
│   ├── LoadingSpinner.jsx         # NEW: Loading state
│   └── ErrorMessage.jsx           # NEW: Error display
└── hooks/
    ├── useStories.js              # NEW: Stories data hook
    ├── usePlayers.js              # NEW: Players data hook
    └── useDebounce.js             # NEW: Debounce hook
```

### Implementation Approach

#### Step 1: Create Shared Components

**File: `frontend/src/components/LoadingSpinner.jsx`**
```jsx
export default function LoadingSpinner() {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p>Loading...</p>
    </div>
  );
}
```

**File: `frontend/src/components/ErrorMessage.jsx`**
```jsx
export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-message">
      <p>❌ {message}</p>
      {onRetry && <button onClick={onRetry}>Retry</button>}
    </div>
  );
}
```

**File: `frontend/src/components/StatusBadge.jsx`**
```jsx
export default function StatusBadge({ status }) {
  const colors = {
    draft: 'yellow',
    rendered: 'blue',
    published: 'green'
  };
  
  return (
    <span className={`status-badge status-${colors[status]}`}>
      {status.toUpperCase()}
    </span>
  );
}
```

#### Step 2: Create Custom Hooks

**File: `frontend/src/hooks/useDebounce.js`**
```jsx
import { useState, useEffect } from 'react';

export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

**File: `frontend/src/hooks/useStories.js`**
```jsx
import { useState, useEffect } from 'react';

export function useStories(token) {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStories = async () => {
    setLoading(true);
    setError(null);
    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await fetch('http://127.0.0.1:8000/stories', { headers });
      if (!res.ok) throw new Error('Failed to fetch stories');
      const data = await res.json();
      setStories(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStories();
  }, [token]);

  return { stories, loading, error, refetch: fetchStories };
}
```

#### Step 3: Implement Dashboard Page

**File: `frontend/src/pages/DashboardPage.jsx`**
```jsx
import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { useStories } from '../hooks/useStories';
import Nav from '../components/Nav';
import Footer from '../components/Footer';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import StatusBadge from '../components/StatusBadge';

export default function DashboardPage() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();
  const { stories, loading, error, refetch } = useStories(token);
  const [deleting, setDeleting] = useState(null);

  const handleDelete = async (storyId) => {
    if (!confirm('Are you sure you want to delete this story?')) return;
    
    setDeleting(storyId);
    try {
      const res = await fetch(`http://127.0.0.1:8000/stories/${storyId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Delete failed');
      refetch();
    } catch (err) {
      alert('Failed to delete story: ' + err.message);
    } finally {
      setDeleting(null);
    }
  };

  const handlePublish = async (storyId) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/stories/${storyId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ status: 'published' })
      });
      if (!res.ok) throw new Error('Publish failed');
      refetch();
    } catch (err) {
      alert('Failed to publish: ' + err.message);
    }
  };

  return (
    <>
      <Nav />
      <main className="dashboard">
        <div className="dashboard-header">
          <h1>Story Dashboard</h1>
          <button onClick={() => navigate('/studio/new')} className="btn-primary">
            + Create New Story
          </button>
        </div>

        {loading && <LoadingSpinner />}
        {error && <ErrorMessage message={error} onRetry={refetch} />}
        
        {!loading && !error && stories.length === 0 && (
          <div className="empty-state">
            <p>No stories yet. Create your first story!</p>
            <button onClick={() => navigate('/studio/new')}>Create Story</button>
          </div>
        )}

        {!loading && !error && stories.length > 0 && (
          <div className="stories-table">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Linked To</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {stories.map(story => (
                  <tr key={story.id}>
                    <td>{story.title}</td>
                    <td>
                      {story.player_id && `Player #${story.player_id}`}
                      {story.club_id && `Club #${story.club_id}`}
                    </td>
                    <td><StatusBadge status={story.status} /></td>
                    <td>{new Date(story.created_at).toLocaleDateString()}</td>
                    <td className="actions">
                      <button onClick={() => navigate(`/studio/${story.id}`)}>
                        Edit
                      </button>
                      {story.status === 'rendered' && (
                        <button onClick={() => handlePublish(story.id)}>
                          Publish
                        </button>
                      )}
                      <button 
                        onClick={() => handleDelete(story.id)}
                        disabled={deleting === story.id}
                        className="btn-danger"
                      >
                        {deleting === story.id ? 'Deleting...' : 'Delete'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
```

#### Step 4: Implement Story Studio Page

**File: `frontend/src/pages/StoryStudioPage.jsx`**
```jsx
import { useContext, useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import Nav from '../components/Nav';
import Footer from '../components/Footer';

export default function StoryStudioPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token } = useContext(AuthContext);
  
  const [formData, setFormData] = useState({
    title: '',
    player_id: '',
    club_id: '',
    script: '',
    narration_file: ''
  });
  
  const [players, setPlayers] = useState([]);
  const [clubs, setClubs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [rendering, setRendering] = useState(false);
  const [story, setStory] = useState(null);
  const [error, setError] = useState('');

  // Fetch story if editing
  useEffect(() => {
    if (id && id !== 'new') {
      fetchStory();
    }
  }, [id]);

  // Fetch players and clubs
  useEffect(() => {
    fetchPlayers();
    fetchClubs();
  }, []);

  const fetchStory = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/stories/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      setStory(data);
      setFormData({
        title: data.title,
        player_id: data.player_id || '',
        club_id: data.club_id || '',
        script: data.script,
        narration_file: data.narration_file || ''
      });
    } catch (err) {
      setError('Failed to load story');
    }
  };

  const fetchPlayers = async () => {
    const res = await fetch('http://127.0.0.1:8000/players');
    const data = await res.json();
    setPlayers(data);
  };

  const fetchClubs = async () => {
    const res = await fetch('http://127.0.0.1:8000/clubs');
    const data = await res.json();
    setClubs(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!formData.title) {
      setError('Title is required');
      return;
    }
    if (!formData.player_id && !formData.club_id) {
      setError('Please select either a player or club');
      return;
    }

    setLoading(true);
    try {
      const method = story ? 'PUT' : 'POST';
      const url = story 
        ? `http://127.0.0.1:8000/stories/${id}`
        : 'http://127.0.0.1:8000/stories';
      
      const payload = {
        ...formData,
        player_id: formData.player_id ? parseInt(formData.player_id) : null,
        club_id: formData.club_id ? parseInt(formData.club_id) : null
      };

      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Save failed');
      }

      alert('Story saved successfully!');
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRender = async () => {
    setRendering(true);
    setError('');
    try {
      const res = await fetch(`http://127.0.0.1:8000/stories/${id}/render`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Render failed');
      }

      const result = await res.json();
      alert(`Rendering complete! Duration: ${result.duration}s, Size: ${result.file_size_mb}MB`);
      fetchStory(); // Refresh to update status
    } catch (err) {
      setError(err.message);
    } finally {
      setRendering(false);
    }
  };

  return (
    <>
      <Nav />
      <main className="story-studio">
        <h1>{story ? 'Edit Story' : 'Create New Story'}</h1>
        
        <div className="parody-disclaimer">
          ⚠️ <strong>Parody Disclaimer:</strong> All content is fictional parody for entertainment purposes only.
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Title *</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              placeholder="Enter story title"
              required
            />
          </div>

          <div className="form-group">
            <label>Player</label>
            <select
              value={formData.player_id}
              onChange={(e) => setFormData({...formData, player_id: e.target.value, club_id: ''})}
            >
              <option value="">-- Select Player --</option>
              {players.map(p => (
                <option key={p.id} value={p.id}>{p.full_name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Club</label>
            <select
              value={formData.club_id}
              onChange={(e) => setFormData({...formData, club_id: e.target.value, player_id: ''})}
            >
              <option value="">-- Select Club --</option>
              {clubs.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Script *</label>
            <textarea
              value={formData.script}
              onChange={(e) => setFormData({...formData, script: e.target.value})}
              placeholder="Write your story script here..."
              rows={10}
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Saving...' : story ? 'Update Story' : 'Create Story'}
            </button>
            
            {story && story.status === 'draft' && (
              <button 
                type="button" 
                onClick={handleRender} 
                disabled={rendering}
                className="btn-secondary"
              >
                {rendering ? 'Rendering...' : '🎬 Trigger Render'}
              </button>
            )}
            
            {story && story.status === 'rendered' && story.render_output_path && (
              <a 
                href={`http://127.0.0.1:8000/videos/${story.render_output_path.split('/').pop()}`}
                download
                className="btn-success"
              >
                ⬇️ Download Video
              </a>
            )}
          </div>
        </form>
      </main>
      <Footer />
    </>
  );
}
```

#### Step 5: Add Search Debounce to Players Page

**Modify: `frontend/src/pages/PlayersPage.jsx`**
```jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDebounce } from '../hooks/useDebounce';
import Nav from '../components/Nav';
import Footer from '../components/Footer';

export default function PlayersPage() {
  const navigate = useNavigate();
  const [players, setPlayers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  
  const debouncedSearch = useDebounce(searchTerm, 300);

  useEffect(() => {
    fetchPlayers(debouncedSearch);
  }, [debouncedSearch]);

  const fetchPlayers = async (search) => {
    setLoading(true);
    try {
      const url = search && search.length >= 2
        ? `http://127.0.0.1:8000/players?search=${encodeURIComponent(search)}`
        : 'http://127.0.0.1:8000/players';
      const res = await fetch(url);
      const data = await res.json();
      setPlayers(data);
    } catch (err) {
      console.error('Failed to fetch players:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Nav />
      <main className="players-page">
        <h1>Players</h1>
        
        <div className="search-box">
          <input
            type="text"
            placeholder="Search players..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {loading && <span className="searching">Searching...</span>}
        </div>

        <div className="players-grid">
          {players.map(player => (
            <div 
              key={player.id} 
              className="player-card"
              onClick={() => navigate(`/players/${player.id}`)}
            >
              {player.image_url && <img src={player.image_url} alt={player.full_name} />}
              <h3>{player.full_name}</h3>
              <p>{player.nationality} • {player.position}</p>
              <div className="player-stats">
                <span>⚽ {player.goals}</span>
                <span>👕 {player.appearances}</span>
                <span>🏆 {player.trophies}</span>
              </div>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </>
  );
}
```

### Styling Approach
- Add CSS to `frontend/src/style.css`
- Use CSS Grid for responsive layouts
- Mobile-first approach (375px base)
- Breakpoints: 768px (tablet), 1024px (desktop)

### Testing Strategy
1. Manual testing in browser at different screen sizes
2. Test all form validations
3. Test loading/error states by throttling network
4. Test keyboard navigation (Tab, Enter, Escape)
5. Verify accessibility (alt text, ARIA labels if needed)

---

## Priority 4: API Documentation Enhancement

### Implementation Approach

#### Step 1: Create Response Models
**File: `backend/app/schemas.py`** (NEW)
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Player schemas
class PlayerResponse(BaseModel):
    id: int
    external_id: str
    full_name: str
    nationality: str
    date_of_birth: str
    position: str
    image_url: str
    goals: int
    appearances: int
    assists: int
    trophies: int

    class Config:
        from_attributes = True

# Club schemas
class ClubResponse(BaseModel):
    id: int
    name: str
    country: str
    founded_year: Optional[int]
    stadium: str
    trophies: int
    logo_url: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

# Story schemas
class StoryResponse(BaseModel):
    id: int
    title: str
    player_id: Optional[int]
    club_id: Optional[int]
    script: str
    media_metadata: dict
    source_rights_metadata: dict
    narration_file: str
    status: str
    render_output_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Auth schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Error schemas
class ErrorDetail(BaseModel):
    detail: str

class ValidationError(BaseModel):
    detail: list[dict]
```

#### Step 2: Add Response Models to Endpoints
**Modify: `backend/app/main.py`**

Add imports:
```python
from .schemas import (
    PlayerResponse,
    ClubResponse,
    StoryResponse,
    TokenResponse,
    ErrorDetail
)
```

Update endpoints with response models:
```python
@app.post(
    "/auth/login",
    tags=["auth"],
    summary="Admin login — returns JWT",
    description="Authenticate with email and password. Returns a JWT token valid for 24 hours.",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorDetail, "description": "Invalid credentials"}
    }
)
async def login(...):
    ...

@app.get(
    "/players",
    tags=["players"],
    summary="List all players",
    description="Returns all players, optionally filtered by name search (case-insensitive substring match).",
    response_model=list[PlayerResponse],
    responses={
        422: {"model": ErrorDetail, "description": "Search term too short (min 2 chars)"}
    }
)
def all_players(...):
    ...

@app.get(
    "/players/{player_id}",
    tags=["players"],
    summary="Get a player by ID",
    description="Returns detailed player information including stats and career data.",
    response_model=PlayerResponse,
    responses={
        404: {"model": ErrorDetail, "description": "Player not found"}
    }
)
def get_player(...):
    ...

@app.post(
    "/stories",
    tags=["stories"],
    summary="Create a story (admin)",
    description="Creates a new story linked to a player or club. Requires authentication.",
    response_model=StoryResponse,
    status_code=201,
    responses={
        401: {"model": ErrorDetail, "description": "Not authenticated"},
        404: {"model": ErrorDetail, "description": "Player or club not found"},
        422: {"model": ErrorDetail, "description": "Validation error - must link to player OR club"}
    }
)
def create_story(...):
    ...

# Apply to all other endpoints...
```

#### Step 3: Add OpenAPI Metadata
**Modify: `backend/app/main.py`**

Enhance FastAPI app configuration:
```python
app = FastAPI(
    title="FootballVerse API",
    version="2.0.0",
    description="""
    Football knowledge and storytelling platform API.
    
    ## Features
    - **Players**: Browse and import player data from TheSportsDB
    - **Clubs**: Manage football club information
    - **Stories**: Create and render video stories with narration
    - **Authentication**: JWT-based admin access
    
    ## Authentication
    Protected endpoints require a Bearer token obtained from `/auth/login`.
    Include the token in the Authorization header: `Authorization: Bearer <token>`
    
    ## Parody Notice
    All generated story content is fictional parody for entertainment purposes only.
    """,
    lifespan=lifespan,
    contact={
        "name": "FootballVerse",
        "url": "https://github.com/yourusername/footballverse"
    },
    license_info={
        "name": "MIT"
    }
)
```

### Testing Strategy
1. Visit `http://127.0.0.1:8000/docs`
2. Verify all endpoints visible with descriptions
3. Test "Try it out" functionality
4. Download OpenAPI spec from `/openapi.json`
5. Validate spec with Swagger Editor

---

## Implementation Order

### Phase 1: Alembic (45 min)
1. Initialize Alembic - 10 min
2. Configure env.py and alembic.ini - 10 min
3. Generate initial migration - 5 min
4. Modify startup code - 10 min
5. Test migration - 10 min

### Phase 2: Video Rendering (4 hours)
1. Install dependencies - 5 min
2. Create TTS service - 30 min
3. Create scene generator - 45 min
4. Create video renderer - 60 min
5. Integrate with endpoint - 30 min
6. Test rendering - 30 min
7. Debug and optimize - 40 min

### Phase 3: Frontend (3 hours)
1. Create shared components - 30 min
2. Create custom hooks - 30 min
3. Implement Dashboard - 45 min
4. Implement Story Studio - 60 min
5. Add search debounce - 15 min

### Phase 4: API Docs (1.5 hours)
1. Create response schemas - 30 min
2. Add to endpoints - 45 min
3. Test documentation - 15 min

---

## Commit Strategy

After each phase:
```bash
git add .
git commit -m "feat: <description>"
git push origin main
```

Commit messages:
- Phase 1: `feat: add Alembic database migrations`
- Phase 2: `feat: implement video rendering pipeline with TTS and scene generation`
- Phase 3: `feat: complete frontend UI for Dashboard and Story Studio`
- Phase 4: `feat: enhance API documentation with response models`

---

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| ffmpeg not installed | Add startup check, document installation in README |
| Video rendering slow | Run in background, show progress indicator |
| TTS quality issues | Allow manual narration file upload |
| Frontend state management complex | Use simple hooks, avoid premature optimization |
| Database migration fails | Test on backup first, provide rollback instructions |

---

## Success Criteria

- [ ] All 9 Alembic criteria met
- [ ] All 12 video rendering criteria met
- [ ] All 30 frontend criteria met
- [ ] All 8 API documentation criteria met
- [ ] All existing tests pass
- [ ] Manual testing successful
- [ ] Code pushed to GitHub
- [ ] README updated with new features
