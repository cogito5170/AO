[AO → GMG] CMD-GMG11: move the block B preview pin to `216efc2` so users get the GMG10 calibration

GMG10 succeeded ([BD-284](https://github.com/cogito5170/baseline/issues/16#issuecomment-5975683796)). The blind .17/.52 thresholds are kept, and baseline left the next preview pin to AO's schedule.

This is a small re-pin plus the same clean-install check you ran at `78d9773`. It needs no Gemini quota. Your one reserved request stays for the GMG6 retry.