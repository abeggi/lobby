#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="lobby"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
USER="$(whoami)"
ENV_FILE="${SCRIPT_DIR}/.env"

# ── Utils ─────────────────────────────────────────────────────────────────
red()   { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
blue()  { printf '\033[34m%s\033[0m\n' "$*"; }

# ── Install ───────────────────────────────────────────────────────────────
install() {
  if [ "$(id -u)" -ne 0 ]; then
    red "Run with sudo or as root."
    exit 1
  fi

  if [ ! -f "$ENV_FILE" ]; then
    red "Missing $ENV_FILE — create it from .env.sample first."
    exit 1
  fi

  if [ ! -f "${SCRIPT_DIR}/.venv/bin/uvicorn" ]; then
    red "Virtual environment not found. Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
  fi

  # Detect port from env
  # shellcheck disable=SC1091
  . "$ENV_FILE"
  PORT="${LOBBY_PORT:-8080}"

  blue "Installing ${SERVICE_NAME} service (port ${PORT})…"

  cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Lobby — Jellyfin Media Browser
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${SCRIPT_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${SCRIPT_DIR}/.venv/bin/uvicorn main:app --host 0.0.0.0 --port ${PORT}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable "${SERVICE_NAME}"
  systemctl start "${SERVICE_NAME}"

  green "✓ Lobby installed and started."
  systemctl status --no-pager "${SERVICE_NAME}"
}

# ── Uninstall ──────────────────────────────────────────────────────────────
uninstall() {
  if [ "$(id -u)" -ne 0 ]; then
    red "Run with sudo or as root."
    exit 1
  fi
  blue "Removing ${SERVICE_NAME} service…"
  systemctl stop "${SERVICE_NAME}" 2>/dev/null || true
  systemctl disable "${SERVICE_NAME}" 2>/dev/null || true
  rm -f "$SERVICE_FILE"
  systemctl daemon-reload
  green "✓ Lobby uninstalled."
}

# ── Commands ───────────────────────────────────────────────────────────────
case "${1:-}" in
  install)   install ;;
  uninstall) uninstall  ;;
  start)     systemctl start   "${SERVICE_NAME}" ; green "✓ started" ;;
  stop)      systemctl stop    "${SERVICE_NAME}" ; green "✓ stopped" ;;
  restart)   systemctl restart "${SERVICE_NAME}" ; green "✓ restarted" ;;
  enable)    systemctl enable  "${SERVICE_NAME}" ; green "✓ enabled" ;;
  disable)   systemctl disable "${SERVICE_NAME}" ; green "✓ disabled" ;;
  status)    systemctl status --no-pager "${SERVICE_NAME}" ;;
  *)
    echo "Usage: $0 {install|uninstall|start|stop|restart|enable|disable|status}"
    exit 1
    ;;
esac
