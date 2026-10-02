# KDP Team Ops Runbook (parent/nano)

Field-tested 2026-09-25 on book-001; host facts re-verified 2026-10-01. Read
before dispatching children.

## End-to-end field test (2026-10-01, research stage)

One research child, dispatched against the revised brief, completed in 854s
and cleared the stage-1 gate on the first try: 13 rows, 11 BSRs, verifier
`13 checked / 12 MATCH / 0 REGRESSION`, exit 0. What made it work, in order of
how much each mattered:

1. **Pasting measured extraction patterns, not just the technique.** The child
   never had to reverse-engineer the page shape.
2. **The UNKNOWN rule stated with its consequence.** It wrote `UNKNOWN (4.9
   stars shown, count string not rendered)` — annotated honesty — instead of
   the zeros that would have corrupted the screen.
3. **Incremental writes.** `decision.md` existed on disk at 1.7KB mid-run, so a
   timeout would have cost rows, not the run.
4. **Naming book-001's niche as a hard exclusion.** No overlap to unwind.

What the child still got wrong, and the parent caught: row-based tallies that
counted multi-format editions as separate rivals (see "Count books, not listings" below), and a
summary tally that disagreed with its own table (it reported 11 of 13 BSRs
resolved and named the two gaps, while a third row recorded BSR UNKNOWN — the
cells were honest, the count was not). **Recompute every tally from the
artifact's cells; never copy a number out of the final message.** A brief that
produces verifiable work does not produce a sound conclusion by itself — the
parent's dedup and gate checks are not ceremony.

## Autonomous chain (default since 2026-10-01)

MEKL's standing order: no approvals, he receives finished work. On "go", run
stages 0-9 without asking — skeleton -> research -> niche decision -> SEO
skeleton -> production -> parent verify -> QA -> fix loop -> SEO finalize ->
publish package -> acceptance. Then hand him ONE message: the package is ready,
here is the runbook.

The only remaining human step is the upload itself (stage 10), because KDP has
no publishing API and the account is his. Never write an ASIN or a published
flag to fake it.

Every gate in that chain is a command, not a question. If a gate fails twice,
stop and report with evidence — the autonomy is in deciding, never in relaxing
a gate to keep the chain moving. Full stop conditions: SKILL.md "Decision
authority".

WIP limit 1: do not start a new book while a finished package waits for upload.
Queued packages pile onto the one human step and burn the 2-per-format weekly
cap without shipping.

## Stage 9: acceptance (parent only, replaces MEKL's read)

MEKL no longer reads the manuscript before upload, so this check is the last
thing standing between a child's output and his account. It is commands, not
impressions. Run from the project dir; write every result into
`qa/acceptance.md` with the command output quoted, then state ACCEPTED or
BLOCKED at the end.

```sh
cd ~/kdp/<slug>
# 1. AI/placeholder slop that must never reach a buyer
grep -rniE 'as an ai|language model|lorem ipsum|placeholder|TODO|TBD|\[insert|XXX' \
  manuscript/chapters/ seo/listing.md publish/package.md
# 2. size + packaging, by command
wc -w manuscript/chapters/*.md | tail -1
python3 -c "import zipfile;z=zipfile.ZipFile('manuscript/book.epub');assert z.read('mimetype')==b'application/epub+zip';print('xhtml:',len([n for n in z.namelist() if n.endswith('.xhtml')]))"
python3 -c "from PIL import Image;print(Image.open('cover/cover.jpg').size)"
# 3. title agreement across artifacts (a mismatch is a rejected upload)
grep -m1 'Title:' seo/listing.md; grep -m1 '^# ' manuscript/chapters/ch00_front.md
# 4. QA verdict is the bold literal the board greps
grep -c '\*\*PASS\*\*' qa/report.md
```

Then three judgment checks the parent performs by reading, not grepping:

- **Read ch01 and the final chapter end to end.** Openings and endings are
  where a degraded child's prose collapses, and the sample MEKL would have
  read. Note anything you would be embarrassed to publish.
- **Every listing description bullet traces to a real chapter.** Bullets
  promising content the book lacks are the top refund/1-star driver.
- **Disclaimer present where the niche needs one** (health, legal, financial
  adjacency). Absent = BLOCKED, not a MINOR note.

BLOCKED routes back through the normal fix loop (stage 6) and then re-runs
Publish, because any post-package fix staled the archive. Never accept with an
open BLOCKER to keep the chain moving.

Field-tested 2026-10-01 against book-001 (every command run, output real): slop
grep exits 1 with no matches, `16681 total` words, `xhtml: 15`,
`cover: (1600, 2560)`, listing `**Title:**` and `ch00_front.md`'s `# ` heading
identical, `**PASS**` count 1. Note grep's exit code is inverted here — exit 1
means CLEAN, exit 0 means slop was found, so never chain it with `&&`.

## Delegation gotchas (hard-won)

- **Children need the routing pinned**: `delegation.provider` must be
   `custom:9router` + `delegation.model` `sm/glm-5.3-flash`. Empty provider
   fields send children to external fallbacks (gc2/growthcircle) which 403
   instantly; the gateway's "switch to <model>" hint is boilerplate and its
   suggested model 403s too. Parent survives on 9router — pin children to the
   same path.
- **`child_timeout_seconds: 3600`** (config, verified 2026-10-01). The old
   600 killed a research run mid-flight with good evidence in context and
   nothing on disk.
- **Incremental writes are non-negotiable in every child brief**: "write
   files one at a time, never batch at the end; files survive, context may
   not." A timeout loses context but not files. Pass prior partial findings
   into the retry brief so nothing is re-derived.
- **Smoke test the pipe before long dispatches**: one `delegate_task` asking
   for a fixed reply string costs ~25s and proves model + route.
- **`web_search` (Firecrawl keyless) 403s intermittently** — children should
   retry/rephrase, not stall. Say so in the brief.
- **429 mid-run = resume, not restart**: upstream rate-limits under long
   generation load (hit at ch09 of 15 files, 2026-09-25). Files on disk
   survive. On retry: inventory the project dir first, then dispatch a resume
   brief listing exactly what exists (do-not-rewrite) and what remains, and
   tell the child to read the last written chapter to match voice.
- **Tiny fix tasks: parent executes directly.** A 3-patch fix dispatch died
   to 429 twice (2026-09-25); the parent doing the patches itself with `patch`
   + grep verification finished in one call. Mechanical edits under ~15
   minutes with deterministic verification go to the parent; dispatch only
   real reasoning work.
- **Fix briefs must inventory partial progress first.** Even the "failed"
   429 run had graded 2 of 5 fixes before dying — grep each finding's
   old/new text in the files before assigning fixes, or the child redoes or
   misses half-done items.
- **Cross-artifact consistency is a parent check too**: after fixes change
   facts (e.g. 3 -> 4 benchmarks), grep the listing description and cover
   brief for the old number. QA checks the book, not the listing against the
   fixed book.

- **Never infer a stage is incomplete from a missing filename.** Check the
    CONSUMER first. book-001 looked like it was missing `publish/runbook.md`;
    in fact the runbook is a section inside `package.md`, which is exactly
    what the dashboard renders and whitelists. Grep the tool that reads the
    artifact before concluding anything is absent — and before writing a
    brief that demands a file nobody will ever open.
- **Progress trackers go stale and become traps.** `PROGRESS.md` sat at
    "end of ch07 / Next: ch08" long after all 14 chapters landed; a resume
    brief trusting it would have rewritten finished work. Before any resume
    or fix dispatch, trust the file listing and `wc -w`, not the tracker.
    When correcting a stale pointer, DELETE it rather than quoting it — a
    blind child reading the quote can act on it.

- **A verifier that silently skips rows is worse than none.** It prints
    "0 failures" while covering a subset, which reads as a clean bill of
    health. `verify_research.py` once skipped rows whose BSR was UNKNOWN and
    every print book cited by ISBN rather than a B0 ASIN — 5 of 18 rows in
    book-001, holding its largest review counts. Drive extraction off the
    table header, and always compare `table rows: N` against `checked: M`.
- **Count books, not listings.** Amazon gives the Kindle, paperback, and
    spiral editions of one title separate ASINs that SHARE a review count, so
    row counts inflate every competition tally. book-002's 13 evidence rows
    were 9 distinct books: three editions of one cookbook read as three
    rivals. `verify_research.py` now prints a DISTINCT BOOKS section and
    re-runs the screen on it. A verifier that only checks per-row honesty
    still passes a table whose CONCLUSION is overcounted.
- **Test a checker against output a real child produced**, not against a
    sample you wrote. Watching a live run's partial `decision.md` showed BSRs
    written as bare `496,607` with the category in its own column; the
    verifier demanded a `#` and nulled all 10 of them, which would have
    failed the ">=6 BSRs resolved" gate on work that was correct. The brief
    and the checker must agree about format, and only real output proves it.

- **Check briefs PAIRWISE: each stage's INPUT spec must match the previous
    stage's OUTPUT spec.** Pre-flighting stage 3 before dispatching found that
    `02-production` read its outline from a "chapter plan" in `listing.md`
    that `03-seo` never told the child to write — book-001 only has one
    because that run improvised it. The same brief ordered the SKELETON
    dispatch to read `manuscript/chapters/*.md`, which cannot exist before
    the manuscript. Neither defect is visible reading one brief; both appear
    the moment you diff producer against consumer, or against a real artifact
    from a past run.
- **This list is deliberately UNNUMBERED — keep it that way.** It was numbered,
    and three separate inserts broke the sequence (a missing 13, then 15, then
    18) plus left a cross-reference pointing at the wrong rule. After the third
    time the fix stopped being "renumber more carefully" and became "remove the
    thing that breaks": an append-only list of lessons has no semantic order, so
    numbers are pure maintenance debt. Cross-reference a lesson by QUOTING ITS
    TITLE, never by index. Number only where position carries meaning — the
    cycle table's stages and a brief's procedure steps.

- **Diff the INSTALLED copy of a script against the bundled one.** Cron and
    the dashboard execute their own installed copies, so a skill can be
    perfectly up to date while the thing that actually runs is months old.
    `~/.hermes/scripts/kdp_watch.sh` still hardcoded an absolute KDP path long
    after the bundled version took `$KDP_ROOT` — which also meant a fixture
    test silently read live data and "passed" with empty output both times.
    After replacing an installed monitor, re-run it and confirm the output
    hash is UNCHANGED, or the swap itself fires a spurious alert.

- **A shared tool holding one project's constants is a cross-book hazard.**
    `cover_build.py` keeps palette and cover text as module-level constants, and
    the installed copy hardcoded book-001's OUTPUT path — so a second book's
    production child running it would have overwritten book-001's finished
    cover. Fix pattern: the installed script is a read-only template; each book
    copies it into `<project>/cover/` and edits the copy, with output paths from
    `KDP_COVER_OUT` / `KDP_FONT`. Verified 2026-10-01 by hashing book-001's
    cover before and after swapping the installed copy, then rendering to a
    temp dir.
- **"Safe HTML" without the whitelist is not a constraint.** The SEO brief said
    "KDP-safe HTML" and named no tags, so nothing stopped a child using `<h2>`
    or `<table>` — both silently stripped at upload, which is how a description
    lands as one mangled paragraph. Worse, KDP's 4,000-char limit COUNTS the
    markup, so a budget check on visible text passes copy that KDP rejects.
    Name the 12 allowed tags (`br p b em i u h4 h5 h6 ol ul li`), name the
    stripped ones, and measure the raw string. book-001 happened to get both
    right; nothing in the brief had required it.
- **A rendering defect is invisible to every source-level check.** Two QA rounds
    and every parent sweep read the markdown and passed it. The EPUB carried
    **338 literal `**` sequences across 137 list items** because `epub_build.py`
    applied inline bold in the paragraph path but returned early for `<li>` and
    headings. book-001, already READY TO UPLOAD, had 172 — visible asterisks in a
    reader, one click from publication. Grep the text of the BUILT artifact, not
    only the sources, and do it for every book the builder has ever touched.
- **Markdown markers hide defects from raw-string searches.** The parent called a
    QA finding unreproducible because `"in a oven"` appeared nowhere; the line
    actually reads `in a **oven`, which renders as the error. Strip inline markers
    (`\*\*|\*|`` ` ``|_`) before any prose sweep, and when a child cites a
    `file:line`, read that line RENDERED before declaring it phantom. QA was
    right and the parent was wrong — the sweep, not the finding, was broken.
- **Read metadata back out of the artifact you just built.** A rebuild wrote
    `dc:title` **"Untitled"** because the parent's regex looked for `| Title |`
    while `package.md` writes `| Book title |`. Exit code 0, valid EPUB, wrong
    book — on the title awaiting upload. Parse the OPF (`dc:title`, `dc:creator`)
    after every build; never let a build's exit code stand as verification.
- **A contradiction fixed in prose can survive in a table.** ch09's recipe
    stopped blanching alliums while the reference table in the SAME chapter still
    gave "Onion, leek | 2 min". Tables are a second home for every fact; after
    fixing prose, re-sweep rows for the same claim.
- **A locale sweep takes two passes and a protect list.** Fixing British
    spelling with exact-word pairs cleared 75 tokens and still missed six
    inflections (`flavoured`, `fibres`, `moulds`, `neighbouring`). A broad stem
    scan catches those — and immediately threatens correct US words that happen
    to contain the stem: `microorganisms` and `organisms` (8 occurrences) would
    have been destroyed by a careless `organis-` rule. So: pass 1 exact words,
    pass 2 stem scan, and an explicit protect list before any replacement.
    Verify by searching the REBUILT EPUB text, not the sources.
- **A fix that changes a chapter title stales two other artifacts.** The EPUB
    must be rebuilt and the listing's chapter plan re-aligned, or the TOC and the
    description promise a chapter the book no longer contains. After any title
    edit, diff plan entries against real chapter headings.
- **Never edit prose to satisfy a finding you cannot reproduce.** QA cited an
    article error at a specific `file:line`; the quoted string existed nowhere in
    the project and a sweep for that error class found nothing. Record it as
    unreproducible and pass it to the re-test. Rewriting correct prose to close a
    phantom finding is how a pipeline degrades a manuscript it was meant to
    protect.
- **An unverifiable attribution is the defect — drop the claim, keep the
    number** (when the number is not safety-critical). A blanch-time table was
    introduced as "the standard extension-service values per NCHFP"; three fetch
    attempts across two routes could not confirm those per-vegetable times.
    Citing an authority that may not say it is worse than stating the figures
    plainly, so the attribution went and the times stayed, with the uncertainty
    written into the text. For a SAFETY number the opposite holds: cut the
    instruction.
- **Never write into a project a child is actively reading.** The parent created
    `publish/ai-disclosure.md` while a QA child was mid-run, so that report
    carries both a BLOCKER (`publish/` was empty when checked) and a separate
    mid-run re-check row clearing it. The child behaved correctly — it recorded
    both rather than rewriting history — but the report is now harder to read and
    the finding count needs a footnote. Either create the artifact BEFORE
    dispatching, or wait and let the re-test see a clean tree. The same rule
    blocks cosmetic edits: a stale header is not worth muddying a verdict.
- **A gate may only check artifacts that exist at its own stage.** QA (stage 5)
    was told to confirm the AI-disclosure plan, which `publish/package.md`
    records at stage 8. Having nothing to verify, the child went looking and read
    ANOTHER BOOK's `START-HERE.md` — one step from a false PASS carried on a
    different title's artifact. Two fixes: the disclosure is now written at
    stage 0 into `publish/ai-disclosure.md` so it is checkable throughout, and
    every child brief states that a missing artifact is a FINDING, never a
    licence to search outside the project dir. When auditing a brief, ask of
    each check: does the file it names exist when this stage runs?
- **Re-verify every safety number the CHILD sourced itself, not just the ones
    you cached.** A brief that caches six USDA figures invites the child to
    research adjacent ones (pasteurisation, pre-treatment dips, shelf life) and
    those arrive with no parent check behind them. On book-002 all of them held
    up — UMN Extension confirmed 160°F/30min and 0°F/48h verbatim, and the
    ascorbic dip proved to be the canonical 2½ tbsp/quart re-expressed as 3¾ tsp
    per 2 cups (1.875 tsp/cup both ways) — but "held up" is a result, not an
    assumption. Write the evidence to `qa/safety-verification.md`, a parent-owned
    file: never into `qa/report.md`, which the QA child owns.
- **Unit equivalence can verify a number no page will serve you.** When every
    extension domain 403s, converting the book's figure into the canonical unit
    settles it by arithmetic. Prefer it to another fetch attempt.
- **For authority pages, expect `web_extract` to 403 and go straight to the
    reader proxy** (`curl -sL "https://r.jina.ai/<url>"`), which returned 12-15KB
    of clean text from Clemson and UMN Extension after five straight 403s. Find
    the page by SEARCH first — constructed NCHFP slugs 404'd.
- **Write structural gates against the artifact's real shape, not a slogan.**
    "Every chapter ends with takeaways" sounds complete and quietly indicts
    `ch00_front.md`, which is a title page plus copyright and disclaimer. A QA
    child reading that gate literally files a MAJOR, and the fix loop then adds
    filler to front matter to satisfy it. Name the exception in the gate itself.
- **A check that reports MISSING on correct content is worse than no check.**
    Three false alarms in one verification pass on book-002: a jerky row flagged
    because my criterion was "no meat row at all" when the row was
    self-qualifying ("after pre-treatment", drying temp only, pointing at the
    safety chapter); `130°F` reported MISSING because the prose correctly writes
    the range `130–140°F` with an en-dash; an authority reported uncited because
    the book spells out "National Center for Home Food Preservation" instead of
    the acronym I grepped. Each nearly triggered a "fix" to correct work, which
    is how a pipeline damages a good manuscript. So: match the form prose
    actually uses (ranges, en-dashes `–`, spelled-out names), and ALWAYS print
    the surrounding line with a finding so it can be falsified at a glance. An
    unfalsifiable MISSING trains you to ignore the checker.
- **Never SAMPLE a physical-harm check.** QA's fact check was "sample 10
    claims", which is right for general facts and wrong for anything a reader's
    safety rests on — the temperature the sample skips is the one that hurts
    someone. Safety numbers get enumerated by grep and checked one by one,
    including the two failure modes a sample almost never catches: a number
    that is correct for one food applied to another, and the same fact stated
    inconsistently across chapters.
- **Physical-harm claims are their own class, separate from "regulated
    advice".** The STOP list covered medical/legal/financial, which would have
    waved through a cookbook whose jerky chapter poisons someone. book-002's
    chapter plan said "160°F pre-cook" — correct for beef, and WRONG for the
    poultry and venison the same plan covers (165°F, and boiling for game).
    Cache verified authority numbers in the brief rather than letting a child
    recall them, and re-check each one at stage 9. A disclaimer transfers
    liability, never risk.
- **Label every constraint as PLATFORM or STRATEGY, and verify the platform
    ones against the vendor's own docs.** This skill carried "$2.99-4.99 (70%
    royalty band)" in five places. The real 70% band is $2.99-$12.99 (ceiling
    raised from $9.99 on 2026-07-07); $2.99-4.99 was our launch strategy wearing
    a platform constraint's clothes. Consequences were concrete: the QA gate
    would have flagged a correct $6.99 price as a finding, and an SEO child
    recommended $4.99 as "top of the band" — reasoning poisoned by the brief it
    was given. A strategy can be overridden on judgment; a platform rule cannot.
    Conflating them silently removes options (here, the post-review price raise
    that keeps 70%).
- **Check a rule's stated REASON against data before letting it block work.**
    A WIP limit here was justified as "parallel books burn the 2-per-format
    weekly cap" — but the cap is spent when MEKL creates a title in the KDP
    dashboard, not when the parent writes files locally, and book-001's title
    predated the open window anyway. The rule was right to exist and wrong in
    scope: it now blocks a second PACKAGE (stage 8), not a second book. A rule
    whose reason does not survive measurement will either be obeyed wrongly or
    quietly ignored.

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
  `python3 ~/kdp/tools/verify_research.py <project>/research/decision.md --all`.
  (Install path, not the skill dir — a relative `scripts/...` path only works
  with cwd set to the skill folder, which it never is mid-run.)
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
