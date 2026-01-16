#!/usr/bin/env python3
"""Serveur HTTP minimaliste – vulnérable par conception."""
from http.server import HTTPServer, BaseHTTPRequestHandler
import time

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Simule un traitement variable
        if self.path == "/slow":
            time.sleep(2)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>DDoS Lab - Serveur Cible</h1>")

    def do_POST(self):
        # Lit le corps → vulnérable à Slow POST
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"✅ Serveur démarré sur :{port}")
    server.serve_forever()
