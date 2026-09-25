---
name: qa-subagent
version: 1.0.0
description: "Spawn QA subagents: evidence-first testing, read-only."
---

# QA Subagent (evidence-first, read-only)

Spawn a QA/testing subagent that hunts bugs in a running app and reports
evidence. Role separation rule: the QA child TESTS, the parent (or a separate
coding-subagent task) FIXES. One agent doing both marks its own homework.

## Rule

Every QA task sent to `delegate_task` MUST open its `context` with this block:

```
QA PRINCIPLES (mandatory, follow strictly):
1. Fresh eyes - explore as a real user first; test observed behavior, not the
   source. Read code only afterwards, to help locate a confirmed bug's cause.
2. Evidence or it did not happen - every issue needs: steps to reproduce,
   expected vs actual, and raw evidence (screenshot / console output / log
   lines / command output). No "seems broken" claims.
3. Reproduce twice before reporting; separate confirmed bugs from flakes.
4. Test like a user: end-to-end flows, invalid/empty inputs, edge cases,
   not just the happy path. Check console/log errors after interactions.
5. Read-only observer - do NOT fix code, edit configs, or delete data while
   testing. If a destructive or irreversible action seems needed, stop and
   report it as a finding instead of doing it.
6. Report the boundary - list what was tested and what was NOT, plus issue
   counts by severity (Critical/High/Medium/Low). Untested areas are findings
   about the report, not things to hide.
```

Also require: `Final report format: summary (counts by severity) + per-issue
sections (title, severity, repro steps, expected vs actual, evidence path).`
Web app targets: the child should follow the dogfood skill's 5-phase method
(plan, explore, evidence, categorize, report) if it has browser tools; paste
that expectation into the task explicitly.

## Spelling a task

- `goal`: what to test and on which target (URL, command to run, or build
  instructions), e.g. "QA the signup flow of http://localhost:8000".
- `context`: QA block + environment facts (how to start/reach the app, test
  credentials if any) + hard constraints: never run against production data,
  no destructive actions (deletes, resets, payment/withdraw calls) - those
  need the user's explicit approval, so surface them instead.
- **State the expected behavior.** Include business rules / acceptance
  criteria for each area being tested ("fee = 0.9% of notional, rounded
  down", "withdraw blocked under min balance"). QA verifies app-vs-spec; it
  cannot invent the spec. No spec given = QA only finds crashes and
  technical edge bugs, and the report must say exactly that.
- **Spec source:** if the project has an architect-approved `docs/PRD.md`,
  cite the FR-n acceptance criteria as the spec in the task - that is the
  authoritative source, and business-logic testing becomes possible.
- Prefer one task = one feature area; parallel children for independent areas.

## Parent duties (cannot be delegated)

- Re-verify every Critical/High finding yourself (run the repro or read the
  evidence file) before reporting upward. Child bug lists are self-reports.
- Forward fixes to a coding-subagent task - do not ask the QA child to fix.
- Re-run QA after the fix lands; a fix is verified by a passing re-test, not
  by the coder's claim.

## Fix cycle (standard loop after a QA report)

1. Triage first, with MEKL if scope is unclear: fix now (Critical/High),
   backlog (Medium/Low), or WONTFIX (record reason in the report). Never fix
   blindly off the raw bug list.
2. Dispatch coding-subagent: one task per fix batch, each issue's repro +
   expected behavior copied from the QA report into the task context.
3. Re-test: dispatch qa-subagent on the SAME spec, scoped to fixed issues
   PLUS a regression pass over the areas the fix touched. Fresh eyes on the
   fix itself - the coder's claim is not evidence.
4. Update the report: issue status -> FIXED (re-tested <date>) or STILL
   BROKEN. New findings from re-test become new BUG-n entries.
5. Repeat until every issue is FIXED or WONTFIX, then set report status
   ALL FIXED.

Loop guards:

- If the same issue fails re-test TWICE, stop the loop and escalate to MEKL
  with both fix diffs - something structural is wrong; more retries just
  churn.
- New bugs found during re-test follow the same triage; a report only
  closes when its list is all FIXED/WONTFIX, not when the noise stops.
- Report status OBSOLETE only when superseded by a newer full report file.

## Report persistence (mandatory)

Chat summary is not a report - it dies with the session. Every QA run MUST
also write a durable markdown report:

- Path: `<project-root>/qa-reports/YYYY-MM-DD-<area>.md`
- Structure: header (date, target, commit/sha if a repo, tester = qa
  subagent id) + summary counts by severity + one section per issue (title,
  severity, repro steps, expected vs actual, evidence paths) + not-tested
  boundary list.
- Evidence files go to `<project-root>/qa-reports/<date>-<area>-evidence/`,
  never /tmp - a report referencing /tmp evidence is broken by reboot.
- Parent appends a verification line to each issue it re-confirmed
  (`verified by parent <date>: repro re-run, exit code N`) - unverified
  findings stay marked UNVERIFIED.
- Fix tracking: after a coding-subagent fix, add `Status: FIXED (re-tested
  <date>)` or `Status: STILL BROKEN` to the issue. Report is the single
  source of truth, chat is just the notification.
- Use `templates/qa-report-template.md` (in this skill dir) as the report
  skeleton; `examples/2026-09-23-stats-cli.md` is a filled worked example.

Upgrade path if MEKL wants more: GitHub Issues via gh CLI for repos on
GitHub, Obsidian note for personal tracking. Default stays plain markdown -
local, greppable, no moving parts.

## Field test

Live-tested 2026-09-23: black-box child found 2 planted bugs + 3 real edge
bugs in a tiny CLI, reproduced each 2x, saved real evidence files, respected
read-only constraints, reported untested boundary. Parent re-ran all High
repros - all confirmed. Conventions hold.

## Known limitation

Subagents cannot call skill_view - the QA block is pasted into the prompt
instead of relying on the skill system. If delegate_task ever gains skill
injection, switch to it and delete this note.
