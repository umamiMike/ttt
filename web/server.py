import os
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json
from web.session import Session
PORT = 8005

class MainHandler(SimpleHTTPRequestHandler):

    def _set_headers(self, code=200, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-type",content_type)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._set_headers()
            if self.path == "/api/status":
                response = {"status": "ok"}
                self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            if self.path == "/":
                self.path = "index.html"
                session = Session()
                session.start()
                    
            return super().do_GET()


def run(port=PORT):
    os.chdir("web_client")
    httpd = HTTPServer(("", port), MainHandler)
    print(f"serving web client from http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
