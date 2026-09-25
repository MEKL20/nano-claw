# AGENTS.md — nano-claw

Rules for any AI agent working in this repository (Hermes, Claude Code,
Codex, OpenCode, ...). Keep them when adding content.

## What this repo is

A portable library of **blueprints** (concepts for fresh servers/workspaces)
and **skills** (installable agent skill packages). Plain markdown, no build
step, no runtime. MIT-licensed with attribution.

## Layout conventions

```
blueprints/<category>/<blueprint-name>/
    BLUEPRINT.md        the portable concept
    README.md           scope + quick usage
skills/<skill-name>/     one folder per skill (folder name = skill id)
    SKILL.md            required entry file (frontmatter: name, version,
                        description) + body
    (supporting files as needed: templates/, examples/, scripts/)
```

Rules:

- One skill = one folder. Folder name = frontmatter `name`. Lowercase,
  hyphenated, stable once published — renames break installs.
- Every skill folder must be self-contained: anyone should be able to copy
  that one folder into an agent and use it.
- Root `README.md` maintains two tables: Available blueprints, Skills. Add
  a row when you add an entry — an unlisted skill does not exist.

## Bundled third-party rules (do not skip)

This repo bundles rule content from external repos (currently: antislop
packs from `miqdadbadjuber/anti-slop`, karpathy-guidelines from
`multica-ai/andrej-karpathy-skills`). When touching those files:

- Keep their LICENSE/attribution notes intact (see `skills/crew5/LICENSE`).
- NEVER update bundled content from upstream without re-auditing the
  source repo first (supply-chain rule: an update is a new supply, not a
  trusted diff). Record the audit date next to the provenance note in the
  skill that consumes it.
- Do not "improve" bundled third-party content in place — propose changes
  upstream or fork with a clear marker.

## Content rules for skills

- Rules must be field-tested before being written down as mandatory; note
  the test in the skill (see existing "Field test" sections).
- Prefer imperative, checkable rules over vibes ("re-run the test and
  report output", not "be careful").
- Keep each SKILL.md focused; split by role/concern rather than growing
  one giant file.
- Provenance section in each skill: source repo, audit date, clone/commit
  if applicable.

## Before you commit

- Markdown only; no binaries without asking.
- Check the diff: no secrets, no tokens, no absolute personal paths
  (`/home/mekl/...`) in published files — use `$HERMES_HOME` / `~`
  conventions in examples.
- Update the relevant README table(s) in the same commit.
