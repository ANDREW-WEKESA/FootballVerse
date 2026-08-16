# FootballVerse Completion - Implementation Tasks

## Priority 1: Alembic Database Migrations (45 min)

### Task 1.1: Initialize Alembic
- [ ] Run `alembic init alembic` in backend directory
- [ ] Verify `alembic/` directory and `alembic.ini` created
- [ ] Verify `alembic/env.py` exists

### Task 1.2: Configure Alembic
- [ ] Modify `alembic.ini` to remove hardcoded database URL
- [ ] Update `alembic/env.py` to import `Base` from `app.database`
- [ ] Update `alembic/env.py` to set `target_metadata = Base.metadata`
- [ ] Update `alembic/env.py` to read `DATABASE_URL` from environment
- [ ] Test configuration: `alembic current`

### Task 1.3: Generate Initial Migration
- [ ] Run `alembic revision --autogenerate -m "Initial schema"`
- [ ] Review generated migration file
- [ ] Verify all 8 tables included (users, clubs, players, stories, player_season_stats, player_honours, player_goals)
- [ ] Test migration: `alembic upgrade head` on backup database

### Task 1.4: Integrate with Application Startup
- [ ] Remove `Base.metadata.create_all(engine)` from `app/main.py`
- [ ] Add Alembic upgrade logic to `lifespan` function
- [ ] Add error handling for migration failures
- [ ] Add logging for migration success/failure
- [ ] Test startup with existing database

### Task 1.5: Test & Verify
- [ ] Backup current `footballverse.db`
- [ ] Test fresh database migration
- [ ] Test existing database migration (no data loss)
- [ ] Run pytest suite to ensure no regressions
- [ ] Verify admin user created on startup
- [ ] Commit and push: `feat: add Alembic database migrations`

---

## Priority 2: Video Rendering Pipeline (4 hours)

### Task 2.1: Install Dependencies
- [ ] Add `Pillow==11.1.0` to `requirements.txt`
- [ ] Add `gTTS==2.5.4` to `requirements.txt`
- [ ] Add `moviepy==1.0.3` to `requirements.txt`
- [ ] Run `pip install -r requirements.txt`
- [ ] Verify ffmpeg installed on system (run `ffmpeg -version`)

### Task 2.2: Create TTS Service
- [ ] Create `backend/app/services/tts_service.py`
- [ ] Implement `TTSService` class
- [ ] Implement `generate_narration()` method
- [ ] Implement `get_audio_duration()` method
- [ ] Create `backend/temp/` directory for temporary files
- [ ] Test TTS generation with sample text

### Task 2.3: Create Scene Generator
- [ ] Create `backend/app/services/scene_generator.py`
- [ ] Implement `SceneGenerator` class
- [ ] Implement `create_title_card()` method
- [ ] Implement `create_text_scene()` method
- [ ] Implement `create_parody_disclaimer()` method
- [ ] Test image generation (verify PNG files created)

### Task 2.4: Create Video Renderer
- [ ] Create `backend/app/services/video_renderer.py`
- [ ] Implement `VideoRenderer` class
- [ ] Implement `render_story()` method (orchestrate TTS + scenes + video)
- [ ] Implement `_cleanup_temp_files()` method
- [ ] Create `backend/static/videos/` directory
- [ ] Test video rendering end-to-end

### Task 2.5: Integrate with API Endpoint
- [ ] Import `VideoRenderer` in `app/main.py`
- [ ] Replace placeholder render endpoint logic
- [ ] Add async execution with thread pool
- [ ] Update story status on success/failure
- [ ] Add logging for render operations
- [ ] Test via API: `POST /stories/{id}/render`

### Task 2.6: Test & Verify
- [ ] Create test story with simple script
- [ ] Trigger render via API
- [ ] Verify MP4 file created in `static/videos/`
- [ ] Verify video plays in browser
- [ ] Verify file size < 40MB
- [ ] Test error handling (invalid story, empty script)
- [ ] Verify download endpoint works
- [ ] Commit and push: `feat: implement video rendering pipeline with TTS and scene generation`

---

## Priority 3: Frontend UI Completion (3 hours)

### Task 3.1: Create Shared Components
- [ ] Create `frontend/src/components/LoadingSpinner.jsx`
- [ ] Create `frontend/src/components/ErrorMessage.jsx`
- [ ] Create `frontend/src/components/StatusBadge.jsx`
- [ ] Add CSS styles for components in `style.css`

### Task 3.2: Create Custom Hooks
- [ ] Create `frontend/src/hooks/useDebounce.js`
- [ ] Create `frontend/src/hooks/useStories.js`
- [ ] Test debounce hook with console.log

### Task 3.3: Implement Dashboard Page
- [ ] Update `frontend/src/pages/DashboardPage.jsx`
- [ ] Add stories table with all columns
- [ ] Add status badges with color coding
- [ ] Add Edit/Publish/Delete actions
- [ ] Add delete confirmation dialog
- [ ] Add "Create New Story" button
- [ ] Add loading state
- [ ] Add error state with retry
- [ ] Add empty state
- [ ] Test all functionality

### Task 3.4: Implement Story Studio Page
- [ ] Update `frontend/src/pages/StoryStudioPage.jsx`
- [ ] Add form with all fields (title, player, club, script)
- [ ] Add player/club dropdown population
- [ ] Add form validation
- [ ] Add parody disclaimer display
- [ ] Add "Trigger Render" button for draft stories
- [ ] Add "Download" button for rendered stories
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test create and edit flows

### Task 3.5: Enhance Players Page
- [ ] Update `frontend/src/pages/PlayersPage.jsx`
- [ ] Add search input with debounce (300ms)
- [ ] Add loading indicator during search
- [ ] Test search functionality
- [ ] Verify responsiveness

### Task 3.6: Add Responsive Styles
- [ ] Add CSS for Dashboard table (mobile-friendly)
- [ ] Add CSS for Story Studio form
- [ ] Add CSS for loading/error states
- [ ] Test on mobile (375px), tablet (768px), desktop (1024px+)
- [ ] Verify keyboard navigation (Tab, Enter)

### Task 3.7: Test & Verify
- [ ] Manual test all pages in browser
- [ ] Test create story flow
- [ ] Test edit story flow
- [ ] Test render trigger
- [ ] Test publish story
- [ ] Test delete story with confirmation
- [ ] Test search with debounce
- [ ] Test loading/error states (throttle network in DevTools)
- [ ] Commit and push: `feat: complete frontend UI for Dashboard and Story Studio`

---

## Priority 4: API Documentation Enhancement (1.5 hours)

### Task 4.1: Create Response Schemas
- [ ] Create `backend/app/schemas.py`
- [ ] Define `PlayerResponse` model
- [ ] Define `ClubResponse` model
- [ ] Define `StoryResponse` model
- [ ] Define `TokenResponse` model
- [ ] Define `ErrorDetail` model
- [ ] Define `ValidationError` model

### Task 4.2: Add Response Models to Endpoints
- [ ] Import schemas in `app/main.py`
- [ ] Add `response_model` to auth endpoints
- [ ] Add `response_model` to player endpoints
- [ ] Add `response_model` to club endpoints
- [ ] Add `response_model` to story endpoints
- [ ] Add `responses` dict with error schemas to all endpoints

### Task 4.3: Enhance OpenAPI Metadata
- [ ] Update FastAPI app configuration with detailed description
- [ ] Add contact information
- [ ] Add license information
- [ ] Add authentication documentation

### Task 4.4: Test & Verify
- [ ] Visit `/docs` in browser
- [ ] Verify all endpoints documented
- [ ] Verify "Try it out" works for sample endpoints
- [ ] Download `/openapi.json` and validate
- [ ] Verify error responses documented
- [ ] Commit and push: `feat: enhance API documentation with response models`

---

## Final Tasks

### Task 5.1: Update README
- [ ] Document new features (Alembic, video rendering)
- [ ] Add ffmpeg installation instructions
- [ ] Add video rendering usage guide
- [ ] Update setup instructions
- [ ] Add troubleshooting section

### Task 5.2: Final Testing
- [ ] Run full test suite: `pytest`
- [ ] Test complete user flow end-to-end
- [ ] Verify no regressions
- [ ] Test on fresh database

### Task 5.3: Final Commit & Push
- [ ] Review all changes
- [ ] Final commit: `docs: update README with new features`
- [ ] Push all commits to GitHub
- [ ] Verify GitHub Actions CI passes

---

## Task Summary

| Priority | Task Count | Estimated Time |
|---|---|---|
| 1. Alembic Migrations | 5 tasks | 45 min |
| 2. Video Rendering | 6 tasks | 4 hours |
| 3. Frontend UI | 7 tasks | 3 hours |
| 4. API Documentation | 4 tasks | 1.5 hours |
| Final Tasks | 3 tasks | 30 min |
| **Total** | **25 tasks** | **9.5 hours** |

---

## Progress Tracking

Use this checklist to track overall progress:

- [ ] Priority 1: Alembic Migrations (5/5 tasks)
- [ ] Priority 2: Video Rendering (6/6 tasks)
- [ ] Priority 3: Frontend UI (7/7 tasks)
- [ ] Priority 4: API Documentation (4/4 tasks)
- [ ] Final Tasks (3/3 tasks)

**Overall Progress: 0/25 tasks complete (0%)**
