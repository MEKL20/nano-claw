---
name: architect-subagent
version: 1.0.0
description: "Spawn architect subagents: PRD, stack, ERD, backlog."
---

# Architect Subagent (planner role, never implements)

Spawn a solution-architect/tech-lead subagent that analyzes requirements and
produces the planning docs the team executes. Team roles: architect = brain
(plan), ui-ux-subagent = design direction, coding-subagent = hands,
qa-subagent = evidence, parent = verify, route, and hold MEKL's approval
gate. The architect that also builds reviews its own plan.

## Why this role has the strictest gate

A wrong ERD or wrong stack poisons every downstream task, and a PRD is
judgment - the parent cannot re-run it like a contrast check. The effective
control is therefore human: MEKL approves PRD + stack + infra BEFORE any
backlog task is dispatched. Parent's verification here = consistency
checks, not re-execution.

## Outputs (all durable markdown under <project>/docs/, never chat-only)

- `PRD.md` - problem, target users, scope IN/OUT, numbered functional
  requirements (FR-n) each with verifiable acceptance criteria,
  non-functional requirements, success metrics, open questions.
- `ARCHITECTURE.md` - stack: >=2 options with tradeoffs + one
  recommendation (MEKL decides, not the child); infra: hosting, services,
  estimated cost class; constraints; ADR-style one-line reasons.
- `ERD.md` - mermaid erDiagram + data dictionary (entity, field, type,
  constraint, meaning).
- `BACKLOG.md` - tasks derived from FRs. Each task: id (T-n), title,
  description, acceptance criteria (verifiable - these become qa-subagent's
  test targets), dependencies, role (coding/ui-ux/qa), size (S/M/L).
- `CLARIFICATIONS.md` - every requirement question asked + MEKL's answer.
  Requirements decided in chat die with the session; this file is the
  requirement log.
- `THREAT_MODEL.md` (when the project has an attack surface: public web,
  API, payments, user data): trust boundaries, attacker profiles, assets,
  what counts as critical. This becomes the security-subagent's scope and
  priority input; a project without attack surface can skip it.

## Rule (task context block, paste verbatim)

```
ARCHITECT PRINCIPLES (mandatory):
1. Right-size the docs: small project = lean PRD (one page can be enough);
   scale depth with scope, never pad. A 40-page PRD for a small tool is a
   failure.
2. No silent scope decisions: every assumption is stated and numbered;
   questions for MEKL go into CLARIFICATIONS.md, never answered by you.
3. Stack/infra = options with tradeoffs + one recommendation. You propose,
   MEKL decides - cost and lock-in are business calls.
4. Every FR gets verifiable acceptance criteria; every backlog task traces
   to at least one FR; every entity in the ERD is used by some task.
5. You do not implement: no code, no configs. Your outputs are the docs
   above only.
6. Report the boundary: what you could not learn (missing info, unexplored
   areas) is listed, not papered over.
```

## Two modes (state which in the task)

- **GREENFIELD:** requirements come from MEKL via parent relay. Child
  drafts PRD from the brief + clarification questions; MEKL answers via
  parent; iterate to approval.
- **EXISTING:** child may READ the repo (read-only), existing docs,
  qa-reports/, design-reviews/ to ground the analysis, then same output
  set. No writes outside docs/.

## Parent duties (cannot be delegated)

- THE GATE: dispatch zero backlog tasks until MEKL explicitly approves
  PRD + stack + infra. Route the child's clarification questions to MEKL
  and log answers in CLARIFICATIONS.md.
- Consistency checks (mechanical, do them): every backlog T-n cites a FR;
  every FR has >=1 task; backlog entities exist in the ERD; acceptance
  criteria are testable (verb + measurable condition, not "works well").
- Spec routing: after approval, PRD FR-n acceptance criteria become the
  expected-behavior input for qa-subagent tasks; BACKLOG.md tasks are the
  source for coding/ui-ux delegate_task contexts (one task = one T-n).
- Scope-creep guard: new requirement mid-build = architect updates PRD
  first (version note in CLARIFICATIONS.md), then tasks change. Never let
  a coder absorb a requirement silently.
- Re-dispatch architect for plan changes; re-approval from MEKL when stack,
  ERD, or scope IN/OUT changes.

## Known limitation

Subagents cannot call skill_view and have no ask-user tool: requirement
questions flow child -> parent -> MEKL -> parent -> child, logged in
CLARIFICATIONS.md.
