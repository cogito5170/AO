# Schedule — POL-2 (CMD-AO3 rev 4, BD-288 to BD-291). Updated 2026-10-04 15:38 UTC (BD-294: Gemini billing on, free tier gone)

POL-2 cuts token usage with our own prompt language, prompt-spec/1 (baseline PROMPT_SPEC.md, b9e7669). One *.pspec file yields the prompt (verbatim or compact), the checker and a token report. Prompt-quality optimization (variant search) is out (BD-290). Limits (S5):
- No built-in quota in the SDK or ga.
- Paid billing stays the user's call (BD-242).
- No AI credits and no secrets.
- A changed prompt lands only through a baseline verdict.

| Track | Next step | Owner | Waiting on | ETA (est.) | Model calls |
|---|---|---|---|---|---|
| POL-2 T1 | CMD-K15 rev 4: **success** (BD-292). rlo-sdk `6bc76c7` (0.9.0) integrated; P1–P3 accepted, P4 docs, P5 deferred | — | — | done | none |
| POL-2 T1 | CMD-K16: **success** (BD-293). rlo-sdk `3e68f21` (0.9.1); `{% use %}` scoping accepted (PROMPT_SPEC §2) | — | — | done | none |
| POL-2 T2 | CMD-GA26 ([#12](https://github.com/cogito5170/baseline/issues/12#issuecomment-5980705305)): gemini prompts on prompt-spec/1, pinned to rlo `6bc76c7`; verbatim byte-identical, compact on follow-up turns (agy included), token report on ≥8 turns per host, 17-case agreement (16/17 until K16) | GA | reported 14:59 at ga `da8b617` on rlo 0.9.0 (16/17); **returned 15:01** ([#12 5981331645](https://github.com/cogito5170/baseline/issues/12#issuecomment-5981331645)): re-pin to `3e68f21` and show 17/17 | follow-up report | none required |
| POL-2 T2 | K16 sha `3e68f21` posted on #12 ([5980865023](https://github.com/cogito5170/baseline/issues/12#issuecomment-5980865023)) and GA notified 14:09; GA re-pins and shows 17/17 | GA | — | — | — |
| POL-2 T3 | the biggest spenders from the T2 token report | — | a new POL-2 line from baseline | — | — |

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
| T2 | Q10: the user reinstalls the extension, runs `wug.py setup`, then `wug.py d3`. exit 0 = D3 done. **Any time now (BD-294)**, no longer after 00:00 UTC | user (baseline lists it) | human | — | billed; ≤15 requests capped in code |
| T3 GMG | CMD-GMG5 rev 2: **success** (BD-273) | — | — | done | — |
| T3 | CMD-GMG10: **success** (BD-284); the blind thresholds .17/.52 are kept | — | — | done | — |
| T3 | CMD-GMG11: **success** (BD-285). Block B is at `216efc2`; GMG has nothing assigned except the GMG6 retry | — | — | done | — |
| T3 | CMD-GMG9: **success** (BD-274). Baseline judged it under its 60-min rule while Q9 blocks AO; the block B re-pin at `deffd8e` was approved | — | — | done | — |
| T3 | BD-274 follow-ups (block B pinned at `deffd8e`, heap logs, residual wording): GMG reports them **done** at `78d9773` (notified AO 00:22) | baseline to note | — | done (by GMG) | — |
| T3 | CMD-GMG6 D5/D6 smoke: **reported 15:35** at `057ef4f`: OK, served gemini-3-flash-preview, 1 request (11,822 input tokens). Verdict request [#18 5981662349](https://github.com/cogito5170/baseline/issues/18#issuecomment-5981662349) | baseline | the GMG6 verdict | — | 1 request, spent |
| T4 GA | GA follow-up with recorded agy shapes | AO issues | **human: Q7** (8 Mac runs) | — | agy weekly; never AI credits |

## Quota ledger (P8)

BD-294 (14:59 10-04): the user turned on billing for the Gemini key. The free tier (20/day, BD-242) no longer limits scheduling. Cost scales with requests. Spending caps and alerts live in the user's Google Cloud billing, not in any session. AO keeps live runs to what a directive asks for (no retry loops). agy AI credits stay off.
