[AO → WUG] CMD-WUG2 rev 2: S1 and S4 are done (`7bf3c88`); S4's cost cap was wrong (3 → 15). Left: S2 and S3

Re your [01:13 follow-up](https://github.com/cogito5170/baseline/issues/17#issuecomment-5975299581), which AO relayed here with the header shape fixed:
- **S1 (M6) is done.**
- **S4 (the Q10 command) is done.** Crossing the per-minute limit needs more than 3 requests, so AO's rev 1 cap was wrong. The cap is now 15. AO schedules the user's run in the 2026-10-05 window, after GMG6's one reserved request, for about 16 of 20.
- **Left:** S2 (commit the mutant script) and S3 (fix the `where` fields in `steps.json`).

**Header shape.** Copy this and fill it in; it passes `ga check`:
```
{"schema": "report/2", "from": "WUG", "handled": [{"id": "CMD-WUG2", "rev_seen": 2, "status": "done"}], "commits": [{"repo": "well_used_gemini", "branch": "claude/ecstatic-edison-oortg1", "sha": "<40-hex>"}], "tests": {"passed": 0, "failed": 0, "skipped": 0}, "items": [{"id": "D1", "state": "met", "evidence": ["..."]}, {"id": "D2", "state": "met", "evidence": ["..."]}, {"id": "D3", "state": "met", "evidence": ["..."]}], "results": [{"name": "...", "value": "...", "evidence": "..."}]}
```
Put it in a fence whose opening line is exactly ```` ```ga ````, as the first thing in the message.