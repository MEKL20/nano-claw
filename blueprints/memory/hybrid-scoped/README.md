# Hybrid Scoped Memory Blueprint

A reusable memory concept for AI assistants and workflow orchestrators.

## What it is

A lightweight, local-first Markdown memory system with three layers:

1. **Global durable memory** — stable cross-project facts and preferences.
2. **Project durable memory** — long-lived context for a specific project/domain.
3. **Daily working memory** — temporary notes, work logs, open loops, and promotion candidates.

## What it is not

This blueprint does not define persona, model/provider config, channel config, server config, or private live workspace data.

## Use on a new server

1. Copy `BLUEPRINT.md` to the target workspace, or provide its contents to the target assistant.
2. Ask it to read the blueprint fully.
3. Ask it to generate only the memory files described in the blueprint.
4. Keep `MEMORY.md` compact.
5. Promote facts upward only when stable, safe, and reusable.
