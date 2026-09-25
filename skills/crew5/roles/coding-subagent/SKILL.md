---
name: coding-subagent
version: 1.0.0
description: "Spawn coding subagents that always load karpathy-guidelines."
---

# Coding Subagent (karpathy-guidelines hard-wired)

Spawn a coding/fullstack subagent whose output follows the four Karpathy
principles: think before coding, simplicity first, surgical changes,
goal-driven execution.

## Rule

Every coding task sent to `delegate_task` MUST open its `context` with this
exact block (untrusted-subagents can't load skills themselves, so the
principles travel inside the prompt):

```
CODING PRINCIPLES (mandatory, follow strictly):
1. Think before coding - state assumptions; if 2+ interpretations exist,
   present all instead of picking silently; push back if a simpler approach exists.
2. Simplicity first - minimum code that solves the problem; no unrequested
   features/abstractions/config; stdlib and already-installed deps first.
3. Surgical changes - touch only what the task requires; match existing style;
   no drive-by refactors; every changed line traces to the request.
4. Goal-driven execution - define verifiable success criteria up front;
   run the code/tests and report real output; never claim done without a check.
```

Also require in every task: `Final message = what was built, files touched,
how it was verified (commands + output).`

## Spelling a task

- `goal`: one concrete deliverable ("write", "fix", "add X to Y"), not "look at".
- `context`: principle block + file paths + constraints (language, style, test
  command, forbidden actions like git push).
- Prefer one task = one deliverable. Parallel children for parallel modules.

## UI/FE tasks (compact anti-slop, when NOT using ui-subagent)

For small UI touches handled by a plain coding task, paste this instead of
the full ui-subagent workflow:

```
UI-SLOP RULES (compact):
- No default blue-purple/pastel gradients or glows; no glassmorphism on
  more than 1-2 elements; radius from a small set, not pill-everything.
- No fabricated content: no invented stats, testimonials, logos, or
  features. Empty beats fake.
- Every button/link does something real or is removed; keyboard reachable,
  visible focus.
- Text contrast WCAG AA: 4.5:1 normal, 3:1 large.
- Copy: no em dash, no AI buzzwords (AI Powered/Seamless/Revolutionary),
  specific CTAs (not "Get Started").
- Include empty/loading/error states; no network-fetched assets.
- No brand direction given = say so, keep it plain, no invented style.
```

Full UI builds (landing pages, product surfaces, design-heavy work) get a
design first: ui-ux-subagent (DESIGN.md / audit) then back here to build.
Parent decides which tier per task.

## Parent duties (cannot be delegated)

- Verify claims yourself: child summaries are self-reports. Re-run the test
  command or check the artifact exists before reporting success upward.
- Vetting an external skill/repo first? untrusted-repo-audit skill.

## Comment hygiene (antislop-code, audited 2026-09-23)

When writing code, comments follow the antislop-code rules (full list:
`~/.hermes/skills/software-development/antislop-code/SKILL.md`, from
miqdadbadjuber/anti-slop, audit clean). Paste this into coding tasks that
write comments:

```
COMMENT RULES (antislop-code):
FORBIDDEN as slop: decorative separators/banner comments (// ==== X ====),
restating the code (// set count to 0), step narration (// Step 1: ...),
empty labels (// main logic, // helper), vague TODOs (// improve this),
signature-echo docs, decorative emoji in comments, end markers (} // end if),
line-by-line commentary, over-explained multi-line padding of a one-line fact.
Keep (never strip): business logic/intent, architectural decisions, security
notes, performance trade-offs, workarounds, edge cases, API contracts,
license notices. A comment earns its place by saying what the code does not.
Style: short, sentence case, one per logical block, explains why not what.
```

Cleanup tasks ("remove slop comments") get one extra line in the task:
`Scope guardrail: touch ONLY comments - never code, identifiers, imports,
formatting, or logic.`

## Provenance

karpathy-guidelines skill = from multica-ai/andrej-karpathy-skills, audited
clean 2026-09-23 (untrusted-repo-audit, clone at ~/audit/andrej-karpathy-skills,
sha256 6e22cc54...b2aea7). antislop-code rules = from miqdadbadjuber/anti-slop,
audited clean 2026-09-23 (51 files, 102 commits, clone at ~/audit/anti-slop).
Keep both installed copies pristine - re-audit before updating from upstream.

On architect-led projects, task context cites the relevant T-n from
docs/BACKLOG.md and the FR acceptance criteria from docs/PRD.md - the
coder implements against the approved spec, not against chat memory.

## Known limitation

Subagents cannot call skill_view - that is why the block is pasted into the
prompt instead of relying on the skill system. If delegate_task ever gains
skill injection, switch to it and delete this note.
