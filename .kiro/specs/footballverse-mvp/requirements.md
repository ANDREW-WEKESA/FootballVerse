# Requirements Document

## Introduction

FootballVerse is a football knowledge and storytelling platform. The current codebase has a working FastAPI/SQLite backend with player data, season stats, honours, goals, and goal evidence endpoints, plus a React/Vite frontend with player browsing and detail pages. This document covers the features that need to be **built** for the MVP: authentication, PostgreSQL migration, Stories CRUD, Clubs CRUD, Story Studio frontend, Dashboard frontend, video pipeline integration, search/filter, and CI.

All fictional or comedic narrative content produced by Story Studio is treated as parody and separated from the factual football data layer. Media assets must carry source and rights metadata.

---

## Glossary

- **API**: The FootballVerse FastAPI backend service.
- **Admin**: The single authorised administrator user who can create and manage stories.
- **Auth_Service**: The component responsible for issuing, validating, and revoking JWT tokens.
- **Club**: A football club entity with name, country, founding year, stadium, trophies count, logo URL, and description.
- **Dashboard**: The admin-only frontend page that lists all stories with their current status and provides quick actions.
- **JWT**: JSON Web Token — the bearer token used to authorise protected API routes.
- **Migration_Tool**: Alembic, used to manage PostgreSQL schema migrations.
- **Password_Hasher**: The bcrypt-based component that hashes and verifies admin passwords.
- **Player**: An existing football player entity already stored in the database.
- **Render_Pipeline**: The PIL + ffmpeg video rendering pipeline that produces exported video files.
- **Story**: A content item linked to a player or club, with a script, status, media metadata, and optional narration file reference.
- **Story_Status**: The lifecycle state of a Story — one of `draft`, `rendered`, or `published`.
- **Story_Studio**: The admin-only frontend UI for creating and editing stories and triggering the Render_Pipeline.
- **Search_Service**: The component that filters players and clubs by name against the PostgreSQL database.

---

## Requirements

### Requirement 1: Admin Authentication

**User Story:** As an Admin, I want to log in with an email and password, so that Story Studio and Dashboard routes are protected from unauthenticated access.

#### Acceptance Criteria

1. THE Auth_Service SHALL store admin credentials with the password hashed using bcrypt before persisting to the database.
2. WHEN a login request is received with a valid email and matching password, THE Auth_Service SHALL return a signed JWT with an expiry of 24 hours.
3. WHEN a login request is received with an invalid email or incorrect password, THE Auth_Service SHALL return an HTTP 401 response with an error message of "Invalid credentials".
4. WHEN a request is received for a protected route without a valid JWT in the Authorization header, THE API SHALL return an HTTP 401 response.
5. WHEN a request is received for a protected route with an expired JWT, THE API SHALL return an HTTP 401 response.
6. THE Auth_Service SHALL read the JWT signing secret from an environment variable and SHALL NOT hard-code the secret in source files.
7. THE API SHALL expose a `POST /auth/login` endpoint that accepts `email` and `password` fields and returns the JWT on success.

---

### Requirement 2: PostgreSQL Migration

**User Story:** As a developer, I want the database to use PostgreSQL instead of SQLite, so that the application is production-ready and supports concurrent connections.

#### Acceptance Criteria

1. THE API SHALL connect to PostgreSQL using a `DATABASE_URL` environment variable read at startup.
2. THE API SHALL NOT contain any hard-coded database connection strings in source files.
3. THE Migration_Tool SHALL manage all schema changes through versioned migration scripts stored in a `migrations/` directory.
4. WHEN the application starts, THE API SHALL apply any pending migrations automatically before accepting requests.
5. THE Migration_Tool SHALL produce migration scripts that preserve all existing data in the `players`, `player_season_stats`, `player_honours`, and `player_goals` tables.
6. IF the `DATABASE_URL` environment variable is not set at startup, THEN THE API SHALL log a descriptive error message and exit with a non-zero status code.

---

### Requirement 3: Stories CRUD

**User Story:** As an Admin, I want to create, read, update, and delete stories linked to players or clubs, so that I can manage narrative content for the platform.

#### Acceptance Criteria

1. THE API SHALL expose a `POST /stories` endpoint, accessible only to authenticated Admins, that creates a new Story with fields: `title`, `player_id` (optional), `club_id` (optional), `script`, `media_metadata` (JSON object), `narration_file` (optional file path reference), and `status` defaulting to `draft`.
2. WHEN a story creation request is received where neither `player_id` nor `club_id` is provided, THE API SHALL return an HTTP 422 response with a descriptive validation error.
3. WHEN a story creation request is received where the provided `player_id` does not exist in the database, THE API SHALL return an HTTP 404 response.
4. WHEN a story creation request is received where the provided `club_id` does not exist in the database, THE API SHALL return an HTTP 404 response.
5. THE API SHALL expose a `GET /stories` endpoint that returns all stories; unauthenticated requests SHALL receive only stories with `status` equal to `published`.
6. WHEN an authenticated Admin sends a `GET /stories` request, THE API SHALL return stories with all Story_Status values.
7. THE API SHALL expose a `GET /stories/{story_id}` endpoint that returns the story with the given ID; IF the story does not exist, THEN THE API SHALL return an HTTP 404 response.
8. THE API SHALL expose a `PUT /stories/{story_id}` endpoint, accessible only to authenticated Admins, that updates any writable field of the story.
9. WHEN a `PUT /stories/{story_id}` request sets `status` to a value other than `draft`, `rendered`, or `published`, THE API SHALL return an HTTP 422 response.
10. THE API SHALL expose a `DELETE /stories/{story_id}` endpoint, accessible only to authenticated Admins, that permanently removes the story; IF the story does not exist, THEN THE API SHALL return an HTTP 404 response.
11. THE Story SHALL store `source_rights_metadata` as a JSON field to record the origin and licensing information of referenced media assets.

---

### Requirement 4: Clubs CRUD

**User Story:** As an Admin, I want to create, read, update, and delete club records, so that stories can be linked to clubs as well as to individual players.

#### Acceptance Criteria

1. THE API SHALL expose a `POST /clubs` endpoint, accessible only to authenticated Admins, that creates a Club with fields: `name` (required), `country` (required), `founded_year` (optional integer), `stadium` (optional), `trophies` (optional integer, default 0), `logo_url` (optional), and `description` (optional).
2. WHEN a club creation request is received with a missing `name` field, THE API SHALL return an HTTP 422 response.
3. WHEN a club creation request is received with a missing `country` field, THE API SHALL return an HTTP 422 response.
4. THE API SHALL expose a `GET /clubs` endpoint that returns all clubs ordered alphabetically by name.
5. THE API SHALL expose a `GET /clubs/{club_id}` endpoint that returns the club with the given ID; IF the club does not exist, THEN THE API SHALL return an HTTP 404 response.
6. THE API SHALL expose a `PUT /clubs/{club_id}` endpoint, accessible only to authenticated Admins, that updates any writable field of the specified club.
7. THE API SHALL expose a `DELETE /clubs/{club_id}` endpoint, accessible only to authenticated Admins, that permanently removes the club; IF the club does not exist, THEN THE API SHALL return an HTTP 404 response.
8. WHEN a `DELETE /clubs/{club_id}` request is received for a club that has associated stories, THE API SHALL return an HTTP 409 response with a message indicating the club has linked stories.

---

### Requirement 5: Story Studio Frontend

**User Story:** As an Admin, I want a Story Studio page where I can create and edit stories, attach media metadata, trigger a video render, and download the output, so that I can produce storytelling content efficiently.

#### Acceptance Criteria

1. THE Story_Studio SHALL be accessible only to authenticated Admins; WHEN an unauthenticated user navigates to the Story Studio route, THE Story_Studio SHALL redirect the user to the login page.
2. THE Story_Studio SHALL display a form with fields: title, player or club selector, script text area, media metadata input, and narration file reference input.
3. WHEN a user submits a valid story creation form, THE Story_Studio SHALL send a `POST /stories` request and display a success confirmation without requiring a full page reload.
4. WHEN a user submits a story creation form with required fields missing, THE Story_Studio SHALL display inline validation messages next to the relevant fields before submitting to the API.
5. THE Story_Studio SHALL display a "Trigger Render" button on existing stories with `status` equal to `draft`; WHEN the button is clicked, THE Story_Studio SHALL call the render endpoint and update the displayed story status to `rendered` upon a successful response.
6. WHEN a render has completed successfully, THE Story_Studio SHALL display a "Download" link that initiates download of the exported video file.
7. WHILE a render request is in progress, THE Story_Studio SHALL display a loading indicator and disable the "Trigger Render" button.
8. IF the render request returns an error, THEN THE Story_Studio SHALL display a descriptive error message and re-enable the "Trigger Render" button.
9. THE Story_Studio SHALL display clear loading states while story data is being fetched and clear empty states when no stories exist.
10. THE Story_Studio SHALL provide a parody disclaimer notice visible to the Admin when composing story scripts, stating that generated content is fictional and comedic in nature.

---

### Requirement 6: Dashboard Frontend

**User Story:** As an Admin, I want a Dashboard page that lists all stories with their current status and provides quick actions, so that I can manage content at a glance.

#### Acceptance Criteria

1. THE Dashboard SHALL be accessible only to authenticated Admins; WHEN an unauthenticated user navigates to the Dashboard route, THE Dashboard SHALL redirect the user to the login page.
2. THE Dashboard SHALL fetch and display a list of all stories from `GET /stories`, showing for each story: title, linked player or club name, current Story_Status, and creation date.
3. THE Dashboard SHALL provide a quick action button to navigate to the Story_Studio editor for each story in `draft` or `rendered` status.
4. THE Dashboard SHALL provide a quick action button to publish each story in `rendered` status, sending a `PUT /stories/{story_id}` request with `status` set to `published`.
5. THE Dashboard SHALL provide a quick action button to delete each story, with a confirmation prompt before sending the `DELETE /stories/{story_id}` request.
6. WHILE story data is loading, THE Dashboard SHALL display a loading indicator. IF the fetch request fails, THEN THE Dashboard SHALL display an error message with a retry option.
7. WHEN the story list is empty, THE Dashboard SHALL display an empty state message with a link to create the first story in Story_Studio.
8. THE Dashboard SHALL display the Story_Status of each story using a visually distinct label (e.g., different colours per status value).

---

### Requirement 7: Video Pipeline Integration

**User Story:** As an Admin, I want the Story Studio to trigger the video rendering pipeline and produce a downloadable export, so that stories can be published as video content.

#### Acceptance Criteria

1. THE API SHALL expose a `POST /stories/{story_id}/render` endpoint, accessible only to authenticated Admins, that triggers the Render_Pipeline for the given story.
2. WHEN the render is triggered, THE Render_Pipeline SHALL use the story's `script` and `media_metadata` as inputs to generate the video output.
3. WHEN the Render_Pipeline completes successfully, THE API SHALL update the story's `status` to `rendered` and store the output file path in the story record.
4. THE Render_Pipeline SHALL produce an output video file smaller than 40 MB.
5. WHEN the render succeeds, THE API SHALL return the output file URL in the response body so the frontend can offer a download link.
6. IF the Render_Pipeline fails for any reason, THEN THE API SHALL update the story's `status` back to `draft`, log the error, and return an HTTP 500 response with a descriptive error message.
7. THE API SHALL expose a `GET /stories/{story_id}/download` endpoint that serves the rendered video file; IF the story has no rendered output file, THEN THE API SHALL return an HTTP 404 response.

---

### Requirement 8: Search and Filter

**User Story:** As a visitor, I want to search and filter players and clubs by name, so that I can find specific records quickly without scrolling through the full list.

#### Acceptance Criteria

1. THE API SHALL expose a `GET /players?search={query}` endpoint that returns all players whose `full_name` contains the query string, using a case-insensitive match.
2. WHEN the `search` query parameter is absent, THE API SHALL return all players ordered alphabetically by `full_name`.
3. WHEN the `search` query parameter is fewer than 2 characters, THE API SHALL return an HTTP 422 response with a descriptive validation error.
4. THE API SHALL expose a `GET /clubs?search={query}` endpoint that returns all clubs whose `name` contains the query string, using a case-insensitive match.
5. WHEN the `search` query parameter is absent on the clubs endpoint, THE API SHALL return all clubs ordered alphabetically by `name`.
6. THE Search_Service SHALL execute search queries against the PostgreSQL database using parameterised queries to prevent SQL injection.
7. THE PlayersPage frontend component SHALL include a search input field that sends a request to `GET /players?search={query}` on input change with a debounce of 300 milliseconds and displays results inline.
8. WHEN the search input is cleared, THE PlayersPage SHALL restore the full player list without a full page reload.

---

### Requirement 9: Continuous Integration

**User Story:** As a developer, I want a CI pipeline that runs linting and tests on every push, so that regressions are caught before code reaches the main branch.

#### Acceptance Criteria

1. THE CI pipeline SHALL be defined as a GitHub Actions workflow file at `.github/workflows/ci.yml`.
2. WHEN a push event is received on any branch, THE CI pipeline SHALL execute Python linting using flake8 against the `backend/` directory.
3. WHEN a push event is received on any branch, THE CI pipeline SHALL execute the pytest test suite in the `backend/` directory.
4. IF any linting check fails, THEN THE CI pipeline SHALL report the job as failed and SHALL NOT proceed to run tests.
5. IF any test in the pytest suite fails, THEN THE CI pipeline SHALL report the job as failed.
6. THE CI pipeline SHALL install Python dependencies from `backend/requirements.txt` before running lint and test steps.
7. THE CI pipeline SHALL run against Python 3.12 (latest stable available on GitHub Actions runners).

---

### Requirement 10: Environment Configuration

**User Story:** As a developer, I want all secrets and environment-specific values managed through environment variables, so that no credentials are hard-coded in the codebase.

#### Acceptance Criteria

1. THE API SHALL read the following values exclusively from environment variables: `DATABASE_URL`, `JWT_SECRET`, and `ADMIN_EMAIL`.
2. THE API SHALL provide a documented `.env.example` file that lists all required environment variable names without their values.
3. IF any required environment variable is missing at startup, THEN THE API SHALL log a descriptive error identifying the missing variable and exit with a non-zero status code.
4. THE API SHALL ensure the `.env` file is listed in `.gitignore` and SHALL NOT commit credential values to source control.

---

### Requirement 11: API Documentation

**User Story:** As a developer, I want the FastAPI built-in Swagger UI to document all endpoints, so that I can explore and test the API without additional tooling.

#### Acceptance Criteria

1. THE API SHALL serve the Swagger UI at the `/docs` path.
2. WHEN a request is made to `/docs`, THE API SHALL return an HTTP 200 response with the OpenAPI specification rendered as interactive documentation.
3. THE API SHALL include `summary`, `description`, and `response_model` metadata on all new endpoints added as part of this MVP build.
4. THE API SHALL include structured error response schemas for HTTP 401, 404, 409, and 422 responses in the OpenAPI specification.

---

### Requirement 12: Structured Error Handling

**User Story:** As a developer, I want all API errors to return consistent, structured JSON responses, so that the frontend can handle errors predictably.

#### Acceptance Criteria

1. THE API SHALL return all error responses as JSON objects with at minimum a `detail` field containing a human-readable error message.
2. WHEN an unhandled exception occurs, THE API SHALL log the full traceback to the server log and return an HTTP 500 response with a generic `detail` message that does not expose internal stack traces to the client.
3. THE API SHALL use FastAPI `HTTPException` or Pydantic validation errors for all expected error conditions and SHALL NOT return HTML error pages for any route.

---

### Requirement 13: Responsive and Accessible Frontend

**User Story:** As a visitor, I want the frontend to work on desktop and mobile screens and to be usable with a keyboard, so that the platform is accessible to a wide audience.

#### Acceptance Criteria

1. THE Story_Studio and THE Dashboard SHALL be responsive and render correctly at viewport widths from 375px to 1440px.
2. THE Story_Studio and THE Dashboard SHALL display clear loading states while asynchronous requests are in progress.
3. THE Story_Studio and THE Dashboard SHALL display descriptive empty states when lists contain no data.
4. THE Story_Studio and THE Dashboard SHALL display descriptive error states when API requests fail, and SHALL provide a mechanism for the user to retry the failed request.
5. ALL interactive elements in THE Story_Studio and THE Dashboard SHALL be reachable and operable via keyboard navigation.
6. ALL images rendered in THE Story_Studio and THE Dashboard SHALL include descriptive `alt` attributes.
