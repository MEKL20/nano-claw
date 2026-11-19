---
name: egm-adapter
description: "Use when a design/spec needs Elephant drafting + Goldfish zero-context review before implementation. Portable EGM adapter for agents with fresh-context delegation."
version: 1.0.0
metadata:
  hermes:
    tags: [egm, sdd, design-review, goldfish, spec-driven]
    upstream: https://github.com/google/elephant-goldfish-model (Apache-2.0)
---

# EGM Adapter — Elephant-Goldfish Model (portable)

EGM = Spec-Driven Development: a deep-context **Elephant** drafts the spec,
zero-context **Goldfish** personas stress-test it, and a **human/lead** decides.

This skill is a portable adapter. It maps EGM onto agent primitives and carries
no host-specific or machine-specific paths. It is an adapter, not a fork: the
EGM skills, personas, and document standards stay in the upstream bundle.

## 1. Locate the EGM bundle

EGM skills read `agents/` and `resources/document_standards/` at run time, so
the whole bundle must be present — a skills-only copy is broken.

Resolve the bundle root in this order; stop at the first hit:

1. `$EGM_HOME` — environment variable pointing at the bundle root.
2. `./vendor/egm` — relative to the current working directory.

Expected layout at the resolved root:

```
skills/       # egm-brainstorm, egm-draft, egm-review, egm-review-loop, egm-resolve, egm-drift-report, egm-bootstrap, egm-lite
agents/       # personas: zoom_out, comprehension, design_critic, structural, style, implementation_readiness, inventive_catalyst, codebase_details, synthesizer, bootstrap_orchestrator
resources/    # document_standards/, execution_instructions.md
docs/         # getting_started.md, harnesses.md
```

If neither location exists, STOP and tell the user to set `EGM_HOME` or clone
the bundle. Never invent a path.

## 2. Harness mapping

| EGM concept | Agent primitive |
|---|---|
| Elephant session (deep context) | the profile holding project context (architect / pm / lead) |
| Goldfish fresh-context subagent | `delegate_task` / `task` / `invoke_subagent` — isolated conversation, no parent history |
| Named persona (`egm-design`) | no native named subagent -> child reads `agents/<persona>.md` first, then reviews |
| Artifact directory | `docs/designs/` in the project repo (commit approved specs) |
| Review synthesizer | synthesizer persona as its own child, or lead aggregates findings |

## 3. Workflow (before implementation)

1. Problem understanding — Elephant extracts problem + constraints.
2. Requirement extraction — from PRD/notes; ambiguities -> OPEN QUESTIONS.
3. Context analysis — codebase facts cited as `file:line`.
4. Candidate solutions — 2-3 options with trade-offs.
5. Design proposal — draft spec via the `egm-draft` methodology (section by section).
6. Independent critique — Goldfish swarm: `zoom_out` -> `comprehension` -> `design_critic` -> `implementation_readiness` (one child per persona, persona file read first).
7. Weakness identification — each finding: severity, evidence, suggested fix.
8. Refinement — Elephant revises the spec per accepted findings.
9. Final decision — lead/nano decides; MEKL owns trade-offs.
10. Implementation handoff — spec becomes TSD input + Kanban child cards.

## 4. Goldfish dispatch contract (parent runs this)

Replace `<EGM_BUNDLE>` with the resolved bundle root (§1) and `<persona>` with
the persona file name.

```
delegate_task:
  context: |
    You are a Goldfish reviewer with ZERO prior context.
    Read <EGM_BUNDLE>/agents/<persona>.md FIRST.
    Then review the spec at <path> against the live code at <repo>.
    Do not trust the spec's claims; verify against files. Cite file:line.
    Output: findings list (severity, evidence, fix), or PASS with rationale.
  goal: Review <spec> as <persona>; return findings only, no code changes.
```

Rules:

- One persona per child; no shared context between reviewers.
- Reviewer NEVER edits the spec; Elephant/lead applies fixes.
- Goldfish runs BEFORE implementation tasks are created.
- AI output is not fact: verify claims against files before acting.
- If fresh-context delegation is unavailable, STOP and report. A review in the
  parent context is not a Goldfish review.

## 5. Boundaries

- EGM does not orchestrate the crew. Lead remains the only orchestrator.
- EGM artifacts are inputs, not approvals. Approval = lead + MEKL.
- The adapter does not modify the upstream bundle; propose changes upstream.

## Provenance

- Source repo: https://github.com/google/elephant-goldfish-model
- License: Apache-2.0 (see `LICENSE`)
- Bundle audited: 2026-11-19 at commit `70406c4d22cc7ea8299637c2c5b44625c48b3f08`
- Adapter: MEKL crew (portable rewrite; no host-specific paths)
