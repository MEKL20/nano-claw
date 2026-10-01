# Crew5 Ops Runbook (parent only)

Read before EVERY dispatch. These are delegation mechanics, learned the
expensive way on this host. They are not optional context for the parent.

## Routing (checked 2026-10-01)

- `delegation.provider` must be `custom:9router`, `delegation.model`
  `sm/glm-5.3-flash`. Empty provider fields route children to external
  fallbacks that 403 instantly, and the gateway's "switch to <model>" hint is
  boilerplate whose suggested model also 403s. The parent surviving on the
  gateway proves nothing about children - pin them explicitly.
- `child_timeout_seconds: 3600`. The old 600 killed a research run mid-flight
  with good evidence in context and nothing on disk.
- **Smoke test the pipe before any long dispatch.** One `delegate_task`
  asking for a fixed reply string costs ~25s and proves model + route. Do it
  after any routing or model change.

## Brief construction (the parent's real job)

Every brief carries, verbatim:

1. the role principle block from the member skill;
2. project dir path, files to READ, files to WRITE (exact paths);
3. the cached host facts this task touches (crew5 SKILL.md "Host facts");
4. forbidden actions / scope list / read-only areas;
5. `write files one at a time, never batch at the end - files survive, context
   may not`;
6. `final message = what you did, files touched, how you verified (commands +
   real output)`.

Children cannot call `skill_view`, cannot read memory, cannot ask the user.
Anything missing from the brief does not exist for them. Questions flow
child -> parent -> MEKL -> parent -> child, logged in `docs/CLARIFICATIONS.md`.

## Failure modes and the response

| Symptom | Response |
|---|---|
| 429 mid-run | Resume, never restart. Inventory the project dir, then dispatch a brief listing exactly what exists (do-not-rewrite) and what remains; tell the child to read the last written file to match style and continue. |
| Child timed out | Same inventory-then-resume brief. Pass prior partial findings in so nothing is re-derived. |
| `web_search` 403 (keyless Firecrawl, intermittent) | Say so in the brief: retry and rephrase, do not stall. |
| Small fix dispatch dies twice | Parent executes the edits itself with `patch` + grep verification. Mechanical work under ~15 min with deterministic verification is parent work; dispatch only real reasoning. |
| Child reports success | Re-run its verification command yourself. Self-report is not evidence. |
| Child touched something outside scope | Log it as a trust failure, not just a bug, and tighten the next brief. |

## Verification moves the parent cannot delegate

- Re-run the build/test/lint command and read real output.
- Re-run every Critical/High repro from a QA or security report; append
  `verified by parent <date>: <command>, exit <n>` to the issue. Unverified
  findings stay marked UNVERIFIED.
- Consistency checks on architect docs (mechanical): every T-n cites an FR,
  every FR has >=1 task, backlog entities exist in the ERD, acceptance
  criteria are verb + measurable condition.
- Cross-artifact check after any fix that changes a fact: grep the OTHER
  artifacts (README, docs, release notes, listing copy) for the stale value.
  A child verifies its own file, not the rest of the project.
- Sweep the project dir before declaring a phase done: probe scripts, nested
  `<slug>/<slug>/` dirs, and stray evidence files are created by degraded
  children and silently ship.

## Evidence storage

Evidence belongs in the project (`qa-reports/<date>-<area>-evidence/`,
`security-reports/...`), never `/tmp` - a report citing `/tmp` is broken by
the next reboot. Never paste discovered secret VALUES into a report or a
message: file and line only.
