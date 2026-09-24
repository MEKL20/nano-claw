---
name: subagent-team
version: 1.0.0
description: "One audited agent team: plan, design, build, test, secure."
---

# Subagent Team: plan-design-build-test-secure

# Crew5

A complete subagent software team for Hermes (or any agent with a
spawn-delegate primitive), shipped as one installable skill: Crew5. Five specialist
roles, one human approval gate, rules that survive sessions. Every rule in
this team was live-tested before being written down (field tests noted in
each member skill).

This SKILL.md is the router and the rulebook. The member skills carry the
detail:

| Role | Skill | Does | Never does |
|---|---|---|---|
| Brain | `architect-subagent` | PRD, stack, ERD, threat model, backlog | implement |
| Design | `ui-ux-subagent` | DESIGN.md, UX critique, antislop audit | implement |
| Hands | `coding-subagent` | implement, Karpathy + comment hygiene | self-verify as final |
| Evidence | `qa-subagent` | black-box testing, bug reports, re-tests | fix |
| Finder | `security-subagent` | vuln findings, PoCs, coverage ledger | fix, exceed scope |
| Parent | your main agent | verify, route, triage, relay MEKL | delegate verification |

External rules sources (audited before adoption, re-audit before updating):
- karpathy-guidelines (multica-ai/andrej-karpathy-skills)
- antislop-code (miqdadbadjuber/anti-slop v3.2.14)

## The 5 non-negotiables (whole team)

1. **Self-report is not evidence.** Every child claim is re-verified by the
   parent: re-run the test/repro/contrast check, read the cited lines.
   Nothing reaches MEKL on a child's word alone.
2. **Separation of duties.** The one who produces never certifies: QA does
   not fix, the designer does not implement, the coder does not re-test
   their own fix, security does not patch. One agent doing both grades its
   own homework.
3. **The human owns risk calls.** MEKL approves: PRD/stack/infra, design
   direction, dynamic security testing (per-run), any destructive or
   external action, anything touching production data. Children propose,
   parent relays, MEKL decides.
4. **Escalation guards, not infinite loops.** Same failure twice = stop and
   escalate with evidence. Scope creep = back to the architect's docs
   first. No agent silently absorbs a requirement or a fix.
5. **Durable docs over chat.** Reports, PRDs, reviews, and decisions are
   markdown files in the project (`qa-reports/`, `security-reports/`,
   `design-reviews/`, `docs/`). Chat is a notification, files are truth.

## Install

Hermes: copy each member folder into `~/.hermes/skills/software-development/`
(e.g. `roles/architect-subagent/` -> `~/.hermes/skills/software-development/architect-subagent/`).
The ui-ux role also needs the `design-rules/` packs: antislop* folders go to
`~/.hermes/skills/creative/`, `antislop-code` goes to
`~/.hermes/skills/software-development/` with the role skills.
All member skills must keep the same version tag as this file; mixed versions
= re-run the field tests before use.

Other agents: any framework with (a) spawned sub-conversations, (b) a
read-only file system for children, (c) a human channel for the parent to
relay approvals. Paste the member skills' principle blocks as the child
system prompt / task preamble; the workflow contracts (who hands what to
whom) are framework-agnostic.

## Standard flows

**New project:** brief from MEKL -> architect drafts PRD + questions ->
MEKL answers -> approve PRD/stack/infra -> (FE project: ui-ux DESIGN.md ->
MEKL approves direction) -> architect finalizes backlog -> parent dispatches
T-n tasks (coding / ui-ux) -> qa tests each acceptance criterion -> fix
cycle until FIXED/WONTFIX -> security review before ship if attack surface
exists.

**Bug/finding loop:** qa or security finding -> parent re-verifies ->
triage (fix now / backlog / WONTFIX with reason) -> coding-subagent fixes
(repro + expected in task) -> finder re-tests -> report status updated.

**Small tasks (most days):** skip the ceremony - coding-subagent + compact
blocks handles it. The team exists for builds, not for one-line fixes.

## Cost discipline

The full ceremony is expensive (a full gated UI build ran 8.5 min + 15 API
calls vs seconds for a compact block). The parent picks the tier per task:
compact rules block for small work, full role engagement when the risk the
role covers is actually present. Skip roles whose risk is absent - but
never skip parent verification, never skip the scope gate, never let a
fixer certify a fix.

## Adaptation notes for other agents

- Roles are contracts, not personas: what matters is output artifacts,
  forbidden actions, and who verifies - not the agent names.
- If your framework lacks read-only children, approximate with strict
  allowed-dirs in the task text plus parent diff review after the run.
- If your model is weak at instruction-following, shrink each role to its
  principle block + report format and drop the rest; the 5 non-negotiables
  are the floor, not the ceiling.
- Re-audit any external rules source before adopting updates; audits are
  snapshots, not endorsements forever.
