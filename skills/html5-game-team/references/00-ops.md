# Ops notes (parent reads before dispatching)

## Delegation mechanics
- Children cannot load skills or memory: paste the role brief + all needed
  context into task context. Repeat shared background in every task.
- delegation.provider must stay custom:9router. child_timeout 1800.
- Long tasks: stub the output file first, tell child to append evidence as it
  lands; parent reads the file, not the chat summary.
- Child reports are self-reports. Parent verifies on disk before relaying.

## Parent verification checklist
- Design: gdd.md exists, has acceptance criteria + scope cuts, no engine
  debate.
- Build: `ls build/` matches report; `du -sh build/` under budget; solver
  run by parent once (`node tools/solver.js levels/*.json` → all SOLVED);
  build-report.md numbers match disk.
- QA: report has per-check evidence (file:line or command output), explicit
  PASS/FAIL verdict.
- Ship: package.md fields complete, no credential material inside.

## Environment
- Child timeout: delegation.child_timeout_seconds = 3600 (raised from 1800
  on 2026-09-27 after 2 visual-fix children died at 30min mid-verification).
  Single-child dispatches may now run the full QA&Tester job; still keep
  verification cheap (scripts reuse qa/pt-* patterns).
- Verify `node -v` exists before promising solver runs; fallback: python
  check script (write one, put in tools/).
- Local test server: `python3 -m http.server` in build/ (no build step).
- Host is a laptop (CLEVO, no AVX2): nothing here needs AVX; fine.
- Browser tooling (since 2026-09-27): Playwright chromium installed at
  ~/.cache/ms-playwright. Node driver pkg lives ONLY in the npx cache —
  locate it with `find ~/.npm/_npx -maxdepth 3 -name playwright -type d`
  and run node scripts with NODE_PATH pointing at that dir's parent node_modules.
  Probe tools: ~/games/tools/boot-probe.js (boot state + PLAY click) and
  deep-probe.js (paint coverage + crash stack). QA and Asset Designer use
  these for real evidence. First install attempt failed on broken apt deps
  — fix with `sudo apt-get --fix-broken install` first.
- No vision on this host: never ask anyone to 'look at' an image. Analyze
  pixels programmatically (getImageData counts, palette histograms).

## Dashboard + publishing infra
- games.mekl.my.id → cloudflared tunnel 'nano-bot' → 127.0.0.1:8792
  (~/games/tools/game_dashboard.py, systemd --user games-dashboard.service,
  token in ~/games/dashboard.token). Status derived from files; SUBMITTED/
  LIVE flags live in <slug>/ship/. Tunnel config edits: backup
  ~/.cloudflared/config.yml first, then `cloudflared tunnel route dns
  nano-bot <host>` + restart system cloudflared-tunnel.service.
- GitHub push: no gh CLI, no stored PAT. MEKL pastes PAT in chat → throwaway
  script → scrub token from disk after. Repo: github.com/MEKL20/nano-claw.

## Lesson (game-001, 2026-09-27): never one monolithic Build child
A single Build child given code+levels+solver+assets+report hit the 1800s
timeout, then DEGENERATED on its final writes: tool calls wrote garbage
paths (~/arguments: [...], wrong slug dir) and engine.js came out corrupted
(duplicate consts, placeholder tokens). Levels+solver survived and were
good. Rules going forward:
1. Split Build into 2 dispatches: (a) levels+tools+assets, (b) runtime
   modules (engine/render/sfx/adapter/main/index). Parent verifies (a) on
   disk + runs solver BEFORE dispatching (b).
2. Every build child: write one file per call, `node --check` after each
   .js, hard rule 'never write outside the project dir', and '2 consecutive
   tool failures = STOP and report'.
3. Parent always re-runs solver + node --check after any build child —
   corruption shows up in files, not in the child's summary.
4. Garbage files can land in ~/ (e.g. 'arguments: ...' files, sibling slug
   dirs) — sweep after a degraded child dies.

## Portal facts (checked 2026-09, re-verify each quarter)
- CrazyGames: dev share ~60% ads (jam terms), ~300M sessions/mo, €100 payout
  min via Tipalti (payment onboarding BEFORE submission), sitelock auto,
  compressed builds only (Brotli/Gzip), 2-month launch exclusivity raises
  share ~50%. SDK v3 required. Manual quality review per game.
- Poki: 50/50 on Poki-sourced traffic, 100% on own traffic; web exclusivity
  (5y default) for full terms; closed-beta dev onboarding — apply early.
- Rewarded video eCPM US ~$28; banners ~$1.50 — rewarded-first design.
- Realistic revenue: decent portal game ~$400/mo per 100k plays; 80% of
  games $0-50/mo. Portfolio play, hit rate ~1:5.

## Game-001 pin (current run)
- Slug: parking-jam-001. Concept: parking-jam exit puzzle + color-gate twist
  (cars may only exit through their color gate). Strategy file:
  ~/saas-blueocean/game-html5-strategi.md (this IS the research evidence;
  no separate research/pick.md for 001 — Research role starts at 002).
- 10 handcrafted levels v1. Level file = JSON (grid, cars, gates, par).
- Submission target: CrazyGames. Copy in English (US audience).
