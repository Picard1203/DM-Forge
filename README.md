# The DM Forge

> A D&D learning platform PWA for aspiring Dungeon Masters — from novice to storyteller.

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 · FastAPI · Beanie ODM · MongoDB Atlas |
| Auth | JWT (python-jose) · passlib · bcrypt |
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS v3 |
| State | Zustand |
| i18n | react-i18next |
| Routing | React Router v6 |
| Dev Infra | Docker Compose · Nginx |

## Getting Started

```bash
# 1. Copy env template and fill in your values
cp .env.example .env

# 2. Start all services
docker-compose up --build

# 3. Open the app
open http://localhost:5173

# 4. API docs
open http://localhost:8000/docs
```

## Project Structure

```
the-dm-forge/
├── backend/          # FastAPI application
│   ├── app/          # Application code (layered architecture)
│   │   ├── models/       # Beanie Documents
│   │   ├── repositories/ # Abstract + MongoDB implementations
│   │   ├── services/     # Business logic
│   │   ├── routers/      # API route handlers
│   │   ├── schemas/      # Pydantic request/response models
│   │   └── utils/        # Security helpers, exceptions
│   ├── curriculum/   # YAML content source of truth
│   └── tests/        # pytest test suite
├── frontend/         # React PWA
│   └── src/
│       ├── api/      # Typed fetch wrappers
│       ├── components/
│       ├── pages/
│       ├── store/    # Zustand stores
│       └── i18n/     # Translations
└── nginx/            # Reverse proxy config
```

## Running Tests

```bash
cd backend
pytest tests/ -v
```
