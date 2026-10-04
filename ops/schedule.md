# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-04 00:24 UTC

Note: the account hit its Claude session limit 18:24–20:10 UTC (GMG, AMP, and AO's 18:40/19:40 rounds did not run). To avoid a repeat, heavy runs are serialized (P8).

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 | CMD-GR8: **success** (BD-272). Baseline judged it directly because AO's request was blocked | — | — | done | — |
| T1 | CMD-GA25 ga rlo pin 3d2e7d0 → 8131a2b, before any upgrade-remote on amp ([#12](https://github.com/cogito5170/baseline/issues/12#issuecomment-5973228433)) | GA | **posted, but GA was not woken:** AO's send_message to GA was denied by the permission classifier. Delivery is the user's call | when GA is woken | small |
| T1 | CMD-K14 S2: rlo uses `extend`, pin Sensor at integration head `f1e45b5` (SEN1 BD-269, SEN2 success BD-271) | SDK | ready (GR8 success). **The start note is blocked:** HUMAN_QUEUE Q9, AO's write permission, is the user's decision | after Q9 | heavy |
| — | Sensor: nothing assigned in POL-1 after SEN2 | — | — | — | — |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump on amp main and `w1/work` | the user OKs in AMP's chat, then AMP | **human: Q8** | — | — |
| T1 | step 2: W1 gets the new files | user (baseline guides) | step 1 | — | — |
| T1 | step 3: P5 success check (a W1 post reaches amp#1, or a send_message reaches AMP) | AO (read only) | step 2 | — | — |
| T2 WUG | CMD-WUG1 S6/S10 | WUG | **human: Q6** (the user types it in WUG's chat) | — | none |
| T3 GMG | CMD-GMG5 rev 2: **success** (BD-273) | — | — | done | — |
| T3 | GMG5 follow-ups (BD-273), to bundle as the next GMG directive after GMG9: (1) a test pinning the log sharpness scale; (2) commit the mood half-split script (.41/.58 → .50/.58); (3) correct the margin wording; (4) optional: re-choose thresholds blind, near .17 / .52 | AO issues | **Q9** (AO write permission), then after GMG9 | after Q9 | 0 Gemini |
| T3 | CMD-GMG9: **success** (BD-274). Baseline judged it under its 60-min rule while Q9 blocks AO; the block B re-pin at `deffd8e` was approved | — | — | done | — |
| T3 | BD-274 follow-ups (block B pinned at `deffd8e`, heap logs, residual wording): GMG reports them **done** at `78d9773` (notified AO 00:22) | baseline to note | — | done (by GMG) | — |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | the 10-04 00:16 run got **429**: the shared key's free tier (20/day, gemini-3-flash) was already spent. Recorded at `905fda3`; GMG booked one retry after 2026-10-05 00:00 UTC | 10-05 00:00+ | **P8: 1 request reserved for this retry.** No other live Gemini calls are scheduled before it |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |

## Quota ledger (P8)

| Pool | Window | Reserved | Note |
|---|---|---|---|
| Gemini API key, free tier, gemini-3-flash-preview (shared by GMG, WUG and every Gemini session) | resets ~00:00 UTC daily | 1 × GMG6 D5/D6 smoke on 2026-10-05 | 10-04 window exhausted before 00:16; who spent it is not known to AO. Telling WUG and GA to hold live calls needs Q9 |
| agy weekly per-family | weekly | — | never accept AI credits |
