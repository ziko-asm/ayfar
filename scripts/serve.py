"""Serves the built site locally the way Vercel does: the headers from vercel.json (CSP included)
and 404.html for unknown paths. Used by the browser tests; also handy for a quick look.

Run:  python scripts/serve.py [port]
"""
import http.server
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

with open(os.path.join(ROOT, "vercel.json"), encoding="utf-8") as f:
    RULES = [(re.compile(r["source"].replace("(.*)", ".*")), r["headers"]) for r in json.load(f)["headers"]]

# HSTS and upgrade-insecure-requests only make sense over HTTPS; locally they would break plain-HTTP requests.
SKIP = {"Strict-Transport-Security"}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        path = self.path.split("?")[0]
        for rx, headers in RULES:
            if rx.fullmatch(path):
                for h in headers:
                    if h["key"] not in SKIP:
                        self.send_header(h["key"], h["value"].replace("; upgrade-insecure-requests", ""))
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code != 404:
            return super().send_error(code, message, explain)
        with open(os.path.join(ROOT, "404.html"), "rb") as f:
            body = f.read()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"http://127.0.0.1:{PORT}/")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
