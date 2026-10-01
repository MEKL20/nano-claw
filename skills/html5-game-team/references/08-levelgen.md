# Role brief: LEVEL GENERATION (parent-run, or a dedicated Build child)

Procedural level generation with a solver in the loop. Field-tested on
game-001 over 18 generator runs; every rule below cost at least one failed
run. Read this BEFORE editing a generator — the failure modes are not
obvious from the code.

## Deliverables
- `build/tools/gen-levels.js` — deterministic (seeded) generate-and-test:
  sample a board, solve it, measure difficulty, accept or reject. Writes
  each accepted level to disk immediately (partial persistence).
- `build/tools/check.js` — the gate. No args; walks every
  `levels/level-*.json`; prints numbered criteria then `ALL CHECKS PASSED`
  or `N FAILURES`. This is what the parent runs, not the generator's own log.
- `build/levels/level-NNN.json` — includes a `difficulty{}` block with the
  SOLVER-MEASURED metrics per level, not the targets that were requested.

## Architecture that worked
- **Tier ramp** as the single difficulty dial: `tier = floor((n - first)/2)`
  (MEKL's rule: harder every 2 levels). Targets derive from tier.
- **Bands** by grid size with a car-count window per band, plus a fill cap
  (`cars + blocks <= fillCap`) so boards never saturate.
- **Partial persistence**: write each level as it is accepted. A run that
  dies at level 82 keeps 11-81, and the next run skips them. This turns a
  3-hour failure into a 5-minute retry.
- **Timebox per acceptance rung** with a relax ladder: full target, then
  one step down, then an honest fallback that records the shortfall in the
  JSON. A generator that can hang is a generator that will hang.

## Rules (each one is a failed run)

1. **Never probe a single level to debug a chain failure.** A seeded run
   that skips levels 11-81 via persistence reaches level 82 with a
   different RNG state than the full run, so its samples differ. Six
   single-level drivers all reported a deterministic wall that the full run
   did not have. Reproduce in the full chain or you are debugging a ghost.
2. **Run the generator in the background, never foreground.** The terminal
   tool caps around 420s; a full chain is minutes to hours. Use
   `background=true, notify=true` and poll the log file.
3. **Instrument before adjusting.** When a level wall appears, log what the
   REJECTED candidates actually scored, not just the rejection counts. The
   game-001 wall looked like a metrics-too-high problem for 6 runs; the
   instrumented log showed candidates passing the metric gate and dying
   earlier, on a car-count window that had collapsed to a single value.
   Cap debug prints by level range, not by a global counter — a global cap
   of 3 prints spends itself on level 11 and tells you nothing about 82.
4. **Anticorrelated metrics need a combined bar.** At high density two
   independent minimums (`sw >= 8` AND `cb >= 6`) were jointly satisfiable
   in ~0.01% of samples because the metrics trade off against each other.
   Gate on the product (`sw * cb >= P`) plus a floor on each. Calibrate P
   from a census of what real samples score — not from the targets.
5. **Clamp targets the census proves unreachable, and say so.** A ramp that
   keeps climbing past the structural ceiling of the board size produces a
   hang, not a hard level. Clamp, log the clamp, and let the measured
   metrics in the JSON carry the honesty.
6. **Exact-N windows starve the sampler.** When the car-count window
   collapses to one value (`min == max`), every attempt must place exactly
   N cars under all placement constraints and essentially nothing reaches
   the metrics stage. Give the window slack — downward if the checker
   allows, upward only if it stays fill-safe.
7. **Never ratchet a window past its band.** Forbidding car-count dips while
   widening upward pushes one level past the band maximum, which forces the
   next level's floor above its own maximum, which poisons every level after
   it. Raw car count is a weak difficulty proxy; allow a small dip (and relax
   the checker's criterion in the SAME change) rather than ratcheting.
8. **Window-below-floor escape order**: drop a block first (restores the
   window on smaller grids), and only when blocks are exhausted raise the
   maximum fill-safely. Bare block-decrement alone burns every attempt with
   zero samples AND zero rejection keys — the stuck level then looks like
   nothing happened at all, which is the most expensive symptom to debug.
9. **Fix one bad level without re-rolling the chain.** Seed-sweep a driver
   that regenerates ONLY that level (child process per seed, restore the
   backup on each failure), and verify the chain constraints against its
   neighbours (optimal moves vs previous, par non-decreasing, dip within
   tolerance) before accepting. Re-running the whole chain to fix level 92
   re-rolls 93-100 for nothing.

## Verification (parent, not the child)
- `node tools/check.js` ends `ALL CHECKS PASSED`. A clean generator log is
  not a pass; the checker is the gate.
- Spot-check the ramp: read `difficulty{}` from the first, middle, and last
  generated level and confirm the metrics actually rise.
- Play-verify the last level in a real browser: load it, tap a car, confirm
  the exit fires and the HUD count drops. A level that solves in the solver
  can still be unreachable in the UI.
- Rebuild the ship archive after ANY level change (`python3` `zipfile`) and
  re-verify the level count inside the archive, not on disk.

## Never
- Never hand-edit a generated level file; fix the generator or seed-sweep.
- Never report a difficulty number you did not measure with the solver.
- Never leave probe/driver scripts in `tools/` — sweep them when done.
