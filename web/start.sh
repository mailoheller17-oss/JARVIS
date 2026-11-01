#!/usr/bin/env bash
# Startet Jarvis mit Auto-Reload im Hintergrund auf Port 8765.
cd "$(dirname "$0")"
mkdir -p ../data
[ -f .pid ] && kill "$(cat .pid)" 2>/dev/null
# Port 8765 sicher freimachen (falls alter Server ohne .pid läuft)
for p in $(lsof -t -iTCP:8765 -sTCP:LISTEN 2>/dev/null); do kill "$p" 2>/dev/null; done
sleep 1
if [ -z "$JARVIS_WEB_TOKEN" ]; then
  # Fester Dev-Token: einmal erzeugt, bleibt über Neustarts gleich (data/ ist in .gitignore)
  [ -s ../data/.devtoken ] || echo "dev-$(head -c 9 /dev/urandom | od -An -tx1 | tr -d ' \n')" > ../data/.devtoken
  chmod 600 ../data/.devtoken
  export JARVIS_DEV_TOKEN="$(cat ../data/.devtoken)"
  echo "Kein JARVIS_WEB_TOKEN gesetzt -> Dev-Token steht in data/.devtoken"
fi
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8765 --reload --reload-dir . --reload-dir ../tools \
  --reload-include '*.html' --reload-include '*.js' --reload-include '*.css' --reload-include '*.json' \
  > server.log 2>&1 &
echo $! > .pid
URL="http://localhost:8765"
[ -n "$CODESPACE_NAME" ] && URL="https://${CODESPACE_NAME}-8765.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"
echo "Jarvis läuft: $URL   (Log: web/server.log)"
echo "Handy-Link mit Auto-Login: python3 tools/link.py"
