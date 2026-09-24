# Crew5

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

Display name: **Crew5** - five roles, one crew. Skill identifier stays
`subagent-team` (stable, grep-able).

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
REPO=https://raw.githubusercontent.com/MEKL20/nano-claw/main/subagent-team

# router + member skills (each folder = one skill)
mkdir -p ~/.hermes/skills/software-development/subagent-team
curl -sL $REPO/SKILL.md -o ~/.hermes/skills/software-development/subagent-team/SKILL.md
for r in architect-subagent coding-subagent qa-subagent security-subagent ui-ux-subagent; do
  mkdir -p ~/.hermes/skills/software-development/$r
  curl -sL $REPO/roles/$r/SKILL.md -o ~/.hermes/skills/software-development/$r/SKILL.md
done

# design rules used by ui-ux-subagent
for d in antislop antislop-ui antislop-copywriting antislop-layoutmobile antislop-human; do
  mkdir -p ~/.hermes/skills/creative/$d
  curl -sL $REPO/design-rules/$d/SKILL.md -o ~/.hermes/skills/creative/$d/SKILL.md
done
mkdir -p ~/.hermes/skills/software-development/antislop-code
curl -sL $REPO/design-rules/antislop-code/SKILL.md -o ~/.hermes/skills/software-development/antislop-code/SKILL.md
# contrast checker + MCP helper for the human skill:
curl -sL $REPO/design-rules/antislop-human/contrast-check.py -o ~/.hermes/skills/creative/antislop-human/contrast-check.py
curl -sL $REPO/design-rules/antislop-human/contrast-mcp.py -o ~/.hermes/skills/creative/antislop-human/contrast-mcp.py

# qa report template lands inside the qa skill:
mkdir -p ~/.hermes/skills/software-development/qa-subagent/templates
curl -sL $REPO/qa-templates/qa-report-template.md -o ~/.hermes/skills/software-development/qa-subagent/templates/qa-report-template.md
curl -sL $REPO/qa-templates/example-stats-cli.md -o ~/.hermes/skills/software-development/qa-subagent/examples/example-stats-cli.md
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
