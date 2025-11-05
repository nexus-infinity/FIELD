#!/usr/bin/env python3
"""
Train Station Frequency Gate Validator
Port: 43200 (12 * 3600 = 12 hours in seconds, half-day cycle)

Validates Solfeggio frequencies for tetrahedral MCP flow:
  174Hz → Foundation
  285Hz → Quantum Cognition  
  396Hz → Liberation
  417Hz → Transformation
  528Hz → Heart/DNA Repair
  639Hz → Connection
  741Hz → Awakening/Expression
  852Hz → Intuition/Truth (TATA)
  963Hz → Unity/Crown (DOJO)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

SOLFEGGIO_FREQUENCIES = {174, 285, 396, 417, 528, 639, 741, 852, 963}
TRAIN_STATION_PORT = 43200

class FrequencyGateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "aligned",
                "train_station": "active",
                "port": TRAIN_STATION_PORT,
                "frequencies": list(SOLFEGGIO_FREQUENCIES)
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/mcp":
            freq_header = self.headers.get("X-Frequency", "0")
            try:
                freq = int(freq_header)
                aligned = freq in SOLFEGGIO_FREQUENCIES
                
                self.send_response(200 if aligned else 403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                
                response = {
                    "aligned": aligned,
                    "frequency": freq,
                    "message": f"Frequency {freq}Hz {'aligned' if aligned else 'misaligned'}"
                }
                self.wfile.write(json.dumps(response).encode())
            except ValueError:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", TRAIN_STATION_PORT), FrequencyGateHandler)
    print(f"🚂 Train Station frequency gate active on port {TRAIN_STATION_PORT}")
    print(f"   Valid frequencies: {sorted(SOLFEGGIO_FREQUENCIES)}")
    server.serve_forever()
