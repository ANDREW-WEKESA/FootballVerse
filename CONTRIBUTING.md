# Contributing to FootballVerse

Thank you for your interest in contributing to FootballVerse! 🎉

## Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/FootballVerse.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make changes** and commit: `git commit -m "feat: your feature"`
5. **Push** to your fork: `git push origin feature/your-feature-name`
6. **Open a Pull Request** on GitHub

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your settings
python migrate.py upgrade
python check_dependencies.py  # Verify setup
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Coding Standards

### Python (Backend)
- Follow PEP 8
- Use type hints where appropriate
- Run `flake8` before committing
- Keep functions small and focused
- Add docstrings to public functions

### JavaScript/React (Frontend)
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful variable names
- Follow existing code style

## Commit Messages

Use semantic commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `chore:` - Maintenance tasks
- `refactor:` - Code restructuring
- `test:` - Adding tests

**Examples:**
```
feat: add player import from TheSportsDB
fix: resolve authentication token expiry issue
docs: update API endpoint documentation
```

## Testing

### Run backend tests:
```bash
cd backend
pytest tests/ -v
```

### Run linting:
```bash
flake8 backend/
```

## Database Migrations

When modifying models in `backend/app/database.py`:

1. Create migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of change"
```

2. Review the generated migration in `alembic/versions/`

3. Test migration:
```bash
python migrate.py upgrade
```

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] Commits use semantic format
- [ ] Tests pass locally
- [ ] Documentation updated (if needed)
- [ ] No merge conflicts with main branch

### PR Description Should Include
- What changes were made
- Why the changes were necessary
- How to test the changes
- Screenshots (if UI changes)
- Related issue number (if applicable)

## What to Contribute

### Good First Issues
- Fix typos in documentation
- Add missing docstrings
- Improve error messages
- Add unit tests
- Update README examples

### Feature Ideas
- Additional player statistics
- New story templates
- Video rendering enhancements
- API endpoint improvements
- Frontend UI components

### Bug Reports
When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Error messages/logs

## Code Review Process

1. Maintainer reviews your PR
2. Feedback provided (if needed)
3. Make requested changes
4. PR approved and merged

## Questions?

- Check existing issues/PRs
- Review documentation in `/docs`
- Open a new issue for discussion

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Welcome newcomers
- Collaborate openly

Thank you for contributing! ⚽🚀
