import http.server
import socketserver
import os

PORT = 8000

# Define the handler class for the HTTP server
class FileServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.abspath('.'), **kwargs)

# Create an instance of the HTTP server
with socketserver.TCPServer(("", PORT), FileServerHandler) as httpd:
    print(f"Serving files from the current directory at http://localhost:{PORT}")
    httpd.serve_forever()