# AGENTS.md — Lobby

## What this is

A FastAPI backend that proxies a Jellyfin media server. Serves a static SPA (`static/index.html`). No database, no async workers.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
```

Or use the helper script:

## Config

All via env (`.env` file loaded automatically in dev):

| Env | Default | Required |
|---|---|---|
| `JELLYFIN_URL` | `http://localhost:8096` | y |
| `JELLYFIN_API_KEY` | `""` | y |
| `LOBBY_PORT` | `8888` | for the lobby.sh script |

## Endpoints

- `GET /api/movies` — movies from Jellyfin
- `GET /api/series` — series from Jellyfin
- `GET /api/proxy/{item_id}/{img_type}` — image proxy (types: `poster`, `backdrop`); hides API key from browser; cache 24h
- `GET /` — serves `static/index.html`
- Static files at `/` mount from `static/` directory

## Developer notes

- No tests, linting, typecheck, or formatter config exists. No CI.
- The app is useless without a reachable Jellyfin instance (set `JELLYFIN_URL` + `JELLYFIN_API_KEY`).
- Image proxy is the only endpoint that intentionally hides credentials — the API key never reaches the browser.
- `docs_url=None, redoc_url=None` — no auto-generated API docs.
- DESIGN.md references a Next.js/React/Tailwind UI that does not match the current FastAPI+static-HTML stack; treat it as aspirational/outdated.
- Requirements are pinned (`fastapi==0.115.6`, `uvicorn[standard]==0.32.1`, `httpx==0.28.1`).
