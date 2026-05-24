# nano-claw

Reusable blueprints for MEKL's systems, workflows, and OpenClaw/nano setup.

This repo is intended as a clean library of portable concepts that can be reused on new servers or fresh assistant workspaces.

## Structure

```text
blueprints/
└── <category>/
    └── <blueprint-name>/
        ├── BLUEPRINT.md
        └── README.md
```

## Available blueprints

| Blueprint | Category | Purpose |
| --- | --- | --- |
| [Hybrid Scoped Memory](./blueprints/memory/hybrid-scoped/) | `memory` | Lightweight local-first memory layout using global, project, and daily memory layers. |

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
