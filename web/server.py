import os
import http.server

PORT = 8005


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        return super().do_GET()

class MainServer(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, code=200, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-type",content_type)
        self.end_headers()

    # def do_GET(self):
    #     if self.path.startswith("/static/"):
    #         self.path = self.path[len(".static/"):]
    #         return super().do_GET()


def run(port=PORT):
    os.chdir("web_client")
    httpd = http.server.HTTPServer(("", port), StaticHandler)
    print(f"serving static from http://localhost:{port}/web_client/")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
