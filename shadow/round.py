"""AO P1 shadow round (BD-243): A1 session watch, A2 pending-report queue,
A3 header pre-check, A4 W1 read-only count, A9 HUMAN_QUEUE done-check.

Read-only. Writes only into this repo (shadow/rounds/, shadow/state.json).
Inputs that only MCP tools can fetch are passed as files:
  --sessions  list_sessions(mine) output file (raw tool result)
  --w1        list_events(W1) output file (raw tool result), optional
Output: shadow/rounds/round-NN.json (ao-status/1) and a short text summary.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys

import ga.forms as forms

ROOT = pathlib.Path(__file__).resolve().parent
OWNER_REPO = "cogito5170/baseline"
BASELINE_BRANCH = "claude/gracious-meitner-vp49xe"

# Sessions baseline directs. Ids from PROTOCOL/DECISION_LOG where recorded,
# otherwise matched by title (marked "title").
SESSIONS = {
    "session_013GnrUQPpcfK4ea1a1Y6SuY": ("baseline", "doc"),
    "session_01GSGTDQF8LUeGv8NzcBPhCG": ("AMP", "doc"),
    "session_012bx4BgLuifWh7YzJ1k1dcU": ("W1", "title"),
    "session_01KHd6Ft8vzjYffMcwhTDwcy": ("GMG", "doc"),
    "session_01WTesMn7FjKtPKSo7SpQBY8": ("WUG", "doc"),
    "session_016ZZiyiYncdkpnpviFL8dBk": ("GR", "title"),
    "session_01L1Sd43LpUVDA9dsnnuWVKt": ("GA", "title"),
    "session_01AsrfNRr3QHbDg7YTBNZQCj": ("SDK", "title"),
    "session_01GgeKT2ewpbQzs7rzJAYq74": ("Health", "title"),
    "session_01DA1zjp6NDjCEZsM8pqWJsz": ("Guard", "title"),
    "session_011tZpN4sVKkxxugFNfWVpDE": ("Action", "title"),
    "session_01MYyRTA1KXiRnDrtvcRnT1a": ("Telemetry", "title"),
    "session_011nbdyVsJ1gRksY1dUf6G4s": ("DC", "doc"),
    "session_01Q5TZ4PEKf6gj5e7Z6ShX41": ("Sensor", "title"),
    "session_01JWUCzhkqtsYpyJ6PyRq9cA": ("AO", "self"),
}
W1_ID = "session_012bx4BgLuifWh7YzJ1k1dcU"
BLOCK_WORDS = re.compile(r"guard|deny|denied|blocked|거부|막힘|permission", re.I)
GA_FENCE = re.compile(r"```ga\s*\n(.*?)\n```", re.S)
CMD_ID = re.compile(r"CMD-[A-Z]+\d+")


def gh(path):
    out = subprocess.run(["gh", "api", "--paginate", path], check=True,
                         capture_output=True, text=True).stdout
    # --paginate concatenates JSON arrays: "][" -> ","
    return json.loads(out.replace("]\n[", ",").replace("][", ","))


def load_tool_result(path):
    s = pathlib.Path(path).read_text()
    j = s.find('{"ccr"')
    if j < 0:
        j = s.find("{")
    doc, _ = json.JSONDecoder().raw_decode(s[j:])
    return doc.get("ccr", doc)


# ---------- A2/A3: reports ----------

def kind_of(body):
    head = body.lstrip()[:300]
    m = GA_FENCE.search(body)
    schema = None
    if m:
        try:
            schema = json.loads(m.group(1)).get("schema")
        except ValueError:
            schema = "unparsable"
    # Baseline's own heads over time: "## [baseline → X]", "## baseline 확인/지시 …",
    # "**CMD-X1 — …**" (bare directive), "## CMD-X1 에 덧붙임".
    if (re.match(r"(?:## )?\[?baseline", head) or re.match(r"(?:\*\*|## )CMD-[A-Z]+\d+", head)
            or "## [baseline" in body[:600]
            or schema in ("directive/1", "directive/2", "review/1")):
        return "baseline", schema
    if "<AO>" in head[:40] or (m and '"from": "AO"' in m.group(1)):
        return "ao", schema
    if schema in ("report/1", "report/2"):
        return "report", schema
    tag = re.match(r"(?:## )?\[([^\]]+)\]", head)
    if tag and not tag.group(1).startswith("baseline"):
        return "report", schema
    return "other", schema


def header_check(body):
    if not GA_FENCE.search(body):
        return {"head": "missing"}
    try:
        _, _, soft = forms.parse_post(body)
        return {"head": "ok", "soft": [f"{p.path}: {p.message}" for p in soft]}
    except forms.FormError as e:
        return {"head": "hard", "problems": [str(e)[:300]]}
    except Exception as e:  # parser bug must not stop the round
        return {"head": "error", "problems": [repr(e)[:200]]}


def handled_ids(body):
    m = GA_FENCE.search(body)
    ids = set()
    if m:
        try:
            for h in json.loads(m.group(1)).get("handled", []):
                if isinstance(h, dict) and h.get("id"):
                    ids.add(h["id"])
        except ValueError:
            pass
    if not ids:
        ids = set(CMD_ID.findall(body[:600]))
    return ids


def scan_issues(now):
    issues = gh(f"repos/{OWNER_REPO}/issues?state=open&per_page=100")
    pending, maybe, checked = [], [], 0
    for iss in issues:
        if "pull_request" in iss:
            continue
        comments = gh(f"repos/{OWNER_REPO}/issues/{iss['number']}/comments?per_page=100")
        posts = [{"body": iss["body"] or "", "url": iss["html_url"], "id": str(iss["id"]),
                  "at": iss["created_at"]}] + [
            {"body": c["body"] or "", "url": c["html_url"], "id": str(c["id"]), "at": c["created_at"]}
            for c in comments]
        for p in posts:
            p["kind"], p["schema"] = kind_of(p["body"])
        for i, p in enumerate(posts):
            if p["kind"] != "report":
                continue
            checked += 1
            ids = handled_ids(p["body"])
            later = [q for q in posts[i + 1:] if q["kind"] == "baseline"]
            matched = [q for q in later
                       if p["id"] in q["body"] or p["url"] in q["body"]
                       or any(re.search(r"(?<![A-Za-z])(?:CMD-)?" + re.escape(x.removeprefix("CMD-")) + r"(?!\d)",
                                        q["body"]) for x in ids)]
            if matched:
                continue
            waited = (now - dt.datetime.fromisoformat(p["at"].replace("Z", "+00:00"))).total_seconds() / 60
            first = p["body"].lstrip().splitlines()[0][:90] if p["body"].strip() else ""
            item = {"issue": iss["number"], "ref": p["url"], "at": p["at"], "waiting_min": round(waited),
                    "ids": sorted(ids), "first_line": first, **header_check(p["body"])}
            (maybe if later else pending).append(item)
    return pending, maybe, checked


# ---------- A1: sessions ----------

def scan_sessions(path):
    data = load_tool_result(path)["data"]
    out = {"working": [], "need_input": [], "blocked_words": [], "idle": [], "unknown_sessions_active": []}
    for c in data:
        sid = c["id"]
        name, src = SESSIONS.get(sid, (None, None))
        updated = c.get("updated_at", "")
        if name is None:
            if c.get("session_status") == "SESSION_STATUS_RUNNING":
                out["unknown_sessions_active"].append({"id": sid, "title": c.get("title", "")[:60]})
            continue
        if name == "AO":
            continue
        pts = c.get("post_turn_summary") or c.get("external_metadata", {}).get("post_turn_summary") or {}
        row = {"name": name, "map": src, "bucket": c.get("status_bucket", "").replace("SESSION_STATUS_BUCKET_", ""),
               "updated": updated[:16], "status_category": pts.get("status_category"),
               "detail": (pts.get("status_detail") or "")[:140], "needs_action": (pts.get("needs_action") or "")[:140]}
        if c.get("session_status") == "SESSION_STATUS_RUNNING":
            out["working"].append(row)
        elif pts.get("status_category") in ("need_input", "failed"):
            out["need_input"].append(row)
        elif BLOCK_WORDS.search(row["detail"] + row["needs_action"]):
            out["blocked_words"].append(row)
        else:
            out["idle"].append({"name": name, "bucket": row["bucket"], "updated": row["updated"]})
    return out


# ---------- A4: W1 ----------

def scan_w1(path, since):
    if not path:
        return {"read": False}
    data = load_tool_result(path).get("data", [])
    tools, denies, grants, reports, newest = 0, {}, 0, 0, since
    for e in data:
        at = e.get("created_at", "")
        if since and at <= since:
            continue
        newest = max(newest or "", at)
        blob = json.dumps(e, ensure_ascii=False)
        if '"tool_use"' in blob:
            tools += blob.count('"type": "tool_use"') + blob.count('"type":"tool_use"')
        for r in re.findall(r"guard DENY\((\w+)\)", blob):
            denies[r] = denies.get(r, 0) + 1
        grants += len(re.findall(r"guard (?:ALLOW|PERMIT)", blob))
        reports += len(re.findall(r"amp/issues/(?:1|14)#issuecomment", blob))
    fresh = [e for e in data if not since or e.get("created_at", "") > since]
    turns = sum(1 for e in fresh if "user" in e or "assistant" in e or "result" in e)
    return {"read": True, "since": since, "new_events": len(fresh), "turn_events": turns,
            "infra_only": len(fresh) - turns,
            "tool_calls": tools, "denies": denies, "grants": grants, "report_links": reports, "newest": newest}


# ---------- A9: HUMAN_QUEUE ----------

def scan_human_queue(baseline_dir):
    subprocess.run(["git", "-C", baseline_dir, "fetch", "-q", "origin", BASELINE_BRANCH], check=True)
    text = subprocess.run(["git", "-C", baseline_dir, "show", f"origin/{BASELINE_BRANCH}:HUMAN_QUEUE.md"],
                          check=True, capture_output=True, text=True).stdout
    sha = subprocess.run(["git", "-C", baseline_dir, "rev-parse", "--short", f"origin/{BASELINE_BRANCH}"],
                         check=True, capture_output=True, text=True).stdout.strip()
    waiting = text.split("## 대기 중", 1)[-1].split("## 끝남", 1)[0]
    rows = []
    for line in waiting.splitlines():
        m = re.match(r"\|\s*(Q\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if m:
            rows.append({"q": m.group(1), "kind": m.group(2).strip(), "task": m.group(3).strip()[:120]})
    return sha, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--sessions", required=True)
    ap.add_argument("--w1")
    ap.add_argument("--baseline-dir", default="/home/user/baseline")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    state_p = ROOT / "state.json"
    state = json.loads(state_p.read_text()) if state_p.exists() else {}

    pending, maybe, checked = scan_issues(now)
    sessions = scan_sessions(a.sessions)
    w1 = scan_w1(a.w1, state.get("w1_since"))
    hq_sha, hq = scan_human_queue(a.baseline_dir)

    status = {
        "schema": "ao-status/1", "round": a.round, "mode": "shadow", "at": now.strftime("%Y-%m-%dT%H:%MZ"),
        "sessions": sessions,
        "pending_reports": pending,
        "answered_without_id_match": maybe,
        "reports_scanned": checked,
        "w1": w1,
        "human_queue": {"baseline_head": hq_sha, "open": hq},
        "not_covered": ["amp#1 (issues API not attached to AO; read-only git only)"],
    }
    out = ROOT / "rounds" / f"round-{a.round:02d}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(status, ensure_ascii=False, indent=1) + "\n")
    if w1.get("read") and w1.get("newest"):
        state["w1_since"] = w1["newest"]
    state["last_round"] = a.round
    state_p.write_text(json.dumps(state, indent=1) + "\n")
    json.dump(status, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
