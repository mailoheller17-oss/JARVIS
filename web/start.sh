#!/usr/bin/env bash
# Startet Jarvis mit Auto-Reload im Hintergrund auf Port 8765.
cd "$(dirname "$0")"
[ -f .pid ] && kill "$(cat .pid)" 2>/dev/null
# Port 8765 sicher freimachen (falls alter Server ohne .pid läuft)
for p in $(lsof -t -iTCP:8765 -sTCP:LISTEN 2>/dev/null); do kill "$p" 2>/dev/null; done
sleep 1
if [ -z "$JARVIS_WEB_TOKEN" ]; then
  export JARVIS_DEV_TOKEN="${JARVIS_DEV_TOKEN:-dev-$(head -c 6 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
  echo "Kein JARVIS_WEB_TOKEN gesetzt -> Dev-Token: $JARVIS_DEV_TOKEN" | tee .devtoken
fi
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8765 --reload \
  --reload-include '*.html' --reload-include '*.js' --reload-include '*.css' --reload-include '*.json' \
  > server.log 2>&1 &
echo $! > .pid
echo "Jarvis läuft: http://localhost:8765  (Log: web/server.log)"
