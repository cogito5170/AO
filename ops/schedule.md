# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-04 01:59 UTC

Note: the account hit its Claude session limit 18:24–20:10 UTC (GMG, AMP, and AO's 18:40/19:40 rounds did not run). To avoid a repeat, heavy runs are serialized (P8).

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 | CMD-GR8: **success** (BD-272). Baseline judged it directly because AO's request was blocked | — | — | done | — |
| T1 | CMD-GR9 verdict ([report](https://github.com/cogito5170/baseline/issues/15#issuecomment-5975551907): ga-SDK `2c68ea2`, P3 ok, D1/D2 met, 478 passed) | baseline | [verdict request 01:55](https://github.com/cogito5170/baseline/issues/18#issuecomment-5975554694) | — | — |
| T1 | CMD-GA25: pin commit `ff67e8c` held locally (no red push, BD-228). After GR9 is integrated: retarget to `c491e96`, merge, test, push ([hold note](https://github.com/cogito5170/baseline/issues/12#issuecomment-5975409493)) | GA | GR9 | after GR9 | small |
| T1 | CMD-K14 S2: **success** (BD-278). rlo-SDK head `c491e96` (0.8.2); SDK has nothing assigned in POL-1 | — | — | done | — |
| — | Sensor: nothing assigned in POL-1 after SEN2 | — | — | — | — |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump (amp stays on 0.8.1 until W1 is confirmed unblocked, BD-278) | AMP | **done** (BD-275): amp `1584696`, rlo 0.8.1, probes all ALLOW | done | — |
| T1 | step 2: a fresh W1 container (archive+unarchive of the same session, or `!` in W1's chat) | user (baseline guides) | **human** | — | — |
| T1 | step 3: P5 success check (a W1 post reaches amp#1, or a send_message reaches AMP) | AO (read only) | step 2 | — | — |
| T2 WUG | CMD-WUG1 rev 3: partial success (BD-276). Q6 done; D3 is HUMAN_QUEUE **Q10** (the user's Mac run) | — | — | — | — |
| T2 | CMD-WUG2 rev 2: **success**, `cad67de` accepted as is (BD-280). WUG1 D3 grading: exit 0 = met, 6 = partly, 5 = honest unmet, no same-day rerun. WUG has nothing assigned | — | — | done | — |
| T2 | Q10: the user reinstalls the extension, runs `wug.py setup`, then `wug.py d3` (cap 15 in code; stops at the first success after a 429). exit 0 = D3 done | user (baseline lists it) | the 2026-10-05 window, after GMG6 | 10-05 | ≤15 Gemini requests |
| T3 GMG | CMD-GMG5 rev 2: **success** (BD-273) | — | — | done | — |
| T3 | CMD-GMG10 verdict ([report](https://github.com/cogito5170/baseline/issues/16#issuecomment-5975567729): `216efc2`, P3 ok, D1/D2 met, 125/125 mutations) | baseline | [verdict request 01:58](https://github.com/cogito5170/baseline/issues/18#issuecomment-5975569802) | — | — |
| T3 | CMD-GMG9: **success** (BD-274). Baseline judged it under its 60-min rule while Q9 blocks AO; the block B re-pin at `deffd8e` was approved | — | — | done | — |
| T3 | BD-274 follow-ups (block B pinned at `deffd8e`, heap logs, residual wording): GMG reports them **done** at `78d9773` (notified AO 00:22) | baseline to note | — | done (by GMG) | — |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | the 10-04 00:16 run got **429**: the shared key's free tier (20/day, gemini-3-flash) was already spent. Recorded at `905fda3`; GMG booked one retry after 2026-10-05 00:00 UTC | 10-05 00:00+ | **P8: 1 request reserved for this retry.** No other live Gemini calls are scheduled before it |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |

## Quota ledger (P8)

| Pool | Window | Reserved | Note |
|---|---|---|---|
| Gemini API key, free tier, gemini-3-flash-preview (shared by GMG, WUG and every Gemini session) | resets ~00:00 UTC daily | 1 × GMG6 D5/D6 smoke, then the Q10 WUG probe `wug.py d3` (≤15), on 2026-10-05 (~16/20) | 10-04 window exhausted before 00:16; who spent it is not known to AO. The 10-05 plan was posted on #18 and carried in GMG10 and WUG2 |
| agy weekly per-family | weekly | — | never accept AI credits |
