# QA Report: {AREA} — {YYYY-MM-DD}

| Field | Value |
|---|---|
| **Target** | {app/CLI/repo + version or path} |
| **Commit/SHA** | {git sha or file sha256, or `n/a`} |
| **Date** | {YYYY-MM-DD HH:MM TZ} |
| **Tester** | qa-subagent {subagent_id} (black-box) |
| **Parent verified** | {date} by nano |
| **Report status** | {OPEN / ALL FIXED / OBSOLETE (superseded by <file>)} |

## Summary

| Severity | Count |
|---|---|
| Critical | {n} |
| High | {n} |
| Medium | {n} |
| Low | {n} |
| **Total** | **{n}** |

One-line assessment: {what state is the target in}

## Issues

<!-- One section per issue, Critical first. Copy the block. -->

### BUG-{n}: {short title}

- **Severity:** {Critical/High/Medium/Low} — **Category:** {functional/data/UX/docs}
- **Status:** {UNVERIFIED / VERIFIED / FIXED (re-tested {date}) / STILL BROKEN ({date}) / WONTFIX ({reason})}

**Repro:**
```
{exact command(s) / click path}
```

**Expected:** {what should happen}
**Actual:** {what happens}

**Evidence:**
- `{evidence-relative-path}` — {one line: what it shows}

**Parent verification:** {`verified {date}: repro re-run, exit code N` or `-`}

**Fix:** {`-` until fixed, then: what changed, commit/sha, re-test result}

<!-- END issue block -->

## Coverage

**Tested:** {bullet list: flows/inputs exercised}
**Not tested:** {bullet list: areas out of scope or skipped, and why}
**Blockers:** {anything that stopped testing, or `none`}

## Notes

{patterns observed, recommendations, or `-`}
