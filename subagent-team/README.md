# subagent-team

One audited AI agent software team — plan, design, build, test, secure —
shipped as installable agent skills. Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent),
portable to any agent framework with a spawn/delegate primitive.

Five specialist roles + one human approval gate. Every rule was live-tested
before being written down.

## Roles

| Role | Skill | Does | Never does |
|---|---|---|---|
| Brain | architect-subagent | PRD, stack options, ERD, threat model, backlog | implement |
| Design | ui-ux-subagent | DESIGN.md, UX critique, antislop audit | implement |
| Hands | coding-subagent | implement (Karpathy principles + comment hygiene) | self-verify as final |
| Evidence | qa-subagent | black-box testing, bug reports, re-tests | fix |
| Finder | security-subagent | vuln findings, PoCs, coverage ledger | fix, exceed scope |
| Parent | your main agent | verify, route, triage, relay approvals | delegate verification |

## The 5 non-negotiables

1. **Self-report is not evidence** — the parent re-verifies every child
   claim (re-run tests/repros/measurements) before it reaches the human.
2. **Separation of duties** — the one who produces never certifies. QA does
   not fix; the designer does not implement; the coder does not re-test
   their own fix; security does not patch.
3. **The human owns risk calls** — PRD/stack/infra approval, design
   direction, dynamic security testing (per-run), destructive or external
   actions, production data. Children propose; the human decides.
4. **Escalation guards, not infinite loops** — same failure twice = stop
   and escalate with evidence. Scope creep = back to the docs first.
5. **Durable docs over chat** — reports/PRDs/decisions are markdown files
   in the project. Chat is a notification; files are truth.

## What's inside

```
SKILL.md              router + rulebook (start here)
roles/                the five member skills (one SKILL.md each)
design-rules/         antislop rule packs (core, ui, copywriting,
                      layout/mobile, human/a11y + contrast-check.py)
qa-templates/         QA report template + filled worked example
```

## Rules sources (audited before adoption)

- [karpathy-guidelines](https://github.com/multica-ai/andrej-karpathy-skills)
  — coding principles (audited clean 2026-09-23)
- [anti-slop](https://github.com/miqdadbadjuber/anti-slop) v3.2.14 —
  anti-AI-slop design/copy/comment rules (audited clean 2026-09-23)
- Design reference for the security role's methodology:
  [strix](https://github.com/usestrix/strix) (audited clean 2026-09-23;
  closure discipline, counterevidence pass, coverage ledger)

Re-audit any external source before adopting updates. An audit is a
snapshot, not an endorsement forever.

## Install (Hermes)

```bash
# member skills
cp roles/*-SKILL.md ~/.hermes/skills/software-development/
# rename each to <name>/SKILL.md layout, e.g.
#   ~/.hermes/skills/software-development/architect-subagent/SKILL.md

# design rules used by ui-ux-subagent
cp -r design-rules/* ~/.hermes/skills/creative/
cp -r roles/creative/antislop-code ~/.hermes/skills/software-development/
```

## Install (other agents)

Any framework with (a) spawned sub-conversations, (b) file read access for
children, (c) a human channel for approval relays. Paste each member
skill's principle block as the child's system prompt / task preamble. The
workflow contracts are framework-agnostic — see SKILL.md "Adaptation notes".

## License

MIT. The bundled antislop rule packs keep their original MIT license
(miqdadbadjuber/anti-slop). karpathy-guidelines is MIT
(multica-ai/andrej-karpathy-skills).
