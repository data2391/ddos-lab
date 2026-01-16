# 🧪 HTTP Flood Lab Éducatif

> **Apprenez les attaques DDoS applicatives avec un outil intelligent et auto-adaptatif.**

![Attaque](https://via.placeholder.com/800x400?text=HTTP+Flood+en+cours)

## 🚀 Démarrage rapide

```bash
# Sur la machine cible
git clone https://github.com/data2391/ddos-lab.git
cd ddos-lab
python3 server/simple-server.py 8000

# Sur la machine attaquante
cd ddos-lab
pip3 install aiohttp
./launch.sh http://192.168.1.10:8000
