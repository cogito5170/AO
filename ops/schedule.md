# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-03 20:40 UTC

Note: the account hit its Claude session limit 18:24–20:10 UTC (GMG, AMP, and AO's 18:40/19:40 rounds did not run). To avoid a repeat, heavy runs are serialized (P8).

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 | CMD-GR8 behavioural tests for chained commands after the pinned `ga mail` ([#15](https://github.com/cogito5170/baseline/issues/15#issuecomment-5973228541)) | GR | issued 20:36, notified | ~1 h | small |
| T1 | CMD-SEN2 tests that kill mutations D/E ([#3](https://github.com/cogito5170/baseline/issues/3#issuecomment-5973228656)) | Sensor | issued 20:36, notified | ~1 h | small |
| T1 | CMD-GA25 ga rlo pin 3d2e7d0 → 8131a2b, before any upgrade-remote on amp ([#12](https://github.com/cogito5170/baseline/issues/12#issuecomment-5973228433)) | GA | **posted, but GA was not woken:** AO's send_message to GA was denied by the permission classifier. Delivery is the user's call | when GA is woken | small |
| T1 | CMD-K14 S2: rlo uses `extend`, pin Sensor `b705574` (unblocked by SEN1, BD-269) | SDK | AO holds it until GR8/SEN2 report (serialized; the last SDK turn cost ~$89) | after GR8/SEN2 | heavy |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump on amp main and `w1/work` | the user OKs in AMP's chat, then AMP | **human: Q8** | — | — |
| T1 | step 2: W1 gets the new files | user (baseline guides) | step 1 | — | — |
| T1 | step 3: P5 success check (a W1 post reaches amp#1, or a send_message reaches AMP) | AO (read only) | step 2 | — | — |
| T2 WUG | CMD-WUG1 S6/S10 | WUG | **human: Q6** (the user types it in WUG's chat) | — | none |
| T3 GMG | CMD-GMG8 verdict (report at [18:21](https://github.com/cogito5170/baseline/issues/16#issuecomment-5972122079), P3 ok) | baseline | baseline said "GMG8 verdict follows" | — | — |
| T3 | CMD-GMG5 rev 2 S4 (calibration from gmg5/refset) | GMG | GMG8 verdict; GMG hit the session limit at 18:24 | after GMG8 | Gemini 20/day shared |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | its own trigger | 00:15 | 1 Gemini request |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |
