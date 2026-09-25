# nano-claw

Reusable blueprints and skills for MEKL's systems, workflows, and OpenClaw/nano setup.

This repo is intended as a clean library of portable concepts that can be reused on new servers or fresh assistant workspaces.

## Structure

```text
blueprints/
└── <category>/
    └── <blueprint-name>/
        ├── BLUEPRINT.md
        └── README.md
skills/
└── <skill-name>/          e.g. skills/crew5/
    └── SKILL.md (+ supporting files)
```

## Available blueprints

| Blueprint | Category | Purpose |
| --- | --- | --- |
| [Hybrid Scoped Memory](./blueprints/memory/hybrid-scoped/) | `memory` | Lightweight local-first memory layout using global, project, and daily memory layers. |

## Skills

Installable, self-contained skills (drop into `~/.hermes/skills/` or paste
the principle blocks into any agent framework):

| Skill | Purpose |
| --- | --- |
| [Crew5](./skills/crew5/) | A complete audited agent team - plan, design, build, test, secure - five specialist roles plus one human approval gate. |
| [KDP Team](./skills/kdp-team/) | Five-role Amazon KDP publishing pipeline - research, production, SEO, QA, publish - with AI-disclosure compliance and manual-upload runbook. |

## Usage

1. Choose a blueprint folder.
2. Read its `README.md` for scope and quick usage.
3. Give its `BLUEPRINT.md` to the target server/assistant.
4. Ask the target to generate only the files described by that blueprint.
5. Customize only confirmed local values.

## Principles

- Simple first.
- Local-first when possible.
- Auditable over magical.
- Keep private live workspace data out of reusable blueprints.
- Prefer concepts and templates over machine-specific configuration.
