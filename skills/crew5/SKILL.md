---
name: subagent-team
version: 1.2.0
description: "One audited agent team: plan, design, build, test, secure."
---

# Crew5: plan - design - build - test - secure

Subagent software team for Hermes (or any agent with a spawn/delegate
primitive), shipped as one installable skill. Five specialist roles, human
gates that cannot be forged, rules that survive sessions. Every rule here was
field-tested before being written down (tests noted in the member skills).

This SKILL.md is the router and the rulebook. Member skills carry the detail;
`references/00-ops.md` carries the delegation mechanics the parent reads
BEFORE every dispatch.

| Role | Skill | Does | Never does |
|---|---|---|---|
| Brain | `architect-subagent` | PRD, stack, ERD, threat model, backlog | implement |
| Design | `ui-ux-subagent` | DESIGN.md, UX critique, antislop audit | implement |
| Hands | `coding-subagent` | implement, Karpathy + comment hygiene | self-verify as final |
| Evidence | `qa-subagent` | black-box testing, bug reports, re-tests | fix |
| Finder | `security-subagent` | vuln findings, PoCs, coverage ledger | fix, exceed scope |
| Parent | your main agent | verify, route, triage, relay MEKL | delegate verification |

## Context protocol (what a child knows: CAG + RAG)

Children start blind: no skills, no memory, no chat history, no ask-user tool.
Two context channels, and the parent owns both.

**CAG - pasted verbatim into the brief, cached by the parent, never
re-derived by the child:**

1. the role's principle block, copied from the member skill;
2. project dir path + the exact files to read and the exact files to write;
3. the cached host facts that touch this task (see Host facts below);
4. hard constraints: forbidden actions, scope list, read-only areas;
5. the approval line when one is required
   (`dynamic approved by MEKL for: <targets>`).

Re-derivation is a failure mode, not thoroughness: a child that discovers
tooling by trial burns the run and sometimes installs things. Facts the
parent already knows belong in the brief.

**RAG - retrieved by the child from disk, at the moment it needs them:**

- `docs/PRD.md` FR-n acceptance criteria = the spec of record;
- `docs/BACKLOG.md` T-n = the task definition;
- prior `qa-reports/`, `security-reports/`, `design-reviews/` = known state;
- the code itself for anything it asserts - claims cite `file:line`.

Three rules make retrieval trustworthy:

- **Artifact outranks summary.** The file on disk beats any prose about it,
  including the parent's. Chat memory is never a spec.
- **Inventory before re-dispatch.** Before a fix or resume brief, the parent
  greps what already exists and lists done / not-done explicitly. Skip this
  and half-finished work gets redone or silently skipped.
- **Write incrementally.** Children write one file at a time, never batched
  at the end. Files survive a timeout; context does not.

## The 8 non-negotiables (whole team)

1. **Self-report is not evidence.** Every child claim is re-verified by the
   parent: re-run the test/repro/measurement, read the cited lines. Nothing
   reaches MEKL on a child's word alone.
2. **Separation of duties.** The producer never certifies: QA does not fix,
   the designer does not implement, the coder does not re-test their own fix,
   security does not patch. One agent doing both grades its own homework.
3. **The human owns risk calls.** MEKL approves: PRD/stack/infra, design
   direction, dynamic security testing (per run), destructive or external
   actions, anything touching production data. Children propose, parent
   relays, MEKL decides.
4. **Human gates are human-only.** An approval, sign-off, or playtest flag is
   recorded by MEKL's own action. An agent writing one fabricates consent -
   the one failure this pipeline cannot detect afterwards.
5. **Escalation guards, not infinite loops.** Same failure twice = stop and
   escalate with evidence. Scope creep = back to the architect's docs first.
   No agent silently absorbs a requirement or a fix.
6. **A stuck loop is a design signal.** Two failed attempts at the same wall:
   stop tweaking parameters, instrument (log what actually failed), then
   change the constraint. Timebox every retry loop so it fails loudly instead
   of hanging.
7. **Durable docs over chat.** Reports, PRDs, reviews, decisions are markdown
   files in the project (`docs/`, `qa-reports/`, `security-reports/`,
   `design-reviews/`). Chat is a notification; files are truth.
8. **Context dies, files survive.** Incremental writes, resume briefs that
   inventory partial progress, evidence stored in the project (never `/tmp`).

## Cycle

One stage = one owner, one durable artifact, one exit gate the parent can
verify by running something. No stage is done on a child's summary.

| # | Stage | Owner | Artifact | Exit gate (parent runs it) |
|---|---|---|---|---|
| 1 | Intake | parent | `docs/CLARIFICATIONS.md` | every open question answered by MEKL or logged as a numbered assumption |
| 2 | Plan | architect | `docs/PRD.md`, `ARCHITECTURE.md`, `ERD.md`, `BACKLOG.md`, `THREAT_MODEL.md` if attack surface | every FR has testable criteria; every T-n cites an FR; every ERD entity is used |
| 3 | Approval | **MEKL** | approval logged in `CLARIFICATIONS.md` | explicit yes on PRD + stack + infra. No yes = zero build dispatches |
| 4 | Design direction (UI projects) | ui-ux | `DESIGN.md` | every decision carries a one-line reason; contrast gates computed, not asserted |
| 5 | Build | coding | code, tests, migrations | parent re-runs build/lint/test and reads real output; `node --check`-class syntax gate per file |
| 6 | QA | qa | `qa-reports/YYYY-MM-DD-<area>.md` | verdict stated; every issue has repro + expected/actual + evidence path; parent re-runs each Critical/High repro |
| 7 | Fix loop | coding (fix) + qa (re-test) | updated diff + issue status | fresh QA pass over ALL criteria, not just the fixed one; fixer never re-checks |
| 8 | Security | security | `security-reports/YYYY-MM-DD-<area>.md` | scope list present in the brief; coverage ledger lists clean surfaces too; each candidate CONFIRMED / RULED_OUT / OPEN_PROOF_GAP |
| 9 | Handoff | parent | summary + release note | every claim traces to an artifact the parent re-verified |

Stage 3 is the hard gate. Stages 4-8 run as needed; skipping one is a
decision the parent records, not a default.

## Fix loops (who fixes what)

- QA FAIL -> **coding** fixes (repro + expected pasted into the brief) ->
  **fresh QA** re-tests everything in scope. Report status becomes FIXED
  (re-tested <date>) / STILL BROKEN / WONTFIX + reason.
- Security finding -> parent re-verifies -> coding fixes -> **security**
  re-tests. Live secret found = escalate to MEKL immediately.
- Design audit finding -> coding implements -> ui-ux re-audits the measured
  claims (re-run `contrast-check.py` on the cited pairs).
- Mechanical edit under ~15 minutes with deterministic verification: the
  **parent does it directly**. Dispatch costs more than the work and dies to
  rate limits on short tasks (see `references/00-ops.md`).
- Same failure twice -> stop, report with evidence (non-negotiable 5).

## Host facts (cached - paste what the task touches, do not let children rediscover)

- `python3` runs from the Hermes venv; PEP 668 host - no system `pip install`.
  `dpkg` is broken for new installs: nothing gets apt-installed mid-task.
- `node` v22 and `npm` present. **No `zip` CLI** - archive with `python3`
  `zipfile` (stdlib); `unzip` exists for verification.
- **No vision on this host.** Never ask anyone to look at an image. Measure
  pixels programmatically (PIL histograms, `getImageData` counts, WCAG
  luminance via `contrast-check.py`).
- Playwright chromium cached under `~/.cache/ms-playwright`; `browser_exec`
  uses its own Chrome under `~/.agent-browser/browsers/`.
- `git` present, **no `gh` CLI**; GitHub over SSH (ed25519). Never route a
  token through chat or a file.
- Delegation is pinned to the local gateway; empty provider fields send
  children to external fallbacks that 403 instantly. Details and the smoke
  test: `references/00-ops.md`.

## Reference index

| Reference | Read by |
|---|---|
| `references/00-ops.md` | parent only, before EVERY dispatch |
| member skill principle blocks | pasted into the matching child brief |
| `qa-subagent/templates/qa-report-template.md` | pasted or path-cited into QA briefs |

## Cost discipline

The full ceremony is expensive (a gated UI build ran 8.5 min + 15 API calls
vs seconds for a compact rules block). The parent picks the tier per task:
compact block for small work, full role engagement when the risk that role
covers is actually present. Skip roles whose risk is absent - never skip
parent verification, the scope gate, the human gates, or the rule that a
fixer cannot certify the fix.

Dispatch one child per stage, sequentially: each one's input is the previous
stage's artifact. Parallel children only for genuinely independent work, and
never two writers in the same directory.

## Install

Hermes: copy each member skill folder into `~/.hermes/skills/` (category dir
is cosmetic - the skill `name` is the id; this live tree keeps the five roles
under `software-development/` except `ui-ux-subagent` under `creative/`).
`ui-ux-subagent` also needs the five antislop skill folders. Keep all member
skills on the same version tag as this file; mixed versions = re-run the
field tests before use.

Other agents: any framework with (a) spawned sub-conversations, (b) file read
access for children, (c) a human channel for the parent to relay approvals.
Paste each member skill's principle block as the child's system prompt or
task preamble; the workflow contracts are framework-agnostic.

## Adaptation notes for other agents

- Roles are contracts, not personas: what matters is output artifacts,
  forbidden actions, and who verifies - not the agent names.
- No read-only children? Approximate with strict allowed-dirs in the brief
  plus parent diff review after the run.
- Weak instruction-following model? Shrink each role to its principle block +
  report format and drop the rest; the 8 non-negotiables are the floor.
- Re-audit any external rules source before adopting updates; an audit is a
  snapshot, not an endorsement forever.

## Provenance

External rules sources, audited clean 2026-09-23 before adoption (re-audit
before updating): karpathy-guidelines (multica-ai/andrej-karpathy-skills),
antislop packs (miqdadbadjuber/anti-slop v3.2.14), security methodology
reference (usestrix/strix).
