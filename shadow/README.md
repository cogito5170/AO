# AO P1 shadow (BD-243)

Read-only rounds. Each round posts one `ao-status/1` on baseline#18; nothing is sent to any session.
Covers A1 session watch, A2 pending-report queue, A3 header pre-check (`ga.forms.parse_post`, ga-SDK 102e48a),
A4 W1 read-only count, A9 HUMAN_QUEUE open items. Skips A5–A8.

Run: fetch `list_sessions(mine)` and `list_events(W1)` via MCP to files, then
`python3 shadow/round.py --round N --sessions <file> --w1 <file>` → `rounds/round-NN.json`.

Pending rule: a session report (``` ga report head, or `[Session]` head) is pending when no later baseline post
in the same issue links it or names one of its handled ids (with or without `CMD-`). Later baseline posts
without such a match are listed separately (`answered_without_id_match`) — the BD-180 masking case — not dropped.
