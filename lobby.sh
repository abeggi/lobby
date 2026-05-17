#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$APP_DIR/.lobby.pid"
UVICORN="$APP_DIR/.venv/bin/uvicorn"

# Carica .env se esiste
if [ -f "$APP_DIR/.env" ]; then
    set -a; source "$APP_DIR/.env"; set +a
fi

PORT="${LOBBY_PORT:-8080}"
HOST="${LOBBY_HOST:-0.0.0.0}"

if [ ! -x "$UVICORN" ]; then
    echo "venv not found — run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

start() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "lobby is already running (PID $(cat "$PIDFILE"))"
        exit 1
    fi
    echo "starting lobby on $HOST:$PORT ..."
    cd "$APP_DIR"
    nohup "$UVICORN" main:app --host "$HOST" --port "$PORT" > "$APP_DIR/.lobby.log" 2>&1 &
    echo $! > "$PIDFILE"
    sleep 1
    if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "lobby started (PID $(cat "$PIDFILE"))"
    else
        echo "lobby failed to start — check .lobby.log"
        rm -f "$PIDFILE"
        exit 1
    fi
}

stop() {
    if [ ! -f "$PIDFILE" ]; then
        echo "no PID file — lobby not running"
        return 0
    fi
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "stopping lobby (PID $PID) ..."
        kill "$PID"
        sleep 1
        if kill -0 "$PID" 2>/dev/null; then
            echo "forcing stop ..."
            kill -9 "$PID" 2>/dev/null || true
        fi
    fi
    rm -f "$PIDFILE"
    echo "lobby stopped"
}

status() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "lobby is running (PID $(cat "$PIDFILE")) on $HOST:$PORT"
    else
        echo "lobby is not running"
    fi
}

case "${1:-}" in
    start)   start ;;
    stop)    stop ;;
    restart) stop; start ;;
    status)  status ;;
    *)
        echo "usage: $0 {start|stop|restart|status}"
        exit 2
        ;;
esac
