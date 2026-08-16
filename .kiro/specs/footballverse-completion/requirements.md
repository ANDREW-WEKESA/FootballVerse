# FootballVerse Completion - Requirements

## Overview

This spec covers the completion of four critical priorities for FootballVerse to achieve production-ready status:

1. **Alembic Database Migrations** - Replace `create_all()` with proper schema versioning
2. **Video Rendering Pipeline** - Implement the actual rendering logic for stories
3. **Frontend UI Completion** - Verify and complete Story Studio and Dashboard pages
4. **API Documentation Enhancement** - Add comprehensive OpenAPI schemas

## Priority 1: Alembic Database Migrations

### Background
Currently, the application uses `Base.metadata.create_all(engine)` which creates tables but doesn't support schema evolution. Alembic is already in `requirements.txt` but not configured.

### User Stories

**As a developer**, I want database schema changes to be version-controlled through Alembic migrations, so that schema evolution is predictable and reversible.

**As a DevOps engineer**, I want migrations to run automatically on application startup, so that deployments don't require manual database management.

### Acceptance Criteria

| # | Criterion | Priority |
|---|---|---|
| 1.1 | Alembic is initialized with `migrations/` directory and `alembic.ini` | Must Have |
| 1.2 | Initial migration captures current schema (all 8 tables) | Must Have |
| 1.3 | `Base.metadata.create_all()` is replaced with migration runner in startup | Must Have |
| 1.4 | Migrations run automatically on app startup before serving requests | Must Have |
| 1.5 | Missing `DATABASE_URL` logs error and exits non-zero | Must Have |
| 1.6 | Migration failures log detailed error and exit non-zero | Must Have |
| 1.7 | `alembic.ini` uses `DATABASE_URL` from environment (not hardcoded) | Must Have |
| 1.8 | All existing tests still pass after migration | Must Have |
| 1.9 | Migration preserves existing data in `footballverse.db` | Must Have |

### Out of Scope
- Migration rollback UI/tooling (manual `alembic downgrade` is sufficient)
- Migration conflict resolution (single-developer project)
- Migration performance optimization

---

## Priority 2: Video Rendering Pipeline

### Background
The `/stories/{id}/render` endpoint currently returns a placeholder message. We need to implement the actual video generation pipeline using the story script and media metadata.

### User Stories

**As an admin**, I want to trigger video rendering for a draft story, so that I can generate publishable video content from the script.

**As an admin**, I want the rendered video to include narration from the script text, so that the story is narrated automatically.

**As an admin**, I want the rendered video to be under 40MB, so that it's suitable for social media sharing.

### Acceptance Criteria

| # | Criterion | Priority |
|---|---|---|
| 2.1 | `POST /stories/{id}/render` generates actual video file from script | Must Have |
| 2.2 | Rendering updates story status from `draft` to `rendered` on success | Must Have |
| 2.3 | Rendering saves output path to `render_output_path` field | Must Have |
| 2.4 | Video includes text-to-speech narration from script content | Must Have |
| 2.5 | Video includes visual scenes (at minimum: title cards with text) | Must Have |
| 2.6 | Output format is MP4, compatible with web browsers | Must Have |
| 2.7 | Video resolution is 1920x1080 (1080p) or 1280x720 (720p) | Should Have |
| 2.8 | Rendered video file size < 40 MB | Should Have |
| 2.9 | Rendering failures revert status to `draft`, log error, return 500 | Must Have |
| 2.10 | `GET /stories/{id}/download` returns actual video file URL | Must Have |
| 2.11 | Rendering runs asynchronously (doesn't block the API endpoint) | Should Have |
| 2.12 | Progress/status tracking for long-running renders | Nice to Have |

### Technical Constraints
- Use ffmpeg for video compilation
- Use Python TTS library (gTTS, pyttsx3, or similar) for narration
- Use PIL/Pillow for image generation (title cards, text overlays)
- Store output in `backend/static/videos/` directory
- Parody disclaimer must be visible in generated content

### Out of Scope
- Advanced animation/cartoon generation (AI models)
- Custom voice selection/cloning
- Video editing UI (timeline, transitions)
- Real-time preview during editing
- Cloud storage integration (S3, etc.)

---

## Priority 3: Frontend UI Completion

### Background
The following pages exist but need verification and potential completion:
- `StoryStudioPage.jsx` - Story creation/editing interface
- `DashboardPage.jsx` - Admin story management
- `PlayersPage.jsx` - Public player browsing
- `PlayerDetailPage.jsx` - Player profile with timeline

### User Stories

**As an admin**, I want a complete Story Studio interface, so that I can create and edit stories with all necessary fields.

**As an admin**, I want a functional Dashboard, so that I can manage all stories from a single view.

**As a visitor**, I want a responsive player browsing experience, so that I can explore football history on any device.

### Acceptance Criteria

#### Story Studio Page

| # | Criterion | Priority |
|---|---|---|
| 3.1 | Form includes all fields: title, player/club selector, script textarea, narration file upload | Must Have |
| 3.2 | Player/club selector fetches from `/players` and `/clubs` endpoints | Must Have |
| 3.3 | Form validation: title required, either player OR club required | Must Have |
| 3.4 | Submit creates story via `POST /stories` | Must Have |
| 3.5 | Success shows confirmation message and redirects to Dashboard | Must Have |
| 3.6 | Editing existing story pre-populates all fields from `GET /stories/{id}` | Must Have |
| 3.7 | "Trigger Render" button visible only for `draft` stories | Must Have |
| 3.8 | Render trigger calls `POST /stories/{id}/render` | Must Have |
| 3.9 | "Download" button visible only for `rendered` stories | Must Have |
| 3.10 | Parody disclaimer text visible when editing script | Must Have |
| 3.11 | Loading states during save/render operations | Should Have |
| 3.12 | Error messages displayed for API failures | Must Have |

#### Dashboard Page

| # | Criterion | Priority |
|---|---|---|
| 3.13 | Lists all stories with: title, linked entity, status, created date | Must Have |
| 3.14 | Status displayed with color-coded badge (draft=yellow, rendered=blue, published=green) | Should Have |
| 3.15 | "Edit" button navigates to Story Studio for each story | Must Have |
| 3.16 | "Publish" button for `rendered` stories, updates status to `published` | Must Have |
| 3.17 | "Delete" button with confirmation dialog | Must Have |
| 3.18 | Delete calls `DELETE /stories/{id}` | Must Have |
| 3.19 | "Create New Story" button navigates to Story Studio | Must Have |
| 3.20 | Empty state when no stories exist | Should Have |
| 3.21 | Loading state while fetching stories | Should Have |
| 3.22 | Error state with retry button on fetch failure | Should Have |

#### Players & Player Detail Pages

| # | Criterion | Priority |
|---|---|---|
| 3.23 | PlayersPage: Search input with 300ms debounce | Should Have |
| 3.24 | PlayersPage: Grid/list of player cards with name, nationality, image | Must Have |
| 3.25 | PlayersPage: Clicking player navigates to detail page | Must Have |
| 3.26 | PlayerDetailPage: Displays player stats (goals, appearances, trophies) | Must Have |
| 3.27 | PlayerDetailPage: Timeline view of career (seasons, teams, honours) | Must Have |
| 3.28 | PlayerDetailPage: Story events visualization | Should Have |
| 3.29 | All pages responsive 375px-1440px | Should Have |
| 3.30 | All interactive elements keyboard accessible | Should Have |

### Out of Scope
- WYSIWYG script editor with rich text
- Drag-and-drop media upload
- Real-time collaboration
- Advanced search filters (position, nationality, etc.)
- Player comparison features

---

## Priority 4: API Documentation Enhancement

### Background
FastAPI provides automatic OpenAPI docs at `/docs`, but our endpoints lack detailed response models and structured error schemas.

### User Stories

**As a frontend developer**, I want comprehensive API documentation with response examples, so that I can integrate with the backend without guessing payloads.

**As a QA engineer**, I want documented error responses, so that I can test error handling thoroughly.

### Acceptance Criteria

| # | Criterion | Priority |
|---|---|---|
| 4.1 | All endpoints have `summary` parameter | Must Have |
| 4.2 | All endpoints have `description` parameter explaining behavior | Should Have |
| 4.3 | All endpoints define `response_model` for 200 responses | Must Have |
| 4.4 | All endpoints document error responses: 401, 404, 409, 422 as applicable | Should Have |
| 4.5 | Error responses include example `detail` messages | Should Have |
| 4.6 | Pydantic models for all response shapes (PlayerResponse, StoryResponse, etc.) | Must Have |
| 4.7 | `/docs` renders correctly with all documented schemas | Must Have |
| 4.8 | OpenAPI spec downloadable via `/openapi.json` | Must Have |

### Out of Scope
- External documentation site (Swagger UI at `/docs` is sufficient)
- API versioning (v2, v3 endpoints)
- Rate limiting documentation
- Authentication flow diagrams

---

## Cross-Cutting Requirements

### Performance
- API endpoints respond within 200ms (excluding rendering)
- Frontend pages load within 2 seconds on 3G connection
- Video rendering completes within 60 seconds for 2-minute stories

### Security
- All admin endpoints require valid JWT token
- Uploaded files validated (type, size)
- SQL injection prevented via ORM (existing)
- XSS prevented via React (existing)

### Compatibility
- Backend: Python 3.11+
- Frontend: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- Database: PostgreSQL 14+ OR SQLite 3.35+ (development)

### Observability
- All errors logged with stack traces
- Migration operations logged (start, success, failure)
- Render operations logged with duration and output file size

---

## Success Metrics

| Metric | Target |
|---|---|
| Alembic migrations initialized and working | 100% |
| Video rendering produces valid MP4 files | 100% |
| Frontend pages fully implemented per acceptance criteria | ≥ 90% |
| API endpoints with response_model defined | ≥ 80% |
| All existing tests passing | 100% |
| No regression in functionality | 100% |

---

## Dependencies & Assumptions

### Dependencies
- Alembic 1.19.1 (already in requirements.txt)
- ffmpeg (must be installed on system)
- PIL/Pillow (add to requirements.txt)
- gTTS or pyttsx3 for TTS (add to requirements.txt)

### Assumptions
- Single admin user (no multi-user auth complexity)
- Stories are text-based (no video upload/editing)
- English language only for narration
- Development on Windows (user's OS)
- Git repository already initialized

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| ffmpeg not installed on user's system | High | Document installation, add startup check |
| TTS quality poor/robotic | Medium | Allow narration file upload as alternative |
| Video rendering too slow | Medium | Implement async rendering, show progress |
| Alembic migration fails on existing DB | High | Test migration on backup DB first |
| Frontend complexity exceeds estimate | Medium | Prioritize must-haves, defer nice-to-haves |

---

## Timeline Estimate

| Priority | Estimated Time |
|---|---|
| 1. Alembic Migrations | 30-45 minutes |
| 2. Video Rendering Pipeline | 3-4 hours |
| 3. Frontend UI Completion | 2-3 hours |
| 4. API Documentation | 1-2 hours |
| **Total** | **6.5-9.5 hours** |

---

## Next Steps

After requirements approval:
1. Create detailed design document
2. Break down into implementation tasks
3. Implement in order: Priority 1 → 2 → 3 → 4
4. Test each priority before moving to next
5. Commit and push to GitHub after each priority completion
