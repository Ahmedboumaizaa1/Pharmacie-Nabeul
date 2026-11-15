#!/usr/bin/env bash
# Met en service une version déjà publiée (jamais reconstruite), puis contrôle la santé.
# Sert aussi au retour arrière : il suffit de passer la version précédente.
# Usage : scripts/deploy.sh v1.0.0
set -euo pipefail

VERSION="${1:?Usage : scripts/deploy.sh vX.Y.Z}"
export APP_VERSION="$VERSION"
HEALTH_URL="${HEALTH_URL:-http://localhost:8000/health}"

echo "Mise en service de la version $VERSION"
docker compose pull app
docker compose up -d --wait --no-build

"$(dirname "$0")/check.sh" "$HEALTH_URL"
echo "Version $VERSION en service."
