import socket
import http.server
import socketserver
import sys

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

# Set server header to allow CORS / cross origin
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

port = find_free_port()

try:
    # Use ThreadingTCPServer so it doesn't block
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), MyHTTPRequestHandler) as httpd:
        print(f"SERVER_URL: http://127.0.0.1:{port}/index.html", flush=True)
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}", flush=True)
    sys.exit(1)
