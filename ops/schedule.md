# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-03 18:25 UTC (POL-1 T1 change, BD-267)

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 W1–AMP | CMD-GR7 rev 3 report (#15). Kept as the path for future guard updates to a running session; no longer gates W1 | GR | GR at work (session running 18:12) | not stated | none |
| T1 | CMD-K14 S2 (incremental cache) | SDK | CMD-SEN1 verdict (K14 S1 success, BD-266, rlo 0.8.1 `8131a2b` integrated) | after SEN1 | none |
| T1 | CMD-SEN1 report (#3) | Sensor | mutation harness re-run (session running 18:12) | ~19:00 | none |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump to rlo-SDK `8131a2b` on amp main and `w1/work` | user OK in AMP chat, then AMP | **human:** HUMAN_QUEUE Q8 (guard change, so AO does not direct it) | when the user acts | — |
| T1 | rlo 0.8.1 to W1, step 2: W1 gets the new files (archive+unarchive of the same session, or a `!` command in W1's chat) | user (baseline guides) | step 1 | when the user acts | — |
| T1 | rlo 0.8.1 to W1, step 3: P5 success check. Success = a W1 post reaches amp#1, or a W1 send_message reaches AMP | AO (read only) | step 2 | every round after step 2 | — |
| T1 | P5 W1 observation (no contact, BD-238) | AO | — | every round | — |
| T2 WUG | CMD-WUG1 S6/S10 | WUG | **human:** WUG did not accept the Q6 approval relayed by baseline (17:55); it asks the user to reply in the WUG chat (e.g. "ga-sdk 설치해") | blocked | none (D2 test uses a fake 429 model) |
| T3 GMG | CMD-GMG8 report (#16) | GMG | mutation run (~33% at 17:52) | ~18:45 | none |
| T3 | CMD-GMG5 rev 2 S4 (calibration from gmg5/refset) | GMG | GMG8 first (POL-1 order) | after GMG8 | check before the live calls |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | GMG's own trigger 00:15 UTC | 00:15 | 1 Gemini API request of 20/day |
| T4 GA | GA follow-up: recorded agy shapes | AO issues it | **human:** Q7 (8 Mac runs, #12 5971823866) | after Q7 output | agy weekly share; never accept AI credits |
