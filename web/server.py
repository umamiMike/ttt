import http.server
import socketserver

PORT = 8000


class IndexHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory="static/", **kwargs)


with socketserver.TCPServer(("", PORT), IndexHandler) as httpd:
    print(f"serving at port {PORT}")
    httpd.serve_forever()
