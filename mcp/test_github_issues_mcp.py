"""Tests for github_issues_mcp.py: runs the server as a subprocess against a
local fake GitHub API. usage: python3 mcp/test_github_issues_mcp.py
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(HERE, "github_issues_mcp.py")
TOKEN = "ghp_test_SECRET_123"


class Fake(BaseHTTPRequestHandler):
    calls = []

    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        raw = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        Fake.calls.append(("GET", self.path, self.headers.get("Authorization"), None))
        if self.path == "/user":
            return self._send(200, {"login": "tester"})
        if self.path.startswith("/repos/cogito5170/baseline/issues/18/comments"):
            return self._send(200, [{"id": i, "html_url": f"u{i}", "user": {"login": "a"},
                                     "created_at": "t", "body": f"b{i}"} for i in range(1, 6)])
        if self.path.startswith("/repos/cogito5170/baseline/issues?"):
            return self._send(200, [{"number": 1, "title": "x", "comments": 2, "updated_at": "t"},
                                    {"number": 2, "title": "pr", "pull_request": {}}])
        # error page that echoes the auth header, to test redaction
        return self._send(404, {"message": "Not Found", "echo": self.headers.get("Authorization")})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n))
        Fake.calls.append(("POST", self.path, self.headers.get("Authorization"), body))
        if self.path.endswith("/comments"):
            return self._send(201, {"id": 77, "html_url": "https://x/c77", "created_at": "t"})
        return self._send(201, {"number": 9, "html_url": "https://x/i9"})


class McpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), Fake)
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.api = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def setUp(self):
        Fake.calls.clear()

    def run_server(self, msgs, token=TOKEN, allowed=None, gitconfig=os.devnull):
        env = {k: v for k, v in os.environ.items()
               if k.lower() not in ("http_proxy", "https_proxy", "all_proxy", "github_token", "gh_token")}
        env["GITHUB_API_URL"] = self.api
        home = tempfile.mkdtemp()  # no git credential helper configured
        env.update(HOME=home, USERPROFILE=home, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=gitconfig)
        if token:
            env["GITHUB_TOKEN"] = token
        if allowed is not None:
            env["GH_ALLOWED_REPOS"] = allowed
        inp = "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in msgs).encode()
        p = subprocess.run([sys.executable, SERVER], input=inp, capture_output=True, env=env, timeout=60)
        out = p.stdout.decode("utf-8")
        self.assertNotIn(TOKEN, out + p.stderr.decode("utf-8", "replace"))
        return [json.loads(l) for l in out.splitlines() if l.strip()]

    def call(self, name, args, **kw):
        r = self.run_server([{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                              "params": {"name": name, "arguments": args}}], **kw)
        return r[0]["result"]

    def test_handshake_and_list(self):
        r = self.run_server([
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "ping"},
            {"jsonrpc": "2.0", "id": 4, "method": "nope"},
        ])
        self.assertEqual([m["id"] for m in r], [1, 2, 3, 4])  # notification gets no reply
        self.assertEqual(r[0]["result"]["protocolVersion"], "2025-06-18")
        names = {t["name"] for t in r[1]["result"]["tools"]}
        self.assertEqual(names, {"github_whoami", "github_issue_comment", "github_issue_comments",
                                 "github_issue_create", "github_issues_list"})
        self.assertEqual(r[2]["result"], {})
        self.assertEqual(r[3]["error"]["code"], -32601)

    def test_parse_error(self):
        env = dict(os.environ, GITHUB_API_URL=self.api)
        p = subprocess.run([sys.executable, SERVER], input=b"{bad\n", capture_output=True, env=env, timeout=30)
        self.assertEqual(json.loads(p.stdout)["error"]["code"], -32700)

    def test_comment_posts_with_bearer_and_utf8(self):
        body = '<agv:message sender="agv-session" target="baseline">한글 payload</agv:message>'
        res = self.call("github_issue_comment", {"repo": "cogito5170/baseline", "issue_number": 18, "body": body})
        self.assertFalse(res["isError"], res)
        self.assertEqual(json.loads(res["content"][0]["text"])["url"], "https://x/c77")
        method, path, auth, sent = Fake.calls[-1]
        self.assertEqual((method, path, auth), ("POST", "/repos/cogito5170/baseline/issues/18/comments",
                                                f"Bearer {TOKEN}"))
        self.assertEqual(sent, {"body": body})

    def test_allowlist_blocks_write(self):
        res = self.call("github_issue_comment", {"repo": "someone/else", "issue_number": 1, "body": "x"})
        self.assertTrue(res["isError"])
        self.assertIn("GH_ALLOWED_REPOS", res["content"][0]["text"])
        self.assertEqual(Fake.calls, [])
        res = self.call("github_issue_comment", {"repo": "someone/else", "issue_number": 1, "body": "x"},
                        allowed="someone/else")
        self.assertFalse(res["isError"])

    def test_bad_args(self):
        for args in ({"repo": "nope", "issue_number": 1, "body": "x"},
                     {"repo": "cogito5170/baseline", "issue_number": 0, "body": "x"},
                     {"repo": "cogito5170/baseline", "issue_number": 1, "body": "  "},
                     {"repo": "cogito5170/baseline", "issue_number": 1, "body": "x" * 60_001}):
            self.assertTrue(self.call("github_issue_comment", args)["isError"], args)
        self.assertEqual(Fake.calls, [])

    def test_error_redacts_token(self):
        res = self.call("github_issue_comments", {"repo": "cogito5170/other", "issue_number": 3})
        self.assertTrue(res["isError"])
        self.assertIn("404", res["content"][0]["text"])
        self.assertIn("***", res["content"][0]["text"])  # echoed header was redacted

    def test_read_limit_and_list(self):
        res = self.call("github_issue_comments", {"repo": "cogito5170/baseline", "issue_number": 18,
                                                  "limit": 2, "since": "2026-10-04T00:00:00Z"})
        items = json.loads(res["content"][0]["text"])
        self.assertEqual([c["id"] for c in items], [4, 5])
        self.assertIn("since=2026-10-04T00%3A00%3A00Z", Fake.calls[-1][1])
        res = self.call("github_issues_list", {"repo": "cogito5170/baseline"})
        self.assertEqual([i["number"] for i in json.loads(res["content"][0]["text"])], [1])

    def test_create_and_whoami(self):
        res = self.call("github_issue_create", {"repo": "cogito5170/baseline", "title": "t", "body": "b"})
        self.assertEqual(json.loads(res["content"][0]["text"])["number"], 9)
        res = self.call("github_whoami", {})
        who = json.loads(res["content"][0]["text"])
        self.assertEqual((who["login"], who["token_source"]), ("tester", "env"))

    def test_no_token(self):
        res = self.call("github_issue_comment", {"repo": "cogito5170/baseline", "issue_number": 1, "body": "x"},
                        token=None)
        self.assertTrue(res["isError"])
        self.assertIn("GITHUB_TOKEN", res["content"][0]["text"])
        self.assertEqual(Fake.calls, [])

    def test_git_credential_fallback(self):
        cfg = os.path.join(tempfile.mkdtemp(), "gitconfig")
        with open(cfg, "w") as f:  # stands in for Git Credential Manager
            f.write('[credential]\n\thelper = "!f() { echo username=x; echo password=%s; }; f"\n' % TOKEN)
        res = self.call("github_whoami", {}, token=None, gitconfig=cfg)
        self.assertEqual(json.loads(res["content"][0]["text"])["token_source"], "git-credential")
        self.assertEqual(Fake.calls[-1][2], f"Bearer {TOKEN}")

    def test_unknown_tool(self):
        r = self.run_server([{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "x"}}])
        self.assertEqual(r[0]["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()
