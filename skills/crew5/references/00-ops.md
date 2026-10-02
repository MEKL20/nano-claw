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
- Recompute every number a child reports, from its own cells. Children count
  their own rows wrong in a consistent direction: favourably. Cells honest,
  summary inflated is the normal failure, not fabrication.
- Test every command you ship inside a brief, by running it. A brief that
  hands a child a command with a quoting bug, a wrong expected count, or a
  path that only resolves from one directory burns a full dispatch cycle.

## Lessons (each one cost a dispatch or shipped a defect)

- **The parent never certifies its own fix.** Mechanical edits with
    deterministic verification belong to the parent, not a dispatch — but then a
    FRESH child re-tests, and re-runs EVERY check, not only the fixed items.
    Fixes routinely break what they did not intend to touch, and the fixer is
    structurally unable to find its own blind spot.
- **Never write into a project a child is actively reading.** Creating a missing
    artifact mid-run forces the child to report both the original finding and a
    re-check that clears it; the record now needs a footnote to read, and a
    finding count that needs explaining is a finding count nobody trusts. Create
    it before dispatching, or wait. This also forbids cosmetic edits mid-run.
- **A gate may only check artifacts that exist at its own stage.** Ask of every
    check in a brief: does the file it names exist when this stage runs? Given
    nothing to verify, a child goes looking — and satisfying a check from a
    DIFFERENT project's files is one step from a false pass.
- **Never edit code or prose to satisfy a finding you cannot reproduce.** Record
    it as unreproducible and pass it to the re-test. Rewriting correct work to
    close a phantom finding is how a pipeline degrades what it was built to
    protect. If the re-test still reports it, the sweep is what is broken.
- **Markers and escaping hide defects from raw-string searches.** `in a **oven`
    renders as "in a oven" while a grep for `"in a oven"` finds nothing. Strip
    markup before any text sweep, and when a child cites `file:line`, read that
    line RENDERED before calling it phantom.
- **Grep the BUILT artifact, not only the sources.** A rendering or compile step
    can introduce a defect that every source-level check passes. Run the sweep on
    the output, and on every artifact the same builder has ever produced — a
    builder bug is retroactive across all of them.
- **Read metadata back out of what you just built.** Exit code 0 plus a valid
    file is not verification: a regex that misses its field writes a correct,
    well-formed artifact describing the wrong thing. Parse the output's own
    identity fields and compare them to the source of truth.
- **A fix applied in one representation survives in the others.** Prose fixed,
    table still wrong; code fixed, docs still wrong; artifact fixed, README still
    quotes the old value. After any fix that changes a fact, grep the other
    representations for the stale one.
- **Mechanical sweeps take two passes and a protect list.** Exact-match
    replacement leaves inflected and compound forms behind; a broad stem scan
    catches those and threatens correct words containing the same stem. Write the
    protect list BEFORE replacing anything, then verify on the rebuilt output.
- **When a stage starts producing NUMBERED artifacts, grep for every reader of
    the old single filename.** A consumer pinned to `report.md` keeps reporting
    round 1's verdict while round 3 passes, and the work looks stuck for reasons
    that have nothing to do with the work.
- **A PASS verdict is not permission to ship.** Gate the shipping state on the
    deliverable existing too, not on the verdict alone, or a phase announces
    itself ready with nothing to hand over.
- **A check that reports MISSING on correct content is worse than no check.**
    False alarms teach the next reader to skim the gate, and the fix loop then
    damages correct work to satisfy it. When a check fires, verify the finding
    before acting on it; three of mine were my own criteria being wrong.

## Evidence storage

Evidence belongs in the project (`qa-reports/<date>-<area>-evidence/`,
`security-reports/...`), never `/tmp` - a report citing `/tmp` is broken by
the next reboot. Never paste discovered secret VALUES into a report or a
message: file and line only.
