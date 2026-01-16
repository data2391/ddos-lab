#!/bin/bash
# install.sh - Installe toutes les dépendances du lab

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[+]${NC} $1"; }
error() { echo -e "${RED}[!]${NC} $1" >&2; exit 1; }

# Détection du système
if command -v pacman &> /dev/null; then
    PKG_MGR="pacman -S --noconfirm"
elif command -v apt &> /dev/null; then
    PKG_MGR="apt install -y"
else
    error "Système non supporté (Arch/Debian seulement)"
fi

log "🔧 Mise à jour du système..."
sudo $PKG_MGR git python3

# Installation de aiohttp
log "📦 Installation de aiohttp..."
pip3 install aiohttp

# Installation de slowhttptest (optionnel mais utile)
if [[ "$PKG_MGR" == *"pacman"* ]]; then
    if ! command -v yay &> /dev/null; then
        log "📥 Installation de yay..."
        git clone https://aur.archlinux.org/yay.git /tmp/yay
        cd /tmp/yay && makepkg -si --noconfirm
    fi
    log "⚡ Installation de slowhttptest..."
    yay -S --noconfirm slowhttptest
else
    log "⚡ Installation de slowhttptest depuis les sources..."
    sudo apt install -y build-essential libssl-dev
    cd /tmp
    git clone https://github.com/shekyan/slowhttptest.git
    cd slowhttptest
    ./configure && make && sudo make install
fi

log "✅ Installation terminée !"
echo
echo "➡️  Lance le serveur : python3 server/simple-server.py 8000"
echo "➡️  Lance l'attaque : ./launch.sh http://IP:8000"
