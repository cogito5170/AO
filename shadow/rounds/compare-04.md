# Round 4 vs baseline (17:40 UTC; baseline head 51d7d89, BD-247..262)

| P | AO saw | baseline | note |
|---|---|---|---|
| P1 | need_input: W1 (guard denied the AMP probe reply), WUG (blocked on the ga-sdk install), baseline (Q6), Action. Working: GR, GMG, GA, SDK, Sensor | BD-252, BD-260, Q6 | match |
| P2 | 2 open on #17: 17:30 relay (hard head) and 17:33 normalized relay | BD-260 (17:32) records CMD-WUG1 rev 3 as partial success in DECISION_LOG. On #17, the only post is the normalized relay; there is no verdict comment linking either report | open under S8 rev 2, because DL alone does not count. Wait is 7–10 min, under 30, so no notify |
| P3 | 17:30 relay: hard (`handled` required; unknown `id` and `rev`) | BD-260: "relay header normalized by baseline", then the 17:33 post passes | match. Baseline fixed it 3 min after posting |
| P5 | W1, 16:36–16:44: 26 turn events, 5 tool calls, denies A1×8 and D×4, 2 report links | BD-248/249/252: the live probe ran; receive works, every send is denied by D | match. AO's count lags baseline by ~56 min (16:44 → 17:40), because AO runs once an hour |
| P6 | open: Q6 at 51d7d89 | Q1 done (BD-251), Q6 added | match |

False positives: none. Missed: none found.
