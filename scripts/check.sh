#!/usr/bin/env bash
# Contrôle de santé : code 0 si /health répond "ok", code non nul sinon.
# Usage : scripts/check.sh [URL] [NB_ESSAIS]
#   0 = application en bonne santé
#   1 = application injoignable ou en erreur
#   2 = curl absent
set -u

URL="${1:-http://localhost:8000/health}"
TRIES="${2:-10}"

command -v curl >/dev/null 2>&1 || { echo "ERREUR : curl est absent" >&2; exit 2; }

for i in $(seq 1 "$TRIES"); do
  if body=$(curl -fsS --max-time 3 "$URL" 2>/dev/null) && echo "$body" | grep -Eq '"status": ?"ok"'; then
    echo "OK ($URL) : $body"
    exit 0
  fi
  echo "Essai $i/$TRIES : pas encore prêt..." >&2
  sleep 2
done

echo "ECHEC : $URL ne répond pas correctement" >&2
exit 1
