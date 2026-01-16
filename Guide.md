# 🧪 Guide d'utilisation – HTTP Flood Éducatif

## 🎯 Objectif
Apprendre à simuler une attaque **HTTP flood réaliste** contre un serveur web vulnérable.

## 🔧 Prérequis
- Deux machines Linux (attaquant + cible)
- Python 3.7+
- Accès réseau local

## 🚀 Étapes

### 1. Sur la machine cible
Lance un serveur vulnérable :
git clone https://github.com/votre-pseudo/ddos-lab.git
cd ddos-lab
python3 server/simple-server.py 8000
