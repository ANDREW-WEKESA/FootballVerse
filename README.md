# FootballVerse

Football stories brought to life through data-driven storytelling and animated content generation.

## Features

- 🏆 **Football History**: Import and manage player data from TheSportsDB
- 📊 **Career Timelines**: Visualize player career progression with season stats and honours
- 🎬 **Story Studio**: Create and manage football stories (admin)
- 🎨 **Animated Storytelling**: Video generation with narration (in development)
- 📹 **Shorts Creator**: Produce short-form football content
- 📱 **Creator Dashboard**: Manage all stories and content from one place
- 🔐 **Admin Authentication**: Secure JWT-based authentication
- 🗄️ **Database Migrations**: Alembic-powered schema management

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with SQLite (dev) / PostgreSQL (prod) support  
- **Alembic** - Database migration management
- **JWT** - Secure authentication with python-jose
- **bcrypt** - Password hashing via passlib
- **TheSportsDB API** - External football data source

### Frontend
- **React** - UI library with Vite build tool
- **React Router** - Client-side routing
- **Context API** - State management

### Video Rendering (Planned)
- **Pillow** - Image generation for title cards
- **gTTS** - Text-to-speech for narration
- **moviepy** - Video compilation and export

## Project Structure

```
FootballVerse/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── auth.py           # Authentication logic
│   │   ├── database.py       # Database models
│   │   └── services/         # External API integrations
│   ├── alembic/              # Database migrations
│   ├── tests/                # Test suite
│   ├── migrate.py            # Migration helper script
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment configuration
├── frontend/
│   ├── src/
│   │   ├── pages/            # React page components
│   │   ├── components/       # Reusable React components
│   │   └── context/          # React context providers
│   └── package.json          # Node dependencies
└── .kiro/specs/              # Development specifications
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- ffmpeg (for video rendering)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `DATABASE_URL` - Database connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `ADMIN_EMAIL` - Admin user email
- `ADMIN_PASSWORD` - Admin user password

5. Run database migrations:
```bash
python migrate.py upgrade
```

6. Start the backend server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API will be available at http://127.0.0.1:8000  
API Documentation at http://127.0.0.1:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

Frontend will be available at http://localhost:5173

## API Endpoints

### Public
- `GET /` - Health check
- `GET /players` - List all players (with optional search)
- `GET /players/{id}` - Get player details
- `GET /players/{id}/timeline` - Player career timeline
- `GET /players/{id}/story` - Player story events
- `GET /players/{id}/goals` - Player goals with evidence
- `GET /clubs` - List all clubs (with optional search)
- `GET /stories` - List published stories (or all if authenticated)
- `POST /auth/login` - Admin login

### Protected (Admin Only)
- `POST /players/import` - Import player from TheSportsDB
- `POST /stories` - Create a new story
- `PUT /stories/{id}` - Update a story
- `DELETE /stories/{id}` - Delete a story
- `POST /stories/{id}/render` - Trigger video rendering
- `POST /clubs` - Create a club
- `PUT /clubs/{id}` - Update a club
- `DELETE /clubs/{id}` - Delete a club
- `POST /players/{id}/goals` - Add a goal
- `DELETE /players/{id}/goals/{goal_id}` - Delete a goal
- `PUT /players/{id}/goals/{goal_id}/evidence` - Update goal evidence

## Database Management

FootballVerse uses Alembic for database schema versioning.

### Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
python migrate.py upgrade
```

### View migration history:
```bash
python migrate.py history
```

### View current revision:
```bash
python migrate.py current
```

## Development

### Running Tests
```bash
cd backend
pytest tests/ -v
```

### Code Quality
```bash
# Linting
flake8 backend/

# Type checking (if configured)
mypy backend/
```

### CI/CD
GitHub Actions workflow runs on every push:
- Linting with flake8
- Test suite with pytest
- Python 3.12 compatibility check

## Roadmap

### Version 0.2 (In Progress)
- [x] Alembic database migrations
- [ ] Video rendering pipeline
  - [ ] TTS narration generation
  - [ ] Scene/title card generation
  - [ ] Video compilation with moviepy
- [ ] Complete frontend UI
  - [ ] Story Studio page
  - [ ] Dashboard page
  - [ ] Player detail page enhancements
- [ ] Enhanced API documentation

### Version 0.3 (Planned)
- PostgreSQL production deployment
- Advanced video rendering features
- Media asset management
- Source rights tracking
- Batch story generation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Football data provided by [TheSportsDB](https://www.thesportsdb.com/)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [React](https://react.dev/) and [Vite](https://vitejs.dev/)

---

**Version 0.1.1** - Database migrations and video rendering prep  
Last updated: August 16, 2026
