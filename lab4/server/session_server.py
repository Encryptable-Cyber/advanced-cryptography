#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import uuid
import time

sessions = {}

class SessionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/dashboard':
            cookie_header = self.headers.get('Cookie', '')
            if 'sessionid=' in cookie_header:
                session_id = cookie_header.split('sessionid=')[1].split(';')[0]
                if session_id in sessions:
                    username = sessions[session_id]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<html><body><h1>Welcome {username}!</h1><p>This is your secure dashboard.</p></body></html>".encode())
                    return
            
            self.send_response(401)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Unauthorized</h1><p>Please login first.</p></body></html>")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode())
            
            username = params.get('user', [''])[0]
            password = params.get('pass', [''])[0]
            
            print(f"\n[!] LOGIN ATTEMPT: {username}:{password}")
            
            session_id = str(uuid.uuid4())
            sessions[session_id] = username
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', f'sessionid={session_id}; Path=/; HttpOnly')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Login Successful!</h1><p><a href='/dashboard'>Go to Dashboard</a></p></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

print("[*] Starting session-enabled web server on port 8080")
HTTPServer(('0.0.0.0', 8080), SessionHandler).serve_forever()
