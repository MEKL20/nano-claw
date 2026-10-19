---
name: html5-game-team
version: 1.4.0
description: "Use when building an HTML5 game for portal ad revenue."
---

# HTML5 Game Team: research - design - build - qa - asset - ship

Persistent agent team for HTML5 portal games (CrazyGames primary, Poki
second), run by nano (parent). Each role is its own Hermes profile —
`game-{research,design,build,qa,ship,asset}` — with a role SOUL carrying
identity + absolute gates (crew-coding pattern). Dispatch = kanban task →
profile worker; the worker reads its own role brief from this skill's live
`references/` path (pinned in its SOUL), so the parent no longer pastes
briefs. Every game run is one project directory under `~/games/<slug>/`.

| Role | Profile | Brief (worker self-loads) | Does | Never does |
|---|---|---|---|---|
| Research | game-research | references/05-research.md | trend scan of portals, 3 candidate concepts, evidence-based pick + risks | build, design levels, invent popularity numbers |
| Design | game-design | references/01-design.md | GDD: core loop, twist, level plan, rewarded slots, acceptance criteria, scope cuts | pick engine (pinned), approve itself |
| Build | game-build | references/02-build.md | full game code, levels JSON, solver tool, SDK wrapper, build report | claim play-tested, invent results |
| QA & Tester | game-qa | references/03-qa.md | ONE quality gate: static+spec+solver+draw-path audit THEN real-browser playtest (playthrough, feel, orientation continuity, mobile, persistence), single PASS/FAIL | fix anything, report without measured evidence, write human flags |
| Ship | game-ship | references/04-ship.md | submission package, portal copy, MEKL runbook, metrics plan | touch credentials, submit, write human flags |
| Asset | game-asset | references/06-asset-design.md + 07-style-guide.md | PRE-build: style guide (hex-level art spec, contrast gates). POST-build: icon 512, real-gameplay screenshots, cover, pixel audit vs style guide | touch js/levels/tools, fake gameplay images, skip contrast gates |

Parent (nano): verify workers, route fixes, relay MEKL, track metrics.
Autonomy (MEKL standing order, 2026-09-27): parent DECIDES game pick, GDD
approval, asset acceptance, and fix routing without asking. MEKL touches
the pipeline twice: playtest verdict (quality) and portal submission
(physical action — his account, his payout identity). Gates are evidence
checks, not permission requests.

## Non-negotiables

1. **Self-report is not evidence.** Parent re-verifies: build exists, size
   budget, solver output, report files. Nothing reaches MEKL on a worker's word.
2. **Separation of duties.** QA never fixes; Build never certifies; whoever
   fixes never re-checks the fix.
3. **Parent owns judgment calls.** Pick, GDD sign-off, asset acceptance,
   FAIL→fix routing = parent decides with evidence. MEKL plays and submits.
4. **Escalation guards.** Same QA failure twice = stop, report with evidence.
   Scope change mid-build = back to design.
5. **Durable docs.** Every phase writes files into the project dir; chat only
   notifies.
6. **A stuck loop is a design signal, not a budget problem.** Two failed
   attempts at the same wall = stop tweaking parameters, instrument instead
   (log what the rejected candidates actually scored), then change the
   constraint. Timebox every generate-and-test loop so it fails loudly
   rather than hanging.
7. **Relax the producer and the checker in the same change.** A constraint
   loosened in one and not the other turns into phantom failures that look
   like real regressions.
8. **Human gates are human-only.** MEKL's playtest and submission flags are
   recorded by HIS click on the board. An agent writing one of those flags
   fabricates approval — the one failure this pipeline cannot detect later.

## Project layout

```
~/games/<slug>/
  research/pick.md
  design/gdd.md
  build/          (index.html, js/, assets/, levels/, tools/)
  build/tools/    solver.js (one level), check.js (ALL criteria), gen-levels.js
  build/build-report.md
  qa/report.md    + pt-*.js probes, evidence PNGs
  ship/package.md, runbook.md, build.zip
  metrics/log.csv
```

Nothing else belongs in the project dir. Sweep leftovers (probe scripts,
nested `<slug>/<slug>/` dirs) before declaring a phase done — degraded
degraded workers create them and they silently ship inside the zip

## Reference index (which worker self-loads which brief)

| Reference | Read by (worker self-loads via its SOUL pin) | Parent-only |
|---|---|---|
| 00-ops.md | nobody — parent reads before EVERY dispatch | yes |
| 01-design.md | game-design | |
| 02-build.md | game-build (both dispatches) | |
| 03-qa.md | game-qa | |
| 04-ship.md | game-ship | |
| 05-research.md | game-research | |
| 06-asset-design.md | game-asset (post-build) | |
| 07-style-guide.md | game-asset (pre-build) | |
| 08-levelgen.md | whoever touches the generator (often the parent) | |
| 09-dashboard.md | nobody — parent operates the board | yes |

Every task body still carries: project dir path, the host facts below that
touch the job, and the exact files to read/write — workers get zero
conversation context and cannot see this table.

Bundled, so the pipeline needs nothing external:

- `scripts/game_dashboard.py` — the console (stdlib only, no deps)
- `templates/games-dashboard.service` — systemd --user unit, `%h` paths

## Role profiles & kanban dispatch (since v1.4.0)

Profiles `game-{research,design,build,qa,ship,asset}` under
`~/.hermes/profiles/`, built on the proven crew-coding pattern: config.yaml =
`custom:9router` (empty provider fields → workers 403), SOUL.md = role
profiling + absolute gates (including the human-flag forgery ban on every
role), `roles/` in this skill = portable SOUL backup. Edit one SOUL → sync
the backup → bump this skill's version → push nano-claw.

One board per game run:

```sh
hermes kanban boards create game-<slug> --default-workdir ~/games/<slug> --switch
```

One stage = one task, created ONLY after the previous stage's gate passed —
the parent's sequential cadence is the anti-premature-spawn guard (park
not-yet-startable work in triage, never in ready). Task body = the CAG:
project dir, exact files to read/write, host facts that touch the job,
forbidden actions, gate numbers. Example (stage 4a):

```sh
hermes kanban create "stage-4a build: levels + tools + assets" \
  --body "ROLE: build (dispatch 4a). Project dir: ~/games/<slug>. READ: design/gdd.md, design/style-guide.md. WRITE: build/levels/*.json, build/tools/{solver.js,check.js,gen-levels.js}, build/assets/. GATES: node tools/check.js ends ALL CHECKS PASSED; node --check every .js. HOST: node v22, no zip CLI, check.js ~60s on 100 levels. RULES: one file per call; 2 consecutive tool failures = STOP; never write outside the project dir. FORBIDDEN: js/ runtime (that is 4b), qa/, git commit/push, messaging MEKL." \
  --assignee game-build --workspace dir:$HOME/games/<slug> --json
hermes kanban dispatch
```

Watch long runs with a background poller on `hermes kanban list --json`
(crew-coding recipe), never a foreground sleep loop. The task result + the
artifacts on disk are the report; the parent re-runs the stage gate itself
before creating the next task. `hermes --profile game-<role> -z "<question>"`
is for identity/gate tests only, never for real work.

Fallback if the kanban/profile stack is broken: `delegate_task` still works —
paste the role brief + the full CAG + the SOUL gates verbatim into the task
context (delegate children cannot load skills or read the SOUL), and pin
`delegation.provider` to `custom:9router` (see 00-ops).

## Host facts (cached — do not re-derive, do not let workers rediscover)

- `node` v22 present. `zip` CLI is **absent**; package with `python3`
  `zipfile` (stdlib). `unzip` exists for verification.
- Level verification is two tools: `node tools/solver.js levels/level-NNN.json`
  (one level, prints move list) and `node tools/check.js` (reads every
  `levels/level-*.json` itself, no args, prints criteria 1-9 then
  `ALL CHECKS PASSED` or `N FAILURES`). check.js is the gate; solver.js is
  for inspecting one board. check.js on 100 levels takes ~60s — budget for it.
- Test server: `python3 -m http.server` from `build/`. No build step.
- Browsers: Playwright chromium at `~/.cache/ms-playwright`, driver pkg only
  in the npx cache (`find ~/.npm/_npx -maxdepth 4 -type d -name playwright`,
  then NODE_PATH at its parent `node_modules`). `browser_exec` uses its own
  Chrome under `~/.agent-browser/browsers/`.
- No vision on this host: never ask anyone to look at an image. Measure
  pixels programmatically (getImageData counts, PIL histograms, WCAG
  luminance).
- GitHub: SSH key `~/.ssh/id_ed25519` on the MEKL20 account. No gh CLI.
  Never route a token through chat or a file.

## Cycle

One stage = one owner, one durable artifact, one exit gate the parent can
verify by running something. No stage is "done" on a worker's summary, and
the dashboard state is derived from the artifacts, never set by hand.

| # | Stage | Owner | Artifact | Exit gate (parent runs it) | Board |
|---|---|---|---|---|---|
| 1 | Research | worker | research/pick.md | pick has cited evidence + named risks | RESEARCHED |
| 2 | Design | worker | design/gdd.md | acceptance criteria measurable + scope cuts listed | DESIGNED |
| 3 | Style guide | game-asset | design/style-guide.md | every contrast gate COMPUTED, not asserted | DESIGNED |
| 4 | Build a | worker | levels/, tools/, assets/ | `node tools/check.js` → ALL CHECKS PASSED | BUILDING |
| 5 | Build b | worker | js/, index.html | `node --check` each file; game boots and accepts input | BUILDING |
| 6 | QA & Tester | worker | qa/report.md | `VERDICT: PASS`, every check backed by command output | PLAYTEST |
| 7 | Asset post-build | game-asset | assets-out/ | pixel audit vs the declared gates, real game pixels | PLAYTEST |
| 8 | Ship | worker | ship/package.md, runbook.md, build.zip | fields complete; archive verified from INSIDE the zip | READY |
| 9 | Playtest | **MEKL** | ship/playtested.flag | his verdict — board unlocks submit | PLAYTESTED |
| 10 | Submit | **MEKL** | ship/submitted.flag | portal submission, his account | SUBMITTED |
| 11 | Metrics | parent | metrics/log.csv | 30-day go/no-go | LIVE |

Stages 9-10 are MEKL's. **Agents never write `playtested.flag`,
`submitted.flag`, or `live.flag`** — those are clicks on the board, and
writing one from a script forges a human gate.

Ship (8) runs before the playtest (9) on purpose: packaging is cheap and
reversible, submitting is not. Any fix after packaging invalidates the
archive — re-run Ship, then re-verify the zip's own contents.

## Fix loops (who fixes what)

- QA FAIL → **Build** fixes; a FRESH QA pass re-verifies ALL checks, not
  just the fixed one. QA never fixes; the fixer never re-checks.
- MEKL playtest finding → same route as a QA FAIL, plus re-run Ship.
- Asset gate failure → **Build** changes the code, Asset re-audits. Asset
  never edits js/levels/tools.
- Generator wall → see references/08-levelgen.md; instrument before tuning.
- Same failure twice → stop, report with evidence (non-negotiable 4).

A FAIL verdict outranks a finished package on the board, so a post-Ship fix
loop shows as QA-FIX instead of silently sitting at READY.

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

New game = full cycle (stages 1-11). Level pack or fix = Build + QA, then
re-run Ship because the archive went stale. Trend scan or concept
exploration = Research brief alone. Skip roles whose risk is absent — never
skip parent verification, the MEKL gates, or the `check.js` gate.

One task per stage, dispatched sequentially: each worker's input is the
previous stage's artifact. Parallel tasks only for genuinely independent work
(e.g. game-asset post-build while game-ship drafts copy), and never two
workers in the same directory.

## Metrics (parent role, no subagent)

30 days post-launch: parent reads portal dashboard numbers (MEKL pastes or
screenshot), logs to metrics/log.csv. Go/no-go: <10k plays OR <35%
1-minute conversion → post-mortem, next game reuses codebase. >100k plays +
healthy retention → level pack, Poki submit, evaluate mobile port.

## Level generation

Procedural generation with a solver in the loop has its own failure modes
(sampler starvation, window ratchets, misleading single-level probes). Nine
field-tested rules live in references/08-levelgen.md — read it before
editing a generator, not after the first wall.

Headline: run the chain in the background, instrument rejected candidates
before adjusting parameters, and treat `check.js` as the only gate.

## Dashboard

The board is part of this bundle, not separate infrastructure:
`scripts/game_dashboard.py` + `templates/games-dashboard.service`. Install:

```sh
cp scripts/game_dashboard.py ~/games/tools/
cp templates/games-dashboard.service ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now games-dashboard
```

It derives every state from artifacts (precedence in the module docstring),
serves the playtest frame, and is where MEKL records his two gates. Token in
`$GAMES_ROOT/dashboard.token` is a capability URL — never paste it anywhere.

Operating notes, the state-precedence rationale, and the bugs that hid behind
a plausible-looking panel live in references/09-dashboard.md. Read it before
editing the board; verify changes through the rendered page, never the source.
