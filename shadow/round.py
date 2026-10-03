"""AO P1 shadow round (BD-243), Operator(Hub) per HUB_CLASSES.md (BD-244):
P1 watch, P2 collect, P3 header pre-check, P5 W1 observe (read-only), P6 human-queue check.

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
    """P3. CMD-AO1 S8: a relay post ('[X → baseline]', posted by baseline on a
    session's behalf) carries the ``` ga block anywhere, so validate the first
    embedded block wherever it is."""
    m = GA_FENCE.search(body)
    if not m:
        return {"head": "missing"}
    try:
        doc = json.loads(m.group(1))
    except ValueError as e:
        return {"head": "hard", "problems": [f"unparsable ga block: {e}"[:200]]}
    try:
        probs = forms.validate(doc)
    except Exception as e:  # validator bug must not stop the round
        return {"head": "error", "problems": [repr(e)[:200]]}
    hard = [f"{x.path}: {x.message}" for x in probs if x.strength == "hard"]
    soft = [f"{x.path}: {x.message}" for x in probs if x.strength != "hard"]
    leading = body.lstrip().startswith("```ga")
    out = {"head": "hard" if hard else "ok", "embedded": not leading}
    if hard:
        out["problems"] = hard
    if soft:
        out["soft"] = soft
    return out


DISPOSITIONS = {d["ref"]: d["disposition"] for d in
                json.loads((ROOT / "dispositions.json").read_text())["items"]}


def handled_revs(body):
    m = GA_FENCE.search(body)
    out = {}
    if m:
        try:
            for h in json.loads(m.group(1)).get("handled", []):
                if isinstance(h, dict) and h.get("id") and isinstance(h.get("rev_seen"), int):
                    out[h["id"]] = h["rev_seen"]
        except ValueError:
            pass
    return out


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
            # CMD-AO1 rev 2 S8: answered when a later same-channel baseline post
            # links it, quotes it, or names one of its handled CMD ids (with the
            # rev when the report names one); a status note without an id needs a
            # link/quote or a baseline disposition entry on #18.
            quotes = [ln.strip() for ln in p["body"].splitlines() if len(ln.strip()) >= 60]
            revs = handled_revs(p["body"])

            def names(text):
                # "with the rev when the report names one": a mention that carries a
                # rev must carry the report's rev; a mention without a rev counts.
                for x in ids:
                    pat = r"(?<![A-Za-z])(?:CMD-)?" + re.escape(x.removeprefix("CMD-")) + r"(?!\d)(?P<tail>[^\n]{0,24})"
                    for m in re.finditer(pat, text):
                        r = re.match(r"\W{0,3}rev\.? ?(\d+)", m.group("tail"))
                        if revs.get(x) is None or r is None or int(r.group(1)) == revs[x]:
                            return True
                return False
            matched = [q for q in later
                       if p["id"] in q["body"] or p["url"] in q["body"]
                       or any(ln in q["body"] for ln in quotes) or names(q["body"])]
            if not matched and p["url"] in DISPOSITIONS:
                continue
            by_id = matched
            if matched:
                continue
            waited = (now - dt.datetime.fromisoformat(p["at"].replace("Z", "+00:00"))).total_seconds() / 60
            first = p["body"].lstrip().splitlines()[0][:90] if p["body"].strip() else ""
            item = {"issue": iss["number"], "ref": p["url"], "at": p["at"], "waiting_min": round(waited),
                    "ids": sorted(ids), "first_line": first, **header_check(p["body"])}
            item["named_by_later_baseline_post"] = bool(by_id)
            pending.append(item)
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
        "class": "Operator(Hub)",
        "P1_watch": sessions,
        "P2_collect": {"pending_reports": pending, "reports_scanned": checked, "rule": "CMD-AO1 rev 2 S8"},
        "P3_header": "per item in P2_collect (head: ok | hard | missing)",
        "P5_observe_w1": w1,
        "P6_human_queue": {"baseline_head": hq_sha, "open": hq},
    }
    prev_p = ROOT / "rounds" / f"round-{a.round - 1:02d}.json"
    prev = json.loads(prev_p.read_text()) if prev_p.exists() else None
    post, notify = to_report2(status, prev)
    (ROOT / "rounds" / f"post-{a.round:02d}.md").write_text(post + "\n")
    status["needs_notify"] = notify
    out = ROOT / "rounds" / f"round-{a.round:02d}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(status, ensure_ascii=False, indent=1) + "\n")
    if w1.get("read") and w1.get("newest"):
        state["w1_since"] = w1["newest"]
    state["last_round"] = a.round
    state_p.write_text(json.dumps(state, indent=1) + "\n")
    json.dump(status, sys.stdout, ensure_ascii=False, indent=1)



# ---------- CMD-AO1 S6/S7: the post is a report/2 ----------

def to_report2(status, prev=None, rev_seen=2):
    """Wrap ao-status in report/2 (S6). Return (text, needs_notify).
    A quiet round (nothing changed since prev) is one line (S7)."""
    p1, p2 = status["P1_watch"], status["P2_collect"]
    pend = p2["pending_reports"]
    unnamed = pend  # rev 2 S8: named ids count as answered, so all remaining are open
    hard = [x for x in unnamed if x.get("head") == "hard"]
    w1, hq = status["P5_observe_w1"], status["P6_human_queue"]
    sig = {"need_input": sorted(r["name"] for r in p1["need_input"]),
           "pending": sorted(x["ref"] for x in pend), "hard": sorted(x["ref"] for x in hard),
           "w1": w1.get("turn_events", 0), "hq": sorted(q["q"] for q in hq["open"])}
    status["signature"] = sig
    if prev and prev.get("signature") == sig:
        return f"<AO> round {status['round']}: no change", False
    over30 = [x for x in unnamed if x["waiting_min"] > 30]
    head = {
        "schema": "report/2", "from": "AO",
        "handled": [{"id": "CMD-AO1", "rev_seen": rev_seen, "status": "done"}],
        "items": [
            {"id": "D1", "state": "met", "evidence": [f"P1 watch: need_input {sig['need_input']}"]},
            {"id": "D2", "state": "met", "evidence": [f"P2 collect (S8 rev 2): {len(pend)} open"]},
            {"id": "D3", "state": "met", "evidence": [f"P3 header: {len(hard)} hard among unnamed pending"]},
            {"id": "D4", "state": "met", "evidence": [f"P5 W1: {w1.get('turn_events', 0)} turns since {w1.get('since')}"]},
            {"id": "D5", "state": "met", "evidence": [f"P6 human queue open {sig['hq']} at {hq['baseline_head']}"]},
        ],
        "results": [
            {"name": "reports_scanned", "value": p2["reports_scanned"], "unit": "reports", "evidence": f"round-{status['round']:02d}.json"},
            {"name": "pending", "value": len(pend), "unit": "reports", "evidence": "CMD-AO1 rev 2 S8"},
            {"name": "pending_over_30min", "value": len(over30), "unit": "reports", "evidence": "S5 notify trigger"},
        ],
    }
    probs = forms.validate(head)
    assert not forms.hard(probs), probs
    lines = [f"## <AO> round {status['round']} (shadow, Operator) — " + ("needs a look" if over30 else "no reply needed"), ""]
    if unnamed:
        lines.append("**Open (not linked, quoted, named or disposed by baseline):**")
        lines += [f"- #{x['issue']} {x['at'][5:16]} ({x['waiting_min']} min) head={x['head']} {x['ref']}" for x in unnamed[:12]]
    if hard:
        lines.append("**P3 hard heads among them:**")
        lines += [f"- {x['ref']}: {'; '.join(x.get('problems', []))[:160]}" for x in hard[:8]]
    lines.append(f"**P1** need_input: {', '.join(sig['need_input']) or 'none'} · **P5** W1 turns: {sig['w1']} · **P6** open: {', '.join(sig['hq']) or 'none'}")
    body = "```ga\n" + json.dumps(head, ensure_ascii=False) + "\n```\n" + "\n".join(lines)
    body += "\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_"
    return body, bool(over30)


if __name__ == "__main__":
    main()
