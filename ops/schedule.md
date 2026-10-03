# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-03 21:19 UTC

Note: the account hit its Claude session limit 18:24–20:10 UTC (GMG, AMP, and AO's 18:40/19:40 rounds did not run). To avoid a repeat, heavy runs are serialized (P8).

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 | CMD-GR8 verdict ([report](https://github.com/cogito5170/baseline/issues/15#issuecomment-5973572832), P3 ok, D1/D2 met) | baseline | **AO's verdict request was not posted:** the permission classifier denied the post (21:18). Waiting on the user | — | — |
| T1 | CMD-GA25 ga rlo pin 3d2e7d0 → 8131a2b, before any upgrade-remote on amp ([#12](https://github.com/cogito5170/baseline/issues/12#issuecomment-5973228433)) | GA | **posted, but GA was not woken:** AO's send_message to GA was denied by the permission classifier. Delivery is the user's call | when GA is woken | small |
| T1 | CMD-K14 S2: rlo uses `extend`, pin Sensor at integration head `f1e45b5` (SEN1 BD-269, SEN2 success BD-271) | SDK | the GR8 report has landed, so the hold is due for release. **The start note was not posted:** same denial at 21:18. Waiting on the user | — | heavy |
| — | Sensor: nothing assigned in POL-1 after SEN2 | — | — | — | — |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump on amp main and `w1/work` | the user OKs in AMP's chat, then AMP | **human: Q8** | — | — |
| T1 | step 2: W1 gets the new files | user (baseline guides) | step 1 | — | — |
| T1 | step 3: P5 success check (a W1 post reaches amp#1, or a send_message reaches AMP) | AO (read only) | step 2 | — | — |
| T2 WUG | CMD-WUG1 S6/S10 | WUG | **human: Q6** (the user types it in WUG's chat) | — | none |
| T3 GMG | CMD-GMG5 rev 2 S4 (calibration from gmg5/refset) | GMG | running ("computing calibration percentiles", 20:53); GMG8 success BD-270 | ~22:00 | none expected |
| T3 | CMD-GMG9 GMG8 follow-ups: launcher GEMINI_CLI_HOME test (V7), 79.5 vs 3.9 KB/turn residual, merge telemetry block, docstring ([#16](https://github.com/cogito5170/baseline/issues/16#issuecomment-5973390104)) | GMG | after GMG5 (issued 20:56, notified with priority later) | after GMG5 | 0 Gemini requests |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | its own trigger | 00:15 | 1 Gemini request |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |
