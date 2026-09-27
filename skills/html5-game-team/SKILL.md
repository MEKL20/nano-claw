---
name: html5-game-team
version: 1.0.0
description: "Use when building an HTML5 game for portal ad revenue."
---

# HTML5 Game Team: research - design - build - qa - asset - ship

Subagent team for HTML5 portal games (CrazyGames primary, Poki second),
run by nano (parent). Children cannot load skills: nano pastes the matching
reference brief into each `delegate_task` task context. Every game run is one
project directory under `~/games/<slug>/`.

| Role | Brief | Does | Never does |
|---|---|---|---|
| Research | references/05-research.md | trend scan of portals, 3 candidate concepts, evidence-based pick + risks | build, design levels, invent popularity numbers |
| Design | references/01-design.md | GDD: core loop, twist, level plan, rewarded slots, acceptance criteria, scope cuts | pick engine (pinned), approve itself |
| Build | references/02-build.md | full game code, levels JSON, solver tool, SDK wrapper, build report | claim play-tested, invent results |
| QA | references/03-qa.md | static+spec+solver+SDK checks with evidence, PASS/FAIL verdict | fix anything |
| Ship | references/04-ship.md | submission package, portal copy, MEKL runbook, metrics plan | touch credentials, submit |
| Asset | references/06-asset-design.md | icon 512, real-gameplay screenshots, cover, visual audit vs GDD | touch js/levels/tools, fake gameplay images |

Parent (nano): verify children, route fixes, relay MEKL, track metrics.
Autonomous mode: after MEKL approves the design gate, run Build→QA loop
without re-asking; gates stay (design, playtest, submission).

## Non-negotiables

1. **Self-report is not evidence.** Parent re-verifies: build exists, size
   budget, solver output, report files. Nothing reaches MEKL on a child's word.
2. **Separation of duties.** QA never fixes; Build never certifies; whoever
   fixes never re-checks the fix.
3. **MEKL owns risk calls.** Approves: game pick, GDD, playtest verdict,
   submission (his portal account, his payout identity).
4. **Escalation guards.** Same QA failure twice = stop, report with evidence.
   Scope change mid-build = back to design gate.
5. **Durable docs.** Every phase writes files into the project dir; chat only
   notifies.

## Project layout

```
~/games/<slug>/
  research/pick.md
  design/gdd.md
  build/          (index.html, js/, assets/, levels/, tools/solver.js)
  build/build-report.md
  qa/report.md
  ship/package.md, runbook.md
  metrics/log.csv
```

## Pipeline

Strategy file → Research (trend scan → pick + evidence) → MEKL game-pick
gate → Design GDD → MEKL design gate → Build → QA verdict loop until
PASS → MEKL playtest → Ship package → MEKL submits manually (~30 min) →
metrics log (plays, conversion ≥1min, plays/day) → 30-day go/no-go.
(For game-001 the research step was done manually by the parent — strategy
file ~/saas-blueocean/game-html5-strategi.md is the pick evidence.)

## Pins (do not re-litigate per game)

Tech: plain JS + Canvas (Phaser only if physics truly needed). Assets: CC0
(Kenney.nl) or generated (jsfxr). Audio: sfx only, no music licensing.
Budget: build <8MB compressed, first playable frame <3s on mid-range phone.
SDK: CrazyGames SDK v3 behind a mock adapter so the game runs without it.
Monetization: ≥3 natural rewarded-video hooks (undo/continue/skip).
Platforms: portal web only for v1 — mobile port is a separate decision after
metrics prove the mechanic.

## Cost discipline

New game = full pipeline (Research → Design → Build → QA → Ship). Level
pack or fix = Build + QA only. Trend scan or concept exploration = Research
brief alone. Skip roles whose risk is absent — never skip parent
verification, the MEKL gates, or the solver check.

## Metrics (parent role, no subagent)

30 days post-launch: parent reads portal dashboard numbers (MEKL pastes or
screenshot), logs to metrics/log.csv. Go/no-go: <10k plays OR <35%
1-minute conversion → post-mortem, next game reuses codebase. >100k plays +
healthy retention → level pack, Poki submit, evaluate mobile port.
