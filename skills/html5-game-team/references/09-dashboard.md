# Dashboard (bundled console)

`scripts/game_dashboard.py` — stdlib-only, token-gated HTTP console for the
cycle: shelf, per-game detail, playtest frame, publish page, live agents
panel. It is the surface where MEKL plays the game and records his two
gates. Status is DERIVED from artifacts; nothing on this board is set by
hand.

## Install

```sh
mkdir -p ~/games/tools ~/.config/systemd/user
cp scripts/game_dashboard.py ~/games/tools/
cp templates/games-dashboard.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now games-dashboard
```

A token is generated on first run into `$GAMES_ROOT/dashboard.token`; every
URL is `/<token>/...`. Override the project root with `GAMES_ROOT`, and the
delegation transcript dir with `AGENTS_LIVE_DIR`.

Exposure is a tunnel to `127.0.0.1:<port>` (cloudflared on this host). The
token in the path IS the only auth — it is a capability URL: treat it as a
secret, never paste it into a report, a commit, or chat.

## State precedence (one place, do not duplicate the logic)

```
live.flag > submitted.flag > QA 'VERDICT: FAIL' > playtested.flag >
ship/package.md > QA 'VERDICT: PASS' > qa/report.md > build/index.html >
design/*.md > research/pick.md > SETUP
```

Two deliberate choices in that order:

- **A QA FAIL outranks a finished package.** With `package.md` checked first,
  one Ship run pinned the board at READY forever and a post-ship fix loop was
  invisible.
- **`playtested.flag` is its own state.** READY used to mean both "waiting for
  MEKL to play" and "MEKL approved", so nothing could tell an approved submit
  from one that skipped the gate.

## Human gates

`playtested.flag`, `submitted.flag`, `live.flag` in `<slug>/ship/` are written
ONLY by a confirm click on the board. The publish page keeps submit locked
until the playtest flag exists.

Agents must never create these files. Forging one fabricates a human
approval, and it is the single failure mode nothing downstream can detect.
When testing the gate chain, delete the test flag afterwards and verify it is
gone.

## Agents panel

Reads delegation transcripts under `AGENTS_LIVE_DIR` and shows the newest run
per role, plus a PARENT row.

`AGENTS_LIVE_DIR` is the agent runtime's own cache, NOT inside `GAMES_ROOT`:
a relocated root still sees the host's global delegation history, so rows may
name slugs that do not exist under that root. Expected, not a bug — point
`AGENTS_LIVE_DIR` at an empty dir to isolate a test instance.

The PARENT row exists because parent-executed work leaves no transcript: the
board kept showing a dead child's FAILED row as if it were current state. The
PARENT row runs the real gate (`check.js`) and reports that verdict, so the
panel shows measured state rather than the newest child's self-report.

`check.js` costs ~60s on 100 levels and the panel polls every 5s, so the
verdict is cached per slug, invalidated by the `levels/` dir mtime with a TTL
floor. Any status wrapper that shells out per request needs the same
treatment or it will pile up overlapping processes and stall the server.

## Lessons (each cost a debugging session)

- **Build poll URLs from the token, not `location.pathname`.** `/<token>`
  without a trailing slash plus `'agents.json'` concatenates into
  `/<token>agents.json`, fails the token check, and the 404 body gets painted
  into the panel AS ITS CONTENT — the panel read "not found" and looked like
  a missing agent. Use an absolute `/<token>/agents.json` and check `r.ok`, so
  a failure reads as "unavailable, retrying" instead of posing as data.
- **A panel that renders is not a panel that works.** Both bugs above
  produced plausible-looking output. Verify through the rendered page (real
  browser, both URL forms), never by reading the source.
- **Age math**: rows carry seconds. Days = `minutes // 1440`, not
  `minutes // 24` — the latter inflates every day figure 60x, so 1.2 days
  rendered as "72d".
- **Every state needs a CHIP entry.** A missing key is a KeyError at render
  time: a blank page, not a styling glitch. Adding a state means adding its
  chip in the same change.
- **A new state also needs to be reachable.** `games()` only lists dirs that
  have artifacts; until `research/*` counted, a research-only game never
  appeared on the shelf and RESEARCHED could not occur. Prove a new state
  with a temp slug, then delete it.
- **`systemctl --user restart` kills agent-started child processes** in the
  same user slice. Restart deliberately; re-verify after.
- **Stopping a backgrounded test server takes the child PID.** A background
  shell launch is a bash wrapper plus a python child; killing the wrapper
  leaves the port bound. Find the real owner with `ss -tlnp | grep ':<port>'`
  and kill that PID. Never `pkill -f` the script name — the pattern also
  matches the shell running the command, which kills the caller.
