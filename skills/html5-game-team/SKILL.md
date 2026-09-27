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
| QA & Tester | references/03-qa.md | ONE quality gate: static+spec+solver+draw-path audit THEN real-browser playtest (playthrough, feel, orientation continuity, mobile, persistence), single PASS/FAIL | fix anything, report without measured evidence |
| Ship | references/04-ship.md | submission package, portal copy, MEKL runbook, metrics plan | touch credentials, submit |
| Asset | references/06-asset-design.md + 07-style-guide.md | PRE-build: style guide (hex-level art spec, contrast gates). POST-build: icon 512, real-gameplay screenshots, cover, pixel audit vs style guide | touch js/levels/tools, fake gameplay images, skip contrast gates |

Parent (nano): verify children, route fixes, relay MEKL, track metrics.
Autonomy (MEKL standing order, 2026-09-27): parent DECIDES game pick, GDD
approval, asset acceptance, and fix routing without asking. MEKL touches
the pipeline twice: playtest verdict (quality) and portal submission
(physical action — his account, his payout identity). Gates are evidence
checks, not permission requests.

## Non-negotiables

1. **Self-report is not evidence.** Parent re-verifies: build exists, size
   budget, solver output, report files. Nothing reaches MEKL on a child's word.
2. **Separation of duties.** QA never fixes; Build never certifies; whoever
   fixes never re-checks the fix.
3. **Parent owns judgment calls.** Pick, GDD sign-off, asset acceptance,
   FAIL→fix routing = parent decides with evidence. MEKL plays and submits.
4. **Escalation guards.** Same QA failure twice = stop, report with evidence.
   Scope change mid-build = back to design.
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

Strategy file → Research (parent picks with evidence) → Design GDD (gameplay)
→ ASSET pre-build: style guide (exact hexes + declared contrast gates) →
Build (2 dispatches; implements GDD + style guide; parent verifies solver
between) → QA & Tester: one quality gate, static THEN real-browser
playtest, verdict loop until PASS → ASSET post-build: pixel audit vs
gates + icon/screenshots → fix loop if gates/playtest fail → MEKL playtest (only
human quality gate) → Ship package → MEKL submits manually (~30 min, his
account) → metrics log → 30-day go/no-go.
(For game-001 research + style guide were done retroactively the hard way:
a full redesign cycle. Their cost is why both now run before build.)

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
