import http.server
import socketserver
import os
import webbrowser
import json
from urllib.parse import unquote, urlparse

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(DIRECTORY, 'Content')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # Handle API request to list markdown files
        if self.path == '/api/files':
            files = self.list_markdown_files()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
        else:
            # Default file serving
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def list_markdown_files(self, directory=CONTENT_DIR, base_path=''):
        files = []
        try:
            for item in sorted(os.listdir(directory)):
                full_path = os.path.join(directory, item)
                rel_path = os.path.join(base_path, item)
                
                if os.path.isdir(full_path):
                    # Skip directories that end with '_files' as they likely contain assets
                    if not item.endswith('_files'):
                        files.append({
                            'name': item.replace('_', ' ').title(),
                            'path': rel_path,
                            'type': 'directory',
                            'children': self.list_markdown_files(full_path, rel_path)
                        })
                elif item.lower().endswith('.md'):
                    files.append({
                        'name': os.path.splitext(item)[0].replace('_', ' ').title(),
                        'path': rel_path,
                        'type': 'file'
                    })
        except Exception as e:
            print(f"Error listing files: {e}")
        return files

def run_server(port=PORT, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                print(f"Serving at http://localhost:{port}")
                print("Press Ctrl+C to stop the server")
                webbrowser.open(f'http://localhost:{port}')
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nServer stopped.")
                    return
                except Exception as e:
                    print(f"\nError: {e}")
                    return
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"Port {port} is in use, trying port {port + 1}...")
                port += 1
            else:
                print(f"Error: {e}")
                return
    print(f"Failed to start server after {max_attempts} attempts")

if __name__ == '__main__':
    run_server()
