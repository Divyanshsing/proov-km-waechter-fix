# What I checked, and what the agent got wrong

## What the agent got wrong

The agent initially could not run the tests at all because the macOS system Python
(`/usr/bin/python3`) is gated behind Xcode Command Line Tools, which require a GUI
dialog click that an automated agent cannot trigger. I had to ask the agent to find a
workaround — it downloaded a standalone CPython build from the
python-build-standalone project, which bypasses the CLT requirement entirely. That
step was not in its first plan and required a follow-up prompt to resolve.

On the first pass the agent also declared the work "done" before actually executing
the tests, then had to walk that back and show real pytest output in a second attempt.
I only accepted the result once I saw the `4 passed in 0.07s` line with the real
Python version in the header.

## What I checked before I accepted the work

1. Ran `pytest test_km_wachter.py test_fleet_report.py -v` and verified all 4 tests
   show PASSED (not just "no failures reported").
2. Ran `python verify.py` and confirmed 9/11 checks passed after the bug fixes, then
   11/11 after analyze.py and NOTES.md were added.
3. Checked that `SERVICE_INTERVAL_KM` is still `15000` and `WARN_AT_PERCENT` is still
   `80` in the source — the agent's job was to fix the floor-division bug, not change
   the thresholds. Both constants are untouched.
4. Verified the km-to-miles fix manually: `0.621371 × 100 = 62.14`, which falls in the
   `61.0–63.5` range the verify script checks for.
5. Read the diff for `needs_service` to confirm the old `car.get("last_service_km", 0)`
   default was replaced with an explicit key-presence check, not just a different
   default value.

## What the data actually said

The obvious assumption — that older, higher-mileage cars break down more — is simply
not in this dataset. `odometer_km` has a Pearson correlation of r = 0.002 with
`broke_down`, and `age_years` is r = −0.001. Both are essentially zero; knowing a
car's total mileage or age tells you almost nothing about whether it will break.

The real signals are:
- `km_since_service` (r = 0.40): cars that have gone far past their last service are
  much more likely to break. This makes mechanical sense — overdue servicing is a
  direct risk factor.
- `avg_daily_km` (r = 0.25): cars driven harder every day accumulate stress faster.

The risk score built from just those two columns identifies 14 of the 26 cars that
actually broke down within the top-20 highest-risk slots — a 70% hit rate versus a
22% baseline, which is 3.2x better than random selection. That is the number that
matters when deciding which cars to pull in for an early service check.
