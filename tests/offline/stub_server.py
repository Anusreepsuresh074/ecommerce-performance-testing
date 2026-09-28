#!/usr/bin/env python3
"""Local stand-in for the DummyJSON endpoints the shopper journey uses, for offline script validation.

It answers like the real API (status, JSON shape, cf-cache-status and x-ratelimit-remaining headers) and records what
the script sent (paths, query, whether Authorization or Cookie headers were present — never their values) to a JSONL
request log that check-offline.py inspects.

Environment:
  STUB_PORT   port on 127.0.0.1 (default 8089)
  STUB_LOG    request log path (JSONL)
  STUB_USER, STUB_PASS   the only credentials login accepts
  STUB_MODE   ok | notoken (login omits accessToken) | ratelimit (429 from the 8th request)
"""

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

MODE = os.environ.get("STUB_MODE", "ok")
TOKEN = "stub.jwt.token"
LOG = open(os.environ["STUB_LOG"], "a")  # noqa: SIM115 - kept open for the server's lifetime
lock = threading.Lock()
count = 0


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("cf-cache-status", "DYNAMIC")
        self.send_header("x-ratelimit-remaining", "97")
        self.end_headers()
        self.wfile.write(body)

    def record(self, n, method, url, query):
        auth = self.headers.get("Authorization")
        entry = {
            "n": n,
            "method": method,
            "path": url.path,
            "query": query,
            "auth": "bearer-ok" if auth == f"Bearer {TOKEN}" else ("other" if auth else None),
            "cookie": self.headers.get("Cookie") is not None,
        }
        with lock:
            LOG.write(json.dumps(entry) + "\n")
            LOG.flush()

    def handle_request(self, method):
        global count
        with lock:
            count += 1
            n = count
        url = urlparse(self.path)
        query = parse_qs(url.query)
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0)) if method == "POST" else b""
        self.record(n, method, url, query)

        if MODE == "ratelimit" and n >= 8:
            return self.reply(429, {"message": "request limit exceeded, please wait a few seconds"})
        if method == "POST" and url.path == "/auth/login":
            creds = json.loads(body or b"{}")
            if creds.get("username") != os.environ["STUB_USER"] or creds.get("password") != os.environ["STUB_PASS"]:
                return self.reply(400, {"message": "Invalid credentials"})
            resp = {"id": 1, "username": creds["username"], "refreshToken": "stub.refresh"}
            if MODE != "notoken":
                resp["accessToken"] = TOKEN
            return self.reply(200, resp)
        if url.path == "/auth/me":
            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                return self.reply(401, {"message": "Access Token is required"})
            return self.reply(200, {"id": 1, "username": os.environ["STUB_USER"]})
        if url.path == "/products/search":
            ids = [3, 7, 11] if query.get("q", [""])[0] else []
            return self.reply(200, {"products": [{"id": i} for i in ids], "total": len(ids), "skip": 0, "limit": 30})
        if url.path == "/products":
            skip = int(query.get("skip", ["0"])[0])
            return self.reply(200, {"products": [{"id": skip + 1}], "total": 194, "skip": skip, "limit": 30})
        if url.path.startswith("/products/"):
            pid = url.path.rsplit("/", 1)[1]
            if not pid.isdigit():
                return self.reply(404, {"message": f"Product with id '{pid}' not found"})
            return self.reply(200, {"id": int(pid), "title": "stub"})
        return self.reply(404, {"message": "not found"})

    def do_GET(self):  # noqa: N802 - http.server API
        self.handle_request("GET")

    def do_POST(self):  # noqa: N802 - http.server API
        self.handle_request("POST")


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(os.environ.get("STUB_PORT", "8089"))), Handler).serve_forever()
