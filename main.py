import os
import re
import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Lobby", docs_url=None, redoc_url=None)

JELLYFIN_URL = os.getenv("JELLYFIN_URL", "http://localhost:8096").rstrip("/")
JELLYFIN_KEY = os.getenv("JELLYFIN_API_KEY", "")

_FIELDS = (
    "Overview,Genres,CommunityRating,OfficialRating,"
    "RunTimeTicks,Studios,ProductionYear,"
    "ImageTags,BackdropImageTags,ChildCount,Status,SortName,"
    "PremiereDate,RemoteTrailers,People,ProviderIds,"
    "RecursiveItemCount"
)

_HEADERS = {"X-Emby-Token": JELLYFIN_KEY}


async def _jf_items(item_type: str) -> list[dict]:
    params = {
        "IncludeItemTypes": item_type,
        "Recursive":        "true",
        "Fields":           _FIELDS,
        "SortBy":           "SortName",
        "SortOrder":        "Ascending",
        "Limit":            "10000",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(
                f"{JELLYFIN_URL}/Items",
                headers=_HEADERS,
                params=params,
            )
            r.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(502, f"Jellyfin irraggiungibile: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(e.response.status_code, f"Jellyfin error: {e}")

    return r.json().get("Items", [])


def _proxy_url(item_id: str, img_type: str) -> str:
    return f"/api/proxy/{item_id}/{img_type}"


def _cast_list(people: list[dict]) -> list[dict]:
    return [
        {
            "id":    p["Id"],
            "name":  p.get("Name"),
            "role":  p.get("Role"),
            "type":  p.get("Type"),
            "image": _proxy_url(p["Id"], "poster") if p.get("PrimaryImageTag") else None,
        }
        for p in people if p.get("Type") in ("Actor", "GuestStar")
    ]


@app.get("/api/movies")
async def get_movies():
    items = await _jf_items("Movie")
    result = []
    for m in items:
        iid  = m["Id"]
        tags = m.get("ImageTags", {})
        bk   = m.get("BackdropImageTags", [])
        ticks   = m.get("RunTimeTicks") or 0
        studios = m.get("Studios", [])
        trailers = [t["Url"] for t in m.get("RemoteTrailers", []) if t.get("Url")]
        result.append({
            "id":            iid,
            "title":         m.get("Name", ""),
            "sortTitle":     m.get("SortName", "").lower(),
            "year":          m.get("ProductionYear"),
            "releaseDate":   m.get("PremiereDate"),
            "overview":      m.get("Overview", ""),
            "poster":        _proxy_url(iid, "poster") if tags.get("Primary") else None,
            "logo":          _proxy_url(iid, "logo") if tags.get("Logo") else None,
            "fanart":        _proxy_url(iid, "backdrop") if bk else None,
            "genres":        m.get("Genres", []),
            "runtime":       round(ticks / 600_000_000) if ticks else None,
            "certification": m.get("OfficialRating"),
            "studio":        studios[0]["Name"] if studios else None,
            "rating":        round(float(m["CommunityRating"]), 1) if m.get("CommunityRating") else None,
            "trailers":      trailers,
            "cast":          _cast_list(m.get("People", [])),
            "externalIds":   m.get("ProviderIds", {}),
        })
    return result


@app.get("/api/series")
async def get_series():
    items = await _jf_items("Series")
    result = []
    for s in items:
        iid  = s["Id"]
        tags = s.get("ImageTags", {})
        bk   = s.get("BackdropImageTags", [])
        studios = s.get("Studios", [])
        trailers = [t["Url"] for t in s.get("RemoteTrailers", []) if t.get("Url")]
        result.append({
            "id":         iid,
            "title":      s.get("Name", ""),
            "sortTitle":  s.get("SortName", "").lower(),
            "year":       s.get("ProductionYear"),
            "releaseDate": s.get("PremiereDate"),
            "overview":   s.get("Overview", ""),
            "poster":     _proxy_url(iid, "poster") if tags.get("Primary") else None,
            "logo":       _proxy_url(iid, "logo") if tags.get("Logo") else None,
            "fanart":     _proxy_url(iid, "backdrop") if bk else None,
            "genres":     s.get("Genres", []),
            "status":     s.get("Status"),
            "network":    studios[0]["Name"] if studios else None,
            "seasons":      s.get("ChildCount"),
            "episodeCount": s.get("RecursiveItemCount"),
            "rating":       round(float(s["CommunityRating"]), 1) if s.get("CommunityRating") else None,
            "trailers":   trailers,
            "cast":       _cast_list(s.get("People", [])),
            "externalIds": s.get("ProviderIds", {}),
        })
    return result


# ── Proxy immagini ─────────────────────────────────────────────────────────────
ITEM_ID_PATTERN = re.compile(r"^[a-zA-Z0-9\-]+$")


@app.get("/api/proxy/{item_id}/{img_type}")
async def proxy_image(item_id: str, img_type: str):
    if not ITEM_ID_PATTERN.match(item_id) or len(item_id) > 64:
        raise HTTPException(400, "Invalid item ID format")

    if img_type == "poster":
        url    = f"{JELLYFIN_URL}/Items/{item_id}/Images/Primary"
        params = {"fillWidth": "400", "quality": "80"}
    elif img_type == "backdrop":
        url    = f"{JELLYFIN_URL}/Items/{item_id}/Images/Backdrop/0"
        params = {"fillWidth": "1280", "quality": "70"}
    elif img_type == "logo":
        url    = f"{JELLYFIN_URL}/Items/{item_id}/Images/Logo"
        params = {"fillWidth": "400", "quality": "80"}
    else:
        raise HTTPException(404)

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            r = await client.get(url, headers=_HEADERS, params=params)
            if r.status_code == 404:
                raise HTTPException(404)
            r.raise_for_status()
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(502, "Image proxy failed")

    ct = r.headers.get("content-type", "image/jpeg")
    cache_headers = {"Cache-Control": "public, max-age=86400"}
    return Response(content=r.content, media_type=ct, headers=cache_headers)


# ── Series counts ────────────────────────────────────────────────────────────
@app.get("/api/series/{series_id}/counts")
async def series_counts(series_id: str):
    if not ITEM_ID_PATTERN.match(series_id) or len(series_id) > 64:
        raise HTTPException(400, "Invalid series ID")

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            r = await client.get(
                f"{JELLYFIN_URL}/Items",
                headers=_HEADERS,
                params={
                    "ParentId": series_id,
                    "IncludeItemTypes": "Season",
                    "Recursive": "true",
                    "SortBy": "IndexNumber",
                    "SortOrder": "Ascending",
                    "Fields": "IndexNumber",
                },
            )
            r.raise_for_status()
            body = r.json()
            season_items = body.get("Items", [])
            seasons = len(season_items)
            seasonNumbers = [
                s.get("IndexNumber")
                for s in season_items
                if s.get("IndexNumber") is not None
            ]

            r = await client.get(
                f"{JELLYFIN_URL}/Items",
                headers=_HEADERS,
                params={
                    "ParentId": series_id,
                    "IncludeItemTypes": "Episode",
                    "Recursive": "true",
                    "Limit": "0",
                },
            )
            r.raise_for_status()
            episodes = r.json().get("TotalRecordCount", 0)
        except httpx.RequestError as e:
            raise HTTPException(502, f"Jellyfin irraggiungibile: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(e.response.status_code, f"Jellyfin error: {e}")

    return {"seasons": seasons, "episodes": episodes, "seasonNumbers": seasonNumbers}


# ── SPA ───────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return FileResponse("static/index.html")

app.mount("/", StaticFiles(directory="static"), name="static")
