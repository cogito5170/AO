# Schedule — POL-2 (CMD-AO3 rev 2, BD-288/289). Updated 2026-10-04 13:20 UTC

POL-2 compiles prompts from a semantic spec and optimizes them. Its limits (S5, rev 2):
- No quota is built into the SDK or ga: the caller passes a budget and a Governor if it wants one.
- Paid billing on our own key stays the user's call (BD-242).
- No AI credits and no secrets.
- No automatic prompt deploys: a changed prompt lands only through a baseline verdict.

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| POL-2 T1 | CMD-K15 rev 2 ([#11](https://github.com/cogito5170/baseline/issues/11#issuecomment-5980318265)): prompt-spec/1, a deterministic compiler and checker, rlo.optimize (optional budget/Governor, no default cap) | SDK | — (rev 1 at 13:08, rev 2 at 13:14, notified) | report next | none (offline tests, fake model) |
| POL-2 T1 | verdict request on #18 after P3 | AO, then baseline judges | K15 report | — | — |
| POL-2 T2 | CMD-GA26: the `ga gemini` plan prompt as a spec (byte-identical base) and `ga optimize gemini-plan` (≥8 labelled cases, ≥3 held out), one real run | AO issues to GA (#12) | **T1 judged a success** | after T1 | the budget GA passes to `ga optimize`. On our own free key, AO books the real run into a window that does not take GMG6's or Q10's share on 10-05 (16/20 reserved) |
| POL-2 T3 | session-start, GMG and WUG prompts move to prompt-spec/1 | — | a new POL-2 line from baseline, after T2 | — | — |

# Schedule — POL-1 (CMD-AO2, BD-263). Updated 2026-10-04 02:34 UTC: POL-1 directives are done (BD-286). Only human items and the GMG6 retry remain

Note: the account hit its Claude session limit 18:24–20:10 UTC (GMG, AMP, and AO's 18:40/19:40 rounds did not run). To avoid a repeat, heavy runs are serialized (P8).

| Track | Next step | Owner | Waiting on | ETA (est.) | Quota |
|---|---|---|---|---|---|
| T1 | CMD-GR8: **success** (BD-272). Baseline judged it directly because AO's request was blocked | — | — | done | — |
| T1 | CMD-GR9: **success** (BD-283). ga-SDK head `2c68ea2`; GR has nothing assigned in POL-1 | — | — | done | — |
| T1 | CMD-GA25 rev 2: **success** (BD-286). ga-SDK head `438a34a` pins rlo 0.8.2 | — | — | done | — |
| T1 | CMD-K14 S2: **success** (BD-278). rlo-SDK head `c491e96` (0.8.2); SDK has nothing assigned in POL-1 | — | — | done | — |
| — | Sensor: nothing assigned in POL-1 after SEN2 | — | — | — | — |
| T1 | rlo 0.8.1 to W1, step 1: PIN bump (amp stays on 0.8.1 until W1 is confirmed unblocked, BD-278) | AMP | **done** (BD-275): amp `1584696`, rlo 0.8.1, probes all ALLOW | done | — |
| T1 | step 2: a fresh W1 container (archive+unarchive of the same session, or `!` in W1's chat) | user (baseline guides) | **human** | — | — |
| T1 | step 3: P5 success check (a W1 post reaches amp#1, or a send_message reaches AMP) | AO (read only) | step 2 | — | — |
| T2 WUG | CMD-WUG1 rev 3: partial success (BD-276). Q6 done; D3 is HUMAN_QUEUE **Q10** (the user's Mac run) | — | — | — | — |
| T2 | CMD-WUG2 rev 2: **success**, `cad67de` accepted as is (BD-280). WUG1 D3 grading: exit 0 = met, 6 = partly, 5 = honest unmet, no same-day rerun. WUG has nothing assigned | — | — | done | — |
| T2 | Q10: the user reinstalls the extension, runs `wug.py setup`, then `wug.py d3` (cap 15 in code; stops at the first success after a 429). exit 0 = D3 done | user (baseline lists it) | the 2026-10-05 window, after GMG6 | 10-05 | ≤15 Gemini requests |
| T3 GMG | CMD-GMG5 rev 2: **success** (BD-273) | — | — | done | — |
| T3 | CMD-GMG10: **success** (BD-284); the blind thresholds .17/.52 are kept | — | — | done | — |
| T3 | CMD-GMG11: **success** (BD-285). Block B is at `216efc2`; GMG has nothing assigned except the GMG6 retry | — | — | done | — |
| T3 | CMD-GMG9: **success** (BD-274). Baseline judged it under its 60-min rule while Q9 blocks AO; the block B re-pin at `deffd8e` was approved | — | — | done | — |
| T3 | BD-274 follow-ups (block B pinned at `deffd8e`, heap logs, residual wording): GMG reports them **done** at `78d9773` (notified AO 00:22) | baseline to note | — | done (by GMG) | — |
| T3 | CMD-GMG6 D5/D6 smoke | GMG | the 10-04 00:16 run got **429**: the shared key's free tier (20/day, gemini-3-flash) was already spent. Recorded at `905fda3`; GMG booked one retry at 2026-10-05 00:20 UTC, on the 7207edd install | 10-05 00:00+ | **P8: 1 request reserved for this retry.** No other live Gemini calls are scheduled before it |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |

## Quota ledger (P8)

| Pool | Window | Reserved | Note |
|---|---|---|---|
| Gemini API key, free tier, gemini-3-flash-preview (shared by GMG, WUG and every Gemini session) | resets ~00:00 UTC daily | 1 × GMG6 D5/D6 smoke, then the Q10 WUG probe `wug.py d3` (≤15), on 2026-10-05 (~16/20) | 10-04 window exhausted before 00:16; who spent it is not known to AO. The 10-05 plan was posted on #18 and carried in GMG10 and WUG2 |
| agy weekly per-family | weekly | — | never accept AI credits |
| POL-2 T2 real run (same Gemini pool, when run on our own key) | daily | T1: none. T2: the budget passed on the command line; booked so it does not take GMG6's or Q10's share | CMD-AO3 rev 2 S5: no built-in cap. Paid billing is the user's call via baseline |
