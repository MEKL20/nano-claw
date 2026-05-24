# Memory Blueprint

Purpose: define a reusable **memory concept only** for an AI assistant/workflow orchestrator. A new server can read this file and generate its own memory files from the concept.

This blueprint intentionally avoids persona, model, provider, channel, server, and tool configuration. It only describes how memory should be structured, written, promoted, reviewed, and reused.

---

## 1. Core Concept

Use a **hybrid scoped memory** system:

1. **Global durable memory**
   - Stores stable facts and preferences that apply across all work.
   - Small, curated, and high-signal.

2. **Project durable memory**
   - Stores long-lived context for a specific project/domain.
   - Includes goals, decisions, constraints, gotchas, and verified workflows.

3. **Daily working memory**
   - Stores temporary notes from active work.
   - Includes findings, work logs, open loops, evidence, and decisions from the day.

Core rule:

> Start specific. Promote upward only when information proves stable, useful, safe, and likely to be reused.

---

## 2. Recommended Layout

A new server may generate this minimal layout:

```text
workspace/
├── MEMORY.md
└── memory/
    ├── README.md
    ├── TAXONOMY.md
    ├── OPERATING_RULES.md
    ├── TEMPLATE.md
    └── projects/
        ├── _template/
        │   ├── SUMMARY.md
        │   └── DAILY.md
        └── <project-slug>/
            ├── SUMMARY.md
            └── YYYY-MM-DD.md
```

Optional files such as identity/persona/user profile can exist outside this blueprint, but they are not part of the memory concept.

---

## 3. Memory Layers

### 3.1 Global Durable Memory

Recommended file:

```text
MEMORY.md
```

Use for:

- stable user preferences
- standing constraints
- long-lived environment facts
- cross-project workflow decisions
- high-level privacy/security boundaries

Do not use for:

- noisy logs
- raw transcripts
- temporary findings
- project-specific details
- abandoned experiments
- credentials, tokens, or secrets
- unnecessary private/personal details

Promotion requirement:

Only write to global memory if the information is:

- stable
- cross-project
- likely useful again
- safe to keep long-term
- compact enough for global context

---

### 3.2 Project Durable Memory

Recommended file:

```text
memory/projects/<project-slug>/SUMMARY.md
```

Use for:

- project purpose and status
- durable project goals
- active decisions and reasons
- constraints
- known gotchas
- preferred workflows
- verification/deployment notes
- open strategic questions

Do not use for:

- every small task
- one-off temporary notes
- noisy command output
- information that belongs globally

---

### 3.3 Daily Working Memory

Recommended file:

```text
memory/projects/<project-slug>/YYYY-MM-DD.md
```

Use for:

- current work context
- work logs
- temporary findings
- open loops
- short-lived constraints
- evidence paths/commands
- decisions made today
- candidates for later promotion

Daily memory is not meant to be permanent truth. It is a staging area.

### 3.4 Semi-Automatic Daily Memory

By default, the assistant should decide when to write into daily memory without requiring the user to explicitly ask. Write when there is a meaningful task, decision, result, blocker, open loop, or follow-up. Do not write for ordinary conversation or noisy transcript logs. Keep notes minimal and auditable rather than exhaustive.

---

## 4. Project Slug Rules

Project slugs should be:

- lowercase
- kebab-case
- stable over time
- broad enough to avoid fragmentation
- specific enough to avoid mixing unrelated context

Examples:

```text
assistant-workspace
runtime-ops
vps-system
user-preferences
experiments
```

Create a new slug only when:

- work is likely to recur, or
- it has its own durable decisions/settings, or
- mixing it into an existing slug would confuse future recall.

If unsure, use an existing broader slug first.

---

## 5. Destination Decision Tree

When deciding where to write memory:

```text
Is it sensitive, noisy, or unnecessary?
  -> Do not store it.

Is it global, stable, and cross-project?
  -> MEMORY.md

Is it durable but project-specific?
  -> memory/projects/<slug>/SUMMARY.md

Is it temporary, exploratory, or part of today's work?
  -> memory/projects/<slug>/YYYY-MM-DD.md

Unsure?
  -> Keep it project-specific or daily first. Promote later if needed.
```

---

## 6. Promotion Rules

Memory should move upward only through review.

### Daily -> Project Summary

Promote when the item is:

- still relevant after the immediate task
- likely useful for future work in that project
- a decision, constraint, gotcha, workflow, or verified fact

### Project Summary -> Global Memory

Promote only when the item is:

- not tied to one project
- stable across contexts
- useful for future unrelated work
- safe to preserve long-term

### Never Promote

Do not promote:

- temporary debugging details
- abandoned experiment steps
- raw logs
- raw private messages
- secrets
- speculation that was not verified

---

## 7. Recall Rules

Before answering about prior work, decisions, dates, people, preferences, or todos:

1. Search memory first.
2. Read only the relevant snippets.
3. Prefer project memory over global memory for project-specific questions.
4. Prefer global memory for stable preferences and standing constraints.
5. If confidence is low, say so.
6. Cite source file/line when useful.

For new tasks without continuity requirements, do not overuse memory.

---

## 8. Review Cadence

Review memory when:

- several meaningful sessions accumulate in one project
- daily notes become noisy
- open loops pile up
- a project changes direction
- the user asks for cleanup/export/reuse

Review process:

1. Read recent daily notes for one project.
2. Extract durable decisions, constraints, gotchas, and workflows.
3. Update that project's `SUMMARY.md`.
4. Promote only truly global durable facts to `MEMORY.md`.
5. Leave temporary details in daily notes.
6. Mark abandoned experiments clearly.
7. Archive old/noisy notes only if useful.

---

## 9. Privacy and Safety Rules

Store the minimum useful information.

Allowed when useful:

- stable interaction preferences
- operational constraints
- project decisions
- safe environment facts
- verified workflow notes

Avoid unless explicitly necessary:

- sensitive personal details
- credentials/tokens/secrets
- raw private message content
- third-party details
- unnecessary identifiers
- speculative or unverified claims

If privacy value and memory value conflict, prefer privacy.

---

## 10. Recommended File Templates

A new server may generate files using these templates.

---

### 10.1 `MEMORY.md`

```md
# MEMORY.md

## Global Preferences
- 

## Standing Constraints
- 

## Environment Facts
- 

## Workflow Decisions
- Use a lightweight, local-first, Markdown-based memory system.
- Keep global memory compact and curated.
- Store project-specific durable context under `memory/projects/<slug>/SUMMARY.md`.
- Store temporary working notes under `memory/projects/<slug>/YYYY-MM-DD.md`.
- Promote facts upward only when stable, safe, and useful across projects.

## Privacy Notes
- Store the minimum useful information.
- Do not store credentials, tokens, or unnecessary private details.
```

---

### 10.2 `memory/README.md`

```md
# Memory Layout

This workspace uses a hybrid scoped memory layout.

## Layers

### 1. Global durable memory
- `../MEMORY.md`
- Stable preferences, standing constraints, global environment facts, long-lived workflow decisions.

### 2. Project durable memory
- `projects/<project-slug>/SUMMARY.md`
- Project goals, active decisions, durable constraints, known gotchas, preferred workflows.

### 3. Project daily working memory
- `projects/<project-slug>/YYYY-MM-DD.md`
- Temporary findings, work logs, open loops, today's decisions, evidence, near-term context.

## Rules

- Do not put all project details into `MEMORY.md`.
- Keep global memory compact.
- Keep project context under project folders.
- Use daily files as staging areas.
- Promote only stable, safe, reusable facts upward.
```

---

### 10.3 `memory/TAXONOMY.md`

```md
# Memory Taxonomy

Purpose: keep memory organized without making the system heavy.

## Slug Rules

Project slugs should be:
- lowercase
- kebab-case
- stable over time
- broad enough to avoid fragmentation
- specific enough to avoid mixing unrelated context

## Starter Slugs

| Slug | Use for |
| --- | --- |
| `assistant-workspace` | assistant identity, behavior, skills, memory workflow, operating conventions |
| `runtime-ops` | runtime/config/provider/channel behavior and operational issues |
| `vps-system` | host-level Linux/VPS administration and services |
| `user-preferences` | stable user preferences and safe personal context useful for assistance |
| `experiments` | temporary trials, spikes, comparisons, prototypes |

Create new slugs only when durable context would otherwise become mixed or confusing.

## Classification Rules

1. If it affects all work, consider `MEMORY.md`.
2. If it affects one project repeatedly, use that project's `SUMMARY.md`.
3. If it is temporary or exploratory, use the daily file.
4. If unsure between global and project-specific, keep it project-specific first.
5. Promote upward only after it proves stable and useful.
```

---

### 10.4 `memory/OPERATING_RULES.md`

```md
# Memory Operating Rules

## Default Stance

- Prefer small, explicit memory updates.
- Verify before recording factual claims as durable.
- Do not add complexity unless it solves a real problem.
- Keep memory useful, not exhaustive.

## Memory Write Checklist

Before writing memory, ask:

- Is this likely useful again?
- Is this stable enough to preserve?
- Is this safe to store?
- Does this belong globally, project-level, or daily?
- Can this be written as a concise summary instead of raw detail?
- Is this ordinary conversation or should it be recorded? Prefer recording meaningful tasks, decisions, results, blockers, open loops, and follow-ups. Skip ordinary chat.

## Completion Checklist

Before saying memory work is done:

- [ ] The correct destination was used.
- [ ] Sensitive/noisy details were excluded.
- [ ] Durable facts are concise and clear.
- [ ] Temporary context stayed in daily memory.
- [ ] Promotion decisions are explainable.

## Failure Handling

If memory search is empty or suspicious:

- retry with another query/path/source when reasonable
- do not pretend certainty
- say what was checked and what remains uncertain
```

---

### 10.5 `memory/TEMPLATE.md`

```md
# Hybrid Memory Rules

## Where to Write

- Global durable facts/preferences/constraints -> `MEMORY.md`
- Durable project knowledge -> `memory/projects/<project-slug>/SUMMARY.md`
- Daily working notes -> `memory/projects/<project-slug>/YYYY-MM-DD.md`

## Promotion Rules

Promote to `MEMORY.md` only if the information is:
- stable
- cross-project
- likely useful again
- safe to keep long-term

Otherwise keep it at the project level or daily level.
```

---

### 10.6 `memory/projects/_template/SUMMARY.md`

```md
# Project Summary Template

## Project
- Name:
- Slug:
- Purpose:
- Status: active / paused / archived

## Durable Context
- Core goal:
- Key environment facts:
- Important dependencies:

## Active Decisions
- Decision:
  - Why:
  - Still valid because:

## Constraints
- Technical constraint:
- Security/privacy constraint:
- Workflow constraint:

## Known Gotchas
- Gotcha:
- Avoid by:

## Preferred Workflow
- Build/test path:
- Review expectations:
- Deployment/ops notes:

## Open Strategic Questions
- Question:
- Next investigation:

## Promote to MEMORY.md?
- [ ] Cross-project durable fact
- [ ] Global user/workflow preference
- [ ] Standing environment constraint
```

---

### 10.7 `memory/projects/_template/DAILY.md`

```md
# Daily Project Memory Template

## Summary
- Main focus:
- Outcome:
- Status: active / blocked / done

## Important Context
- Current subtask:
- Relevant files/components:
- Short-lived constraints:

## Decisions Today
- Decision:
  - Why:
  - Revisit when:

## Work Log
- Task:
  - Action taken:
  - Result:
  - Evidence/path:

## Findings / Observations
- Useful fact:
- Gotcha:
- Pattern noticed:

## Open Loops
- Pending item:
  - Next step:
  - Blocker:

## Follow-ups
- Need to check later:
- Need to ask user:
- Reminder candidate:

## Promote?
- To project `SUMMARY.md`:
- To global `MEMORY.md`:
- Keep only in daily note:
```

---

## 11. Generation Instructions for a New Server

When a new server receives this blueprint:

1. Read the whole blueprint.
2. Generate only the memory files described in section 10.
3. Do not generate persona, identity, provider, model, channel, or server config from this blueprint.
4. Create directories as needed.
5. Customize starter slugs only if the target environment needs different categories.
6. Keep `MEMORY.md` mostly empty except for confirmed global facts.
7. Verify that the memory files exist.
8. Report any values that require user confirmation.

Verification checklist:

```text
MEMORY.md exists
memory/README.md exists
memory/TAXONOMY.md exists
memory/OPERATING_RULES.md exists
memory/TEMPLATE.md exists
memory/projects/_template/SUMMARY.md exists
memory/projects/_template/DAILY.md exists
```

---

## 12. Success Criteria

The memory system is working when:

- global facts stay compact in `MEMORY.md`
- project facts live under `memory/projects/<slug>/SUMMARY.md`
- daily notes are used as staging areas, not permanent truth
- promotion is deliberate and review-based
- sensitive/noisy details are excluded
- another server can regenerate the memory layout from this single blueprint
