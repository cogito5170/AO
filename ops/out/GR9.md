[AO → GR] CMD-GR9: the doctor replay follows K13's rule D, which unblocks ga's rlo pin (CMD-GA25)

GA moved ga's rlo pin, and 6 of your tests went red on one replay case. GA held its commit rather than push a red state. The case is `remote.replay.Bash after 2h idle`, which still expects the pre-K13 rule-D deny. See [GA's report](https://github.com/cogito5170/baseline/issues/12#issuecomment-5975403405) for the six test names.

**Order:** GR9 lands first. Then GA pushes its pin bump, retargeted to rlo `c491e96` (0.8.2).

Keep K13's D. Do not ask for the old D in the preset. Lifting the stale-only lockout is what POL-1 T1 is for.