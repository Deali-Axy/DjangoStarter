# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DjangoStarter v3 is an AI-native full-stack Django scaffolding framework for rapid web application development. It combines Django 5 with Django-Ninja (type-safe APIs), HTMX/Alpine.js, and TailwindCSS, with built-in authentication, security, code generation, and Docker support.

**Target use cases:** Personal/indie product MVPs, internal enterprise tools, data dashboards, and AI Agent/assistant backends with management interfaces.

## Essential Commands

### Setup
```bash
# Install Python dependencies
pdm install

# Install frontend dependencies
pnpm install

# Run database migrations
python manage.py migrate

# Copy frontend assets
gulp move
```

### Development
```bash
# Django dev server (WSGI)
python manage.py runserver

# Granian ASGI server (better performance)
pdm run granian-asgi

# Watch TailwindCSS changes
npm run tailwind:watch

# Build optimized assets
npm run build:assets
```

### Code Generation
```bash
# Generate CRUD + tests + admin for an app
python manage.py autocode app_name "Display Name"

# Generate specific models only
python manage.py autocode blog "Blog" --models post category

# Generate seed data for an app
python manage.py seed app_label 10
```

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Testing
```bash
# Django tests
python manage.py test

# Pytest (preferred)
pytest
```

### Docker
```bash
# Build and run
docker compose up --build

# Restart services
docker compose down && docker compose up -d
```

## Architecture

### Core Framework Components

**ModelExt Base Class** (`src/django_starter/db/models.py`):
All models inherit from `ModelExt`, which provides:
- Soft delete via `is_deleted` field
- Automatic timestamps (`created_time`, `updated_time`)
- Custom manager that filters out deleted objects

**Django-Ninja API Organization**:
- APIs organized per app in `apps/[app]/apis/`
- Automatic CRUD generation via `autocode` command
- Type-safe Pydantic schemas
- Auto-generated OpenAPI docs at `/api/docs`

**Split Settings** (`src/config/settings/`):
- Base settings in `components/`
- Environment-specific overrides in `environments/`
- Docker-aware configuration detection

### URL Prefix Support

Environment variable `URL_PREFIX` enables subdirectory deployment:
- Automatically prefixes all URLs, static files, and media paths
- Nginx proxy-ready configuration
- Example: `URL_PREFIX=djangostarter` makes app accessible at `/djangostarter/`

### Directory Structure
```
src/
├── apps/                    # Business applications
│   ├── account/            # Authentication system
│   └── demo/               # Demo app (reference implementation)
├── config/                 # Django configuration
│   ├── settings/           # Split settings (django-split-settings)
│   │   ├── components/    # Config components (cache, auth, security, etc.)
│   │   └── environments/  # Environment-specific configs
│   ├── urls.py            # Main URL config
│   ├── apis.py            # NinjaAPI initialization - register routers here
│   └── wsgi.py/asgi.py    # Entry points
├── django_starter/         # Core framework code
│   ├── contrib/           # Built-in components (code_generator, admin, monitoring)
│   ├── db/models.py       # ModelExt base class
│   ├── http/              # Response handling
│   └── middleware/        # Security middleware
├── static/                # Static files
└── templates/             # Jinja2 templates
```

### Application Development Pattern

When creating a new app:
1. Create app: `cd apps && django-admin startapp app_name`
2. Add to `INSTALLED_APPS` in `src/config/settings/components/django_starter.py`
3. Define models in `apps/app_name/models.py` (inherit from `ModelExt`)
4. Run `python manage.py autocode app_name "Display Name"` to generate CRUD, tests, admin
5. Register router in `src/config/apis.py`: `api.add_router('app_name', router)`
6. Run migrations

### Frontend Stack

- **HTMX 1.9.12**: AJAX without heavy JavaScript
- **Alpine.js 3.14.8**: Minimal reactive capabilities
- **TailwindCSS 3.4.6**: Utility-first styling
- **Flowbite 2.4.1**: Component library
- **Jinja2**: Template engine (Django templates compatible)

## Configuration

### Key Configuration Files

- `src/config/settings/components/django_starter.py`: Project info, admin, auth, OAuth2
- `src/config/settings/components/common.py`: URL_PREFIX, security settings
- `src/config/settings/components/caches.py`: Redis/cache configuration
- `src/config/settings/components/authentication.py`: Authentication settings
- `.env`: Environment variables for Docker deployment

### Environment Variables (Docker)
- `APP_PORT`: External port (default: 9876)
- `APP_INTERNAL_PORT`: Internal container port (default: 8000)
- `URL_PREFIX`: Subdirectory prefix (optional)
- `DEBUG`: Debug mode flag

## Development Guidelines (from .cursor/rules)

- Follow PEP 8 with type hints and Google-style docstrings
- All models inherit from `ModelExt`
- Use Django-Ninja for APIs with Pydantic schemas
- Frontend: HTMX + Alpine.js, avoid heavy JavaScript frameworks
- Use select_related/prefetch_related for query optimization
- Redis caching via django-redis

### Code Standards

- Use snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- Add `verbose_name` to all model fields
- Define `__str__` and `Meta` classes for models
- All functions/classes must have docstrings
- Test new functionality appropriately

## Deployment

### Docker Multi-Stage Build

Production-ready Dockerfile with:
- Python dependencies build stage
- Node.js dependencies and frontend build stage
- Static file compilation
- Minimal production image

### Application Servers

- Default: **Daphne** (ASGI)
- Alternative: **Granian** (Rust-based, supports ASGI/WSGI, HTTP/2, WebSocket)
  - Dev: `pdm run granian-asgi` / `pdm run granian-http2`
  - Docker: Override command in `docker-compose.yml`

### Docker Compose Services
- `app`: Main Django application
- `redis`: Redis cache server
- Named volumes for static files and database

## AI-Ready Features

The framework is designed for LLM integration with reserved extension points:
- Function calling/Tools support
- RAG with vector search (pgvector planned)
- Streaming responses (SSE/WebSocket planned)

## Important Notes

- **autocode command overwrites existing files** in the target app
- Redis is required for rate limiting and security features
- PostgreSQL is recommended for production (SQLite is default for dev)
- URL_PREFIX affects all paths including admin, static, and media files
