# Lobby

A FastAPI proxy frontend for browsing a Jellyfin media server. No database, no workers — just a lightweight webapp that serves a static SPA.

## Features

- Browse movies and series from your Jellyfin library
- Advanced filtering: year, sort order, text search on title
- Detail page with poster, backdrop, logo, cast, trailer links, external links (TMDB/TVDB/IMDb)
- Image proxy (hides API key from the browser, 24h cache)
- Responsive layout with collapsible sidebar
- Dark-only theme (indigo accent, gray-900 background)
- LocalStorage cache (60 min) with background refresh

## Quick start

```bash
git clone <repo>
cd lobby
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Copy `.env.sample` to `.env` and fill in your Jellyfin details:

```bash
cp .env.sample .env
```

Then run:

```bash
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
```

Or use the helper script:

```bash
./lobby.sh start
./lobby.sh stop
./lobby.sh restart
./lobby.sh status
```

## Configuration

All via environment variables (`.env` file loaded automatically):

| Variable | Default | Required |
|---|---|---|
| `JELLYFIN_URL` | `http://localhost:8096` | yes |
| `JELLYFIN_API_KEY` | — | yes |
| `LOBBY_PORT` | `8888` | for the lobby.sh script |

## Endpoints

| Path | Description |
|---|---|
| `GET /api/movies` | Movies from Jellyfin |
| `GET /api/series` | Series from Jellyfin |
| `GET /api/proxy/{item_id}/{type}` | Image proxy (types: `poster`, `backdrop`, `logo`) |
| `GET /` | SPA entry point (`static/index.html`) |

## Tech stack

- **Backend:** FastAPI, httpx, uvicorn
- **Frontend:** Vanilla HTML/CSS/JS (single file, no framework)
- **Minimum Python:** 3.12+

## Notes

- The app is useless without a reachable Jellyfin instance.
- The image proxy is the only endpoint that intentionally hides credentials from the browser.
- No tests, no linting, no CI.
- `docs_url=None, redoc_url=None` — no auto-generated API docs.
