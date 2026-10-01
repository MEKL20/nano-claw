# KDP Team Ops Runbook (parent/nano)

Field-tested 2026-09-25 on book-001; host facts re-verified 2026-10-01. Read
before dispatching children.

## Autonomous chain (default)

After MEKL approves niche + concept, run the pipeline without re-asking:
research -> SEO skeleton -> production -> parent verify -> QA -> fix loop ->
SEO finalize -> publish package. MEKL gates that remain: niche pick, final
manuscript read, upload click. Report progress, don't ask permission for the
next link in the chain.

## Delegation gotchas (hard-won)

1. **Children need the routing pinned**: `delegation.provider` must be
   `custom:9router` + `delegation.model` `sm/glm-5.3-flash`. Empty provider
   fields send children to external fallbacks (gc2/growthcircle) which 403
   instantly; the gateway's "switch to <model>" hint is boilerplate and its
   suggested model 403s too. Parent survives on 9router — pin children to the
   same path.
2. **`child_timeout_seconds: 3600`** (config, verified 2026-10-01). The old
   600 killed a research run mid-flight with good evidence in context and
   nothing on disk.
3. **Incremental writes are non-negotiable in every child brief**: "write
   files one at a time, never batch at the end; files survive, context may
   not." A timeout loses context but not files. Pass prior partial findings
   into the retry brief so nothing is re-derived.
4. **Smoke test the pipe before long dispatches**: one `delegate_task` asking
   for a fixed reply string costs ~25s and proves model + route.
5. **`web_search` (Firecrawl keyless) 403s intermittently** — children should
   retry/rephrase, not stall. Say so in the brief.
6. **429 mid-run = resume, not restart**: upstream rate-limits under long
   generation load (hit at ch09 of 15 files, 2026-09-25). Files on disk
   survive. On retry: inventory the project dir first, then dispatch a resume
   brief listing exactly what exists (do-not-rewrite) and what remains, and
   tell the child to read the last written chapter to match voice.
7. **Tiny fix tasks: parent executes directly.** A 3-patch fix dispatch died
   to 429 twice (2026-09-25); the parent doing the patches itself with `patch`
   + grep verification finished in one call. Mechanical edits under ~15
   minutes with deterministic verification go to the parent; dispatch only
   real reasoning work.
8. **Fix briefs must inventory partial progress first.** Even the "failed"
   429 run had graded 2 of 5 fixes before dying — grep each finding's
   old/new text in the files before assigning fixes, or the child redoes or
   misses half-done items.
9. **Cross-artifact consistency is a parent check too**: after fixes change
   facts (e.g. 3 -> 4 benchmarks), grep the listing description and cover
   brief for the old number. QA checks the book, not the listing against the
   fixed book.

10. **Never infer a stage is incomplete from a missing filename.** Check the
    CONSUMER first. book-001 looked like it was missing `publish/runbook.md`;
    in fact the runbook is a section inside `package.md`, which is exactly
    what the dashboard renders and whitelists. Grep the tool that reads the
    artifact before concluding anything is absent — and before writing a
    brief that demands a file nobody will ever open.
11. **Progress trackers go stale and become traps.** `PROGRESS.md` sat at
    "end of ch07 / Next: ch08" long after all 14 chapters landed; a resume
    brief trusting it would have rewritten finished work. Before any resume
    or fix dispatch, trust the file listing and `wc -w`, not the tracker.
    When correcting a stale pointer, DELETE it rather than quoting it — a
    blind child reading the quote can act on it.

12. **A verifier that silently skips rows is worse than none.** It prints
    "0 failures" while covering a subset, which reads as a clean bill of
    health. `verify_research.py` once skipped rows whose BSR was UNKNOWN and
    every print book cited by ISBN rather than a B0 ASIN — 5 of 18 rows in
    book-001, holding its largest review counts. Drive extraction off the
    table header, and always compare `table rows: N` against `checked: M`.
14. **Count books, not listings.** Amazon gives the Kindle, paperback, and
    spiral editions of one title separate ASINs that SHARE a review count, so
    row counts inflate every competition tally. book-002's 13 evidence rows
    were 9 distinct books: three editions of one cookbook read as three
    rivals. `verify_research.py` now prints a DISTINCT BOOKS section and
    re-runs the screen on it. A verifier that only checks per-row honesty
    still passes a table whose CONCLUSION is overcounted.
15. **Test a checker against output a real child produced**, not against a
    sample you wrote. Watching a live run's partial `decision.md` showed BSRs
    written as bare `496,607` with the category in its own column; the
    verifier demanded a `#` and nulled all 10 of them, which would have
    failed the ">=6 BSRs resolved" gate on work that was correct. The brief
    and the checker must agree about format, and only real output proves it.

## Proven techniques (reuse verbatim)

- **Amazon data via r.jina.ai** (keyless; re-verified 2026-10-01, returns
  ~200-260KB of markdown per product page):

      curl -sL --max-time 50 "https://r.jina.ai/https://www.amazon.com/dp/<ASIN>"

  Extraction patterns that actually match (6-ASIN sample):

      BSR      Best Sellers Rank:\s*#([\d,]+)\s+in\s+([^(\n\[]+)    4/6
      ratings  ([\d,]+)\s+global\s+ratings                          2/6
      stars    ([\d.]+)\s+out of 5 stars                            5/6
      title    ^Title:\s*(.+)$                                      4/4

  Strip a leading `Amazon.com: ` from the title. The first markdown heading
  is "Follow the author", never the book title.

  `(\d[\d,]*) ratings` matched 0/6 — it was wrong in the original brief.
  `#N in Kindle Store` misses titles ranked "in Books". Gaps are UNKNOWN,
  never 0: a star score with no count means the count did not render, and a
  refetch returns a byte-identical page, so retrying is wasted time.
  Google suggest works for autocomplete; Amazon's own API returns empty.
- **Probe with REAL data before declaring an outage.** A made-up ASIN returns
  HTTP 200 with a ~400-byte "continue shopping" stub, which reads exactly
  like a bot wall. Diagnosing the proxy as dead from that is a fabricated
  blocker — always probe with an ASIN cited in an existing decision.md.
- **Verification of child evidence**: run
  `python3 scripts/verify_research.py <project>/research/decision.md --all`.
  Exit 1 only on REGRESSION (a recorded count above the live one — impossible
  organically). DRIFT and UNVERIFIABLE are facts about Amazon, not faults in
  the child's work; judging drift as fabrication is a false accusation.
- **Builders, not packages**: EPUB via `scripts/epub_build.py`, cover via
  `scripts/cover_build.py`. No pandoc/calibre/epubcheck on this host and
  `dpkg` is broken for new installs — never apt-install for this pipeline.
- **EPUB self-check after every build** (don't trust exit code alone):

      python3 -c "import zipfile; z=zipfile.ZipFile('book.epub'); assert z.read('mimetype')==b'application/epub+zip'; print('docs:', len([n for n in z.namelist() if n.endswith('.xhtml')]))"

  book-001: 15 xhtml docs from 14 chapter files, mimetype OK.
- **Cover is 1600x2560 portrait** (W x H). Verify with PIL, not by eye:
  `python3 -c "from PIL import Image; print(Image.open('cover/cover.jpg').size)"`
  -> `(1600, 2560)`. A brief demanding 2560x1600 fails every correct cover.

## Agentic cycle (triggers 2+3)

ASIN is the switch: MEKL pastes it into the dashboard form
(`/<token>/<slug>/` set-asin) -> log.csv updated + `.tracking-armed` marker ->
status LIVE. An agent never writes an ASIN — that forges the human gate.
Cron jobs (created 2026-09-25, deliver to MEKL's Telegram, 09:00 WIB =
02:00 UTC):

- kdp-live-detector (daily, monitor-gated on `scripts/kdp_watch.sh`):
  announces a book going LIVE/UNLISTED only when the stable ASIN state
  changes.
- kdp-weekly-digest (Mondays 09:00 WIB, loads this skill): sales digest per
  live book, asks MEKL for numbers when stale, performs the 30-day
  SEQUEL/KILL review (writes `sales/review-30d.done` so it fires once).

Trigger 1 (new book) stays manual: MEKL says go -> full pipeline. Monitor
scripts must emit STABLE output (no timestamps or day counters) or
monitor-gated cron runs every tick.

## Run-state layout used by book-001

`manuscript/chapters/chNN.md` one file per chapter (resumable),
`manuscript/PROGRESS.md` carries per-chapter word counts, `seo/listing.md`
carries TODO markers until the manuscript exists, `sales/log.csv` pre-seeded
with `asin=PENDING`.
