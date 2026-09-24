# QA Report: stats.py CLI — 2026-09-23

| Field | Value |
|---|---|
| **Target** | `/home/mekl/audit/qa-target/stats.py` (test target, 2 planted bugs) |
| **Commit/SHA** | sha256 `213defd452fd9d3462d38cc31c6edc022f2c8161fa30dadf65631adfaa94380e` |
| **Date** | 2026-09-23 08:45 WIB |
| **Tester** | qa-subagent sa-0-88e133b2 (black-box, source unread) |
| **Parent verified** | 2026-09-23 by nano |
| **Report status** | OBSOLETE (superseded by none — target deleted after test; kept as worked example) |

## Summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 2 |
| Medium | 0 |
| Low | 3 |
| **Total** | **5** |

One-line assessment: happy path solid; all crashes and silent-wrong-answer cases cluster at input edges.

## Issues

### BUG-1: Empty input crashes with ZeroDivisionError

- **Severity:** High — **Category:** functional
- **Status:** VERIFIED

**Repro:**
```
python3 stats.py
```

**Expected:** spec says empty input must work (usage message or defined result)
**Actual:** traceback `ZeroDivisionError: division by zero`, exit 1

**Evidence:**
- `2026-09-23-stats-evidence/bug1-run1.txt` — raw output, exit 1
- `2026-09-23-stats-evidence/bug1-run2.txt` — repro 2/2

**Parent verification:** verified 2026-09-23: repro re-run, exit code 1

**Fix:** -

### BUG-2: Non-numeric input crashes with ValueError

- **Severity:** High — **Category:** functional
- **Status:** VERIFIED

**Repro:**
```
python3 stats.py 1 abc 3
```

**Expected:** spec says non-numeric must be handled (clear error, nonzero-but-clean exit)
**Actual:** traceback `ValueError: could not convert string to float: 'abc'`, exit 1

**Evidence:**
- `2026-09-23-stats-evidence/bug2-run1.txt` — raw output
- `2026-09-23-stats-evidence/bug2-mixed.txt` — mixed valid/invalid args, same crash

**Parent verification:** verified 2026-09-23: repro re-run, exit code 1

**Fix:** -

### BUG-3: --help parsed as number

- **Severity:** Low — **Category:** UX
- **Status:** VERIFIED (parent saw evidence file; consistent with BUG-2 root cause)

**Repro:**
```
python3 stats.py --help
```

**Expected:** usage text
**Actual:** ValueError, exit 1

**Evidence:**
- `2026-09-23-stats-evidence/bug3-help.txt` — raw output

**Parent verification:** -

**Fix:** -

### BUG-4: nan/inf accepted silently

- **Severity:** Low — **Category:** data
- **Status:** VERIFIED (parent saw evidence file)

**Repro:**
```
python3 stats.py nan 1
```

**Expected:** reject non-finite floats
**Actual:** `mean = nan`, exit 0

**Evidence:**
- `2026-09-23-stats-evidence/bug4-nan.txt` — raw output

**Parent verification:** -

**Fix:** -

### BUG-5: Sum overflow → silent wrong answer

- **Severity:** Low — **Category:** data
- **Status:** VERIFIED (parent re-ran: `mean = inf`, exit 0)

**Repro:**
```
python3 stats.py 1e308 1e308
```

**Expected:** detect/handle overflow, or at minimum not print a wrong finite-looking result silently
**Actual:** `mean = inf`, exit 0

**Evidence:**
- `2026-09-23-stats-evidence/bug5-overflow.txt` — raw output

**Parent verification:** verified 2026-09-23: repro re-run, exit code 0

**Fix:** -

## Coverage

**Tested:** ints, floats, negatives, sci-notation, single arg, 1000 args (`seq 1 1000`), whitespace-padded args, empty input, non-numeric input, `--help`, nan/inf, overflow-scale values.

**Not tested:** stdin input path, ARG_MAX-scale arg counts, locale decimal separators.

**Blockers:** none.

## Notes

BUG-2/3 share one root cause (unvalidated float parse); BUG-1 the empty-list division; BUG-4/5 no finite/overflow guards — 3 fixes would close all 5. All findings deterministic, zero flakes. Target was a disposable test rig with 2 planted bugs (BUG-1, BUG-2); the 3 Low bugs were real edges the rig author did not plan.
