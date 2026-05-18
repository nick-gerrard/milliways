# Milliways

A personal recipe management app built to replace Notion as a recipe store. Notion treats recipes as dumb documents — slow to open, impossible to compare, useless for grocery lists. Milliways fixes this by modeling recipes as structured data.

## What it does

- **Browse and search recipes** — fast, filterable by tag, no waiting for PDFs to load
- **Cook mode** — clean, mobile-friendly view optimized for use in the kitchen
- **Shopping list** — select multiple recipes, get a single deduplicated ingredient list
- **Manual entry** — mobile-friendly form for creating recipes from scratch (cocktails, family recipes, etc.)
- **AI ingestion** — drop a PDF or screenshot into a watched folder on your desktop; the ingestion agent parses it with a local LLM and syncs it to the server automatically

## Architecture

This is a two-part system:

### Server (runs on Linode)
- **Backend:** FastAPI + SQLModel + PostgreSQL
- **Frontend:** SvelteKit
- Lean — no AI dependencies. Serves the web app and exposes the API.

### Desktop ingestion agent (runs on your machine)
- Watches a local folder (e.g. `~/recipe-inbox`) for new PDFs and screenshots
- Parses them using local [ollama](https://ollama.com) — no API costs
- POSTs structured recipe data to the server API
- Runs whenever your desktop is on and idle

This split keeps the server cheap and the AI heavy lifting local. If the app ever grows beyond personal use, swapping ollama for a cloud model (Claude Haiku, etc.) is a single interface change.

## Development setup

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- Node.js + npm
- tmux

### Install dependencies

```bash
uv sync
cd frontend && npm install
```

### Database

Migrations live in `backend/alembic/`. Run from `backend/`:

```bash
cd backend
uv run alembic upgrade head
```

By default uses SQLite (`milliways.db`). Set `DATABASE_URL` to a Postgres connection string for production.

### Run the dev servers

```bash
./start.sh
```

Opens a new tmux window with two panes — FastAPI on port 8000 (left) and SvelteKit on port 5173 (right). The frontend is served with `--host` so it's accessible from any device on your local network.

## Project structure

```
milliways/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app
│   │   ├── models.py      # SQLModel data models
│   │   └── database.py    # Engine and session setup
│   └── alembic/           # Database migrations
├── frontend/              # SvelteKit app
├── agent/                 # Desktop ingestion agent (coming soon)
├── start.sh               # Dev server launcher
└── pyproject.toml         # Python dependencies (server only)
```

## Roadmap

- [x] Data models and migrations
- [x] Dev tooling (start.sh, pyrightconfig, gitignore)
- [ ] Core API routes (recipes, tags, shopping list)
- [ ] Recipe list and detail views
- [ ] Cook mode (mobile-optimized)
- [ ] Shopping list UI
- [ ] Recipe create/edit form (mobile-friendly)
- [ ] Desktop ingestion agent (folder watcher + ollama parser)
- [ ] Notion migration script (one-time)
- [ ] Auth (Google OAuth) and multi-user support
