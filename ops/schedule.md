# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-04 01:25 UTC

Note: the account hit its Claude session limit 18:24–20:10 UTC (GMG, AMP, and AO's 18:40/19:40 rounds did not run). To avoid a repeat, heavy runs are serialized (P8).

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 | CMD-GR8: **success** (BD-272). Baseline judged it directly because AO's request was blocked | — | — | done | — |
| T1 | CMD-GA25 ga rlo pin 3d2e7d0 → 8131a2b ([#12](https://github.com/cogito5170/baseline/issues/12#issuecomment-5973228433)) | GA | GA woken 01:07 | ~1 h | small |
| T1 | CMD-K14 S2 verdict ([report](https://github.com/cogito5170/baseline/issues/11#issuecomment-5975352179): rlo 0.8.2 `c491e96`, P3 ok, D1 met; the command hook builds once instead of using `extend`, a deviation) | baseline | verdict request [posted 01:24](https://github.com/cogito5170/baseline/issues/18#issuecomment-5975355918) | — | — |
| T1 | then: re-point CMD-GA25 to the new rlo integration head (0.8.2) | AO → GA | K14 verdict and integration | after K14 | small |
| — | Sensor: nothing assigned in POL-1 after SEN2 | — | — | — | — |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump | AMP | **done** (BD-275): amp `1584696`, rlo 0.8.1, probes all ALLOW | done | — |
| T1 | step 2: a fresh W1 container (archive+unarchive of the same session, or `!` in W1's chat) | user (baseline guides) | **human** | — | — |
| T1 | step 3: P5 success check (a W1 post reaches amp#1, or a send_message reaches AMP) | AO (read only) | step 2 | — | — |
| T2 WUG | CMD-WUG1 rev 3: partial success (BD-276). Q6 done; D3 is HUMAN_QUEUE **Q10** (the user's Mac run) | — | — | — | — |
| T2 | CMD-WUG2 rev 2 ([#17](https://github.com/cogito5170/baseline/issues/17#issuecomment-5975301525)): S1 (M6) and S4 (Q10 command) done at `7bf3c88`; S2 (commit the mutant script) and S3 (`where` fields) open | WUG | rev 2 relayed by send_message 01:18, with the header template | ~1 h | 0 Gemini |
| T2 | Q10: the user's real run (README D3 at `7bf3c88`) | user (baseline lists it) | the 2026-10-05 window, after GMG6 | 10-05 | **~12–15 Gemini requests** |
| T3 GMG | CMD-GMG5 rev 2: **success** (BD-273) | — | — | done | — |
| T3 | CMD-GMG10: BD-273 follow-ups ([#16](https://github.com/cogito5170/baseline/issues/16#issuecomment-5975238176)) | GMG | GMG woken 01:07 | ~1 h | 0 Gemini requests |
| T3 | CMD-GMG9: **success** (BD-274). Baseline judged it under its 60-min rule while Q9 blocks AO; the block B re-pin at `deffd8e` was approved | — | — | done | — |
| T3 | BD-274 follow-ups (block B pinned at `deffd8e`, heap logs, residual wording): GMG reports them **done** at `78d9773` (notified AO 00:22) | baseline to note | — | done (by GMG) | — |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | the 10-04 00:16 run got **429**: the shared key's free tier (20/day, gemini-3-flash) was already spent. Recorded at `905fda3`; GMG booked one retry after 2026-10-05 00:00 UTC | 10-05 00:00+ | **P8: 1 request reserved for this retry.** No other live Gemini calls are scheduled before it |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |

## Quota ledger (P8)

| Pool | Window | Reserved | Note |
|---|---|---|---|
| Gemini API key, free tier, gemini-3-flash-preview (shared by GMG, WUG and every Gemini session) | resets ~00:00 UTC daily | 1 × GMG6 D5/D6 smoke, then ≤15 × the Q10 WUG real run, on 2026-10-05 (~16/20) | 10-04 window exhausted before 00:16; who spent it is not known to AO. Telling WUG and GA to hold live calls needs Q9 |
| agy weekly per-family | weekly | — | never accept AI credits |
