# Lobby

Un frontend FastAPI proxy per navigare la libreria di un server Jellyfin. Niente database, niente worker — solo un'app web leggera che serve una SPA statica.

## Funzionalità

- Navigazione di film e serie dalla libreria Jellyfin
- Filtri avanzati: anno, ordinamento, ricerca testuale per titolo
- Pagina dettaglio con poster, backdrop, logo, cast, link trailer, link esterni (TMDB/TVDB/IMDb)
- Proxy immagini (nasconde la API key dal browser, cache 24h)
- Layout responsive con sidebar collassabile
- Tema scuro (accento indaco, sfondo gray-900)
- Cache LocalStorage (60 min) con refresh in background

## Screenshot

![Sezione Film](screenshots/film.png)

*La schermata di navigazione della libreria film.*

## Avvio rapido

```bash
git clone <repo>
cd lobby
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Copia `.env.sample` in `.env` e inserisci i dati del tuo Jellyfin:

```bash
cp .env.sample .env
```

Poi avvia:

```bash
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
```

Oppure usa lo script helper:

```bash
./lobby.sh start    # avvia
./lobby.sh stop     # ferma
./lobby.sh restart  # riavvia
./lobby.sh status   # stato
```

## Configurazione

Tutto via variabili d'ambiente (il file `.env` viene caricato automaticamente):

| Variabile | Default | Obbligatoria |
|---|---|---|
| `JELLYFIN_URL` | `http://localhost:8096` | sì |
| `JELLYFIN_API_KEY` | — | sì |
| `LOBBY_PORT` | `8888` | per lo script lobby.sh |

## Endpoint

| Path | Descrizione |
|---|---|
| `GET /api/movies` | Elenco film da Jellyfin |
| `GET /api/series` | Elenco serie da Jellyfin |
| `GET /api/proxy/{item_id}/{type}` | Proxy immagini (`poster`, `backdrop`, `logo`) |
| `GET /` | Punto di ingresso SPA (`static/index.html`) |

## Stack tecnico

- **Backend:** FastAPI, httpx, uvicorn
- **Frontend:** Vanilla HTML/CSS/JS (singolo file, nessun framework)
- **Python minimo:** 3.12+

## Note

- L'app è inutile senza un'istanza Jellyfin raggiungibile.
- Il proxy immagini è l'unico endpoint che nasconde intenzionalmente le credenziali dal browser.
- Nessun test, nessun linting, nessuna CI.
- `docs_url=None, redoc_url=None` — niente documentazione API auto-generata.
