#!/usr/bin/env python3
"""github-issues MCP server for Antigravity (agy) and any stdio MCP client.

Posts and reads GitHub issue comments **without the `gh` CLI**: it calls the
GitHub REST API with the Python standard library only (no pip install).

Auth (the token is never printed, logged or returned):
  1. GITHUB_TOKEN or GH_TOKEN from the environment, else
  2. the git credential already stored for github.com (`git credential fill`),
     e.g. Git Credential Manager on Windows after any `git push` login.

Safety:
  - Writes only to repos matching GH_ALLOWED_REPOS (comma list, `owner/*` ok).
    Default: cogito5170/*  ("*" allows all).
  - Bodies are capped at 60,000 chars (GitHub's limit is 65,536).

Transport: MCP over stdio, newline-delimited JSON-RPC 2.0.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

SERVER = {"name": "github-issues", "version": "0.1.0"}
PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")
API = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
MAX_BODY = 60_000
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")

_token_cache = {}


# ---------- auth ----------

def _git_credential_token():
    """Ask git for the stored github.com credential (no prompt, no output)."""
    host = re.sub(r"^https?://", "", API)
    host = "github.com" if host in ("api.github.com",) else host.split("/")[0]
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    try:
        out = subprocess.run(["git", "credential", "fill"],
                             input=f"protocol=https\nhost={host}\n\n",
                             capture_output=True, text=True, timeout=20, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    for line in out.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip() or None
    return None


def get_token():
    if "t" not in _token_cache:
        tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        source = "env"
        if not tok:
            tok, source = _git_credential_token(), "git-credential"
        _token_cache["t"] = (tok, source if tok else None)
    return _token_cache["t"]


# ---------- policy ----------

def allowed(repo):
    pats = [p.strip() for p in os.environ.get("GH_ALLOWED_REPOS", "cogito5170/*").split(",") if p.strip()]
    for p in pats:
        if p == "*" or p.lower() == repo.lower():
            return True
        if p.endswith("/*") and repo.lower().startswith(p[:-1].lower()):
            return True
    return False


class ToolError(Exception):
    pass


def check_repo(repo, write):
    if not isinstance(repo, str) or not REPO_RE.match(repo):
        raise ToolError("repo must look like 'owner/name'")
    if write and not allowed(repo):
        raise ToolError(f"repo {repo} is not in GH_ALLOWED_REPOS")


# ---------- GitHub REST ----------

def gh(method, path, payload=None):
    tok, _ = get_token()
    if not tok:
        raise ToolError("no GitHub token: set GITHUB_TOKEN in your environment, "
                        "or sign in once with git (e.g. `git push` to github.com) so "
                        "`git credential fill` can supply it")
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(API + path, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {tok}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "github-issues-mcp/0.1",
        **({"Content-Type": "application/json"} if data else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")[:300]
        msg = msg.replace(tok, "***")
        raise ToolError(f"GitHub API {e.code}: {msg}")
    except urllib.error.URLError as e:
        raise ToolError(f"network error: {e.reason}")


# ---------- tools ----------

def t_whoami(_args):
    tok, source = get_token()
    if not tok:
        raise ToolError("no token found (see GITHUB_TOKEN / git credential)")
    me = gh("GET", "/user")
    return {"login": me.get("login"), "token_source": source,
            "allowed_repos": os.environ.get("GH_ALLOWED_REPOS", "cogito5170/*")}


def t_comment(args):
    repo, num, body = args.get("repo"), args.get("issue_number"), args.get("body")
    check_repo(repo, write=True)
    if not isinstance(num, int) or num < 1:
        raise ToolError("issue_number must be a positive integer")
    if not isinstance(body, str) or not body.strip():
        raise ToolError("body must be a non-empty string")
    if len(body) > MAX_BODY:
        raise ToolError(f"body is {len(body)} chars; limit {MAX_BODY}")
    c = gh("POST", f"/repos/{repo}/issues/{num}/comments", {"body": body})
    return {"id": c["id"], "url": c["html_url"], "created_at": c["created_at"]}


def t_read(args):
    repo, num = args.get("repo"), args.get("issue_number")
    check_repo(repo, write=False)
    if not isinstance(num, int) or num < 1:
        raise ToolError("issue_number must be a positive integer")
    limit = max(1, min(int(args.get("limit", 10)), 100))
    since = args.get("since")
    q = "?per_page=100" + (f"&since={urllib.parse.quote(str(since))}" if since else "")
    items = gh("GET", f"/repos/{repo}/issues/{num}/comments{q}") or []
    items = items[-limit:]
    return [{"id": c["id"], "url": c["html_url"], "author": (c.get("user") or {}).get("login"),
             "created_at": c["created_at"], "body": c["body"]} for c in items]


def t_create(args):
    repo, title, body = args.get("repo"), args.get("title"), args.get("body", "")
    check_repo(repo, write=True)
    if not isinstance(title, str) or not title.strip():
        raise ToolError("title must be a non-empty string")
    if len(body or "") > MAX_BODY:
        raise ToolError("body too long")
    i = gh("POST", f"/repos/{repo}/issues", {"title": title, "body": body or ""})
    return {"number": i["number"], "url": i["html_url"]}


def t_list(args):
    repo = args.get("repo")
    check_repo(repo, write=False)
    state = args.get("state", "open")
    if state not in ("open", "closed", "all"):
        raise ToolError("state must be open, closed or all")
    items = gh("GET", f"/repos/{repo}/issues?state={state}&per_page=50") or []
    return [{"number": i["number"], "title": i["title"], "comments": i.get("comments"),
             "updated_at": i.get("updated_at")} for i in items if "pull_request" not in i]


REPO = {"type": "string", "description": "owner/name, e.g. cogito5170/baseline"}
NUM = {"type": "integer", "minimum": 1, "description": "issue number"}
TOOLS = {
    "github_whoami": (t_whoami, "Check that GitHub auth works; returns the login and where the token came from (never the token).",
                      {"type": "object", "properties": {}}),
    "github_issue_comment": (t_comment, "Post a comment on a GitHub issue (replaces `gh issue comment`). Only repos in GH_ALLOWED_REPOS.",
                             {"type": "object", "properties": {"repo": REPO, "issue_number": NUM,
                              "body": {"type": "string", "description": "Markdown body, up to 60,000 chars"}},
                              "required": ["repo", "issue_number", "body"]}),
    "github_issue_comments": (t_read, "Read the latest comments on a GitHub issue.",
                              {"type": "object", "properties": {"repo": REPO, "issue_number": NUM,
                               "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10},
                               "since": {"type": "string", "description": "ISO 8601 time; only comments updated after it"}},
                               "required": ["repo", "issue_number"]}),
    "github_issue_create": (t_create, "Open a new GitHub issue (e.g. a session channel). Only repos in GH_ALLOWED_REPOS.",
                            {"type": "object", "properties": {"repo": REPO, "title": {"type": "string"}, "body": {"type": "string"}},
                             "required": ["repo", "title"]}),
    "github_issues_list": (t_list, "List issues in a repo (to find the right issue number).",
                           {"type": "object", "properties": {"repo": REPO,
                            "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"}},
                            "required": ["repo"]}),
}


# ---------- MCP (JSON-RPC over stdio) ----------

def handle(msg):
    mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
    if mid is None:  # notification (e.g. notifications/initialized)
        return None
    if method == "initialize":
        want = params.get("protocolVersion")
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": want if want in PROTOCOLS else PROTOCOLS[0],
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": [
            {"name": n, "description": d, "inputSchema": s} for n, (_, d, s) in TOOLS.items()]}}
    if method == "tools/call":
        name, args = params.get("name"), params.get("arguments") or {}
        if name not in TOOLS:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown tool {name}"}}
        try:
            out = TOOLS[name][0](args)
            text, err = json.dumps(out, ensure_ascii=False, indent=1), False
        except ToolError as e:
            text, err = str(e), True
        except Exception as e:  # never crash the server
            text, err = f"internal error: {type(e).__name__}: {e}", True
        tok, _ = _token_cache.get("t", (None, None))
        if tok:
            text = text.replace(tok, "***")
        return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": text}], "isError": err}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}


def main():
    stdin, out = sys.stdin.buffer, sys.stdout.buffer
    for raw in stdin:
        line = raw.decode("utf-8", "replace").strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            resp = handle(msg)
        if resp is not None:
            # write UTF-8 bytes: on Windows a piped stdout defaults to the ANSI
            # code page (cp949/cp1252) and would choke on Korean text
            out.write((json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8"))
            out.flush()


if __name__ == "__main__":
    main()
