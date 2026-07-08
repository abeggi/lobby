# AGENTS.md — Lobby

## What this is

A FastAPI backend that proxies a Jellyfin media server. Serves a static SPA (`static/index.html`). No database, no async workers. Single-file Python backend (`main.py`).

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080 --env-file .env
```

Or use the helper script (`./lobby.sh start|stop|restart|status`) which sources `.env` automatically.

## Systemd service

`sudo ./lobby-service.sh install|uninstall|start|stop|restart|enable|disable|status`

## Config

All via env vars:

| Env | Default | Required |
|---|---|---|
| `JELLYFIN_URL` | `http://localhost:8096` | y |
| `JELLYFIN_API_KEY` | `""` | y |
| `LOBBY_PORT` | `8888` | for helper scripts |

Pass `--env-file .env` to uvicorn, or use the helper scripts which load it automatically.

## Endpoints

- `GET /api/movies` — movies from Jellyfin
- `GET /api/series` — series from Jellyfin
- `GET /api/series/{series_id}/counts` — season/episode counts and season numbers for a series (called async by frontend; needed because Jellyfin doesn't return `ChildCount`/`RecursiveItemCount` in batch queries)
- `GET /api/proxy/{item_id}/{img_type}` — image proxy (types: `poster`, `backdrop`, `logo`); hides API key from browser; cache 24h; validates item_id with `^[a-zA-Z0-9\-]+$` (max 64 chars)
- `GET /` — serves `static/index.html`
- Static files mounted at `/` from `static/` directory

## Developer notes

- **Stack:** Backend: FastAPI + httpx + uvicorn (pinned). Frontend: single-file vanilla HTML/CSS/JS (~1481 lines).
- **Python:** 3.12+
- No tests, linting, typecheck, or formatter config. No CI.
- Requires a reachable Jellyfin instance (`JELLYFIN_URL` + `JELLYFIN_API_KEY`).
- `docs_url=None, redoc_url=None` — no auto-generated API docs.
- DESIGN.md references a Next.js/React/Tailwind UI that does not match the current vanilla frontend; treat as aspirational/outdated.
