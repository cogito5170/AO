# Round 2 vs baseline (16:39 UTC; baseline head fcd67e4, BD-241..246)

Run early, at the user's request ("지금 바로 보고해"). The trigger round at 16:40 becomes round 3.

| P | AO saw | baseline (from BD-241..246 and its #-comments) | note |
|---|---|---|---|
| P1 | W1, GMG, Action and Telemetry are need_input; GA, SDK, WUG and baseline are working | BD-245 has WUG blocked on add_repo; BD-246 has the W1 root cause | match. Action and Telemetry have been idle since 10-02; baseline does not list them (they are in wait by design) |
| P2 | 4 pending: WUG #17 16:35, GA #12 16:35, GMG #16 16:23, AMP #14 16:23 | GMG 16:23 matches the BD-241 topic, AMP 16:23 Q2 matches BD-242, but neither comment is linked in DL or answered on its issue | AO counts the 16:23 pair as pending; baseline handled the topics in DL only. Lag for WUG and GA is 4 min (posted after baseline's last commit) |
| P3 | WUG #17 `5971141887`: hard, no leading ```ga head | — | baseline's rule: request a header fix before judging |
| P5 | W1: 0 turns, 1 infra event at 16:36 | BD-246: root cause found from the SDK transcript | match |
| P6 | Q1 open only, at fcd67e4 | BD-242/244: Q5 done, Q1 needs the gmg-net environment | match |
