# KDP Tools (bundled scripts)

Companion scripts for the kdp-team pipeline, bundled in the skill's
`scripts/` dir. stdlib + Pillow only: this host has no pandoc, no calibre, no
epubcheck, no tesseract, no `zip` CLI, and `dpkg` is broken for new installs.
Install copies to `~/kdp/tools/` (where book-001 ran them from).

## scripts/epub_build.py — EPUB 3 builder (stdlib only)

    python3 epub_build.py --title "T" --author "A" --out book.epub \
        chapters/ch00_front.md chapters/ch01.md ... chapters/ch13_end.md

- Chapters are simple markdown (h1 title, paragraphs, h2/h3, ul/ol,
  `**bold**`, `*italic*`). Chapter title = the first `# ` line.
- Field-tested 2026-09-25: book-001 (14 chapter files, 16.7k words) built,
  passed the zipfile self-check, and passed the KDP previewer.
- Self-check after every build — do not trust the exit code alone:

      python3 -c "import zipfile; z=zipfile.ZipFile('book.epub'); assert z.read('mimetype')==b'application/epub+zip'; print('docs:', len([n for n in z.namelist() if n.endswith('.xhtml')]))"

## scripts/cover_build.py — eBook cover (Pillow)

- Output is **1600x2560 JPG** (`W, H = 1600, 2560` at the top of the file),
  type-forward. Edit the constants (palette, text, font path) per book.
- Fonts: DejaVu ships with the OS; `Montserrat.ttf` is already in
  `~/kdp/tools/` (variable TTF — `set_variation_by_name('Bold')` works).
- Acceptance checks are numeric, because this host has no vision model:
  margins (>=5% edges, nothing in the bottom 6% = 153px), zero text-block
  overlaps (`ImageDraw.textbbox` math), grayscale contrast (title band vs
  background), and 100px-thumbnail legibility by contrast numbers.
- Keep `cover/preview_400.png` and `cover/thumb_100.png` in the project so
  MEKL can eyeball the render himself.

## scripts/kdp_dashboard.py — publish console (stdlib http.server)

Token-gated LAN dashboard over the whole `~/kdp/` tree:

    python3 kdp_dashboard.py [--port 8791] [--root ~/kdp]

- First run mints `~/kdp/dashboard.token` (0600). URLs: `/<token>/` shelf,
  `/<token>/<slug>/` book detail, `/<token>/<slug>/publish` runbook,
  `/<token>/raw/<slug>/<relpath>` whitelisted download.
- Shelf status is DERIVED from the project tree, never set by hand: SETUP ->
  RESEARCHED (decision.md) -> WRITING (chapters exist) -> PACKAGING
  (book.epub) -> IN QA (qa/report.md) -> READY TO UPLOAD (QA verdict PASS +
  epub + cover) -> LIVE (ASIN != PENDING in sales/log.csv). New `book-NNN`
  dirs appear automatically.
- The set-asin form is MEKL's gate. Agents never write an ASIN.
- Download whitelist per book: book.epub, cover.jpg, preview_400.png,
  publish/package.md, seo/listing.md, cover/brief.md, qa/report.md.
  Everything else 404s (verified: cross-book fetch, `../../` traversal, and
  token-file fetch all 404).
- Deploy as a systemd `--user` service and enable linger so it survives
  logout/reboot. Plain HTTP: home LAN and tailnet only — never expose it
  publicly without TLS + auth.
- The token in `dashboard.token` is a capability URL. Never paste it anywhere.

## scripts/verify_research.py — parent's evidence verifier

The parent cannot accept a research child's table on its word. This re-fetches
sampled rows through the proxy and diffs them:

    python3 verify_research.py <project>/research/decision.md --all
    python3 verify_research.py <decision.md> --sample 3 --json

A decision table is a SNAPSHOT, so divergence alone is not dishonesty. The
verdicts separate time drift from numbers that cannot have come from a page:

| Verdict | Meaning | Fails? |
|---|---|---|
| MATCH | recorded == live | no |
| DRIFT | live >= recorded reviews: ordinary growth | no |
| REGRESSION | live materially BELOW recorded — counts do not shrink, so the recorded figure is unsupported | **yes, exit 1** |
| ZERO_VS_STARS | recorded 0 but page shows stars: ratings exist NOW, may have been true THEN | human judgment |
| UNVERIFIABLE | page rendered neither field (record UNKNOWN, not 0) | no |
| STUB | ~400-byte "continue shopping" — the ASIN is wrong, the proxy is fine | no |

BSR is printed but never fails a row: too volatile for single-sample evidence
(a low-ranked title moves an order of magnitude in a day).

Row extraction is driven off the TABLE HEADER (`bsr`/`rank`, `review`/`rating`,
`title` columns), not column position. Two holes this closed, both of which
made the tool print "0 failures" while covering only a subset:

- a row whose BSR cell said `UNKNOWN` — the very format the research brief
  mandates — had its review count skipped entirely;
- print books cited as `/dp/<ISBN>` instead of a `B0...` ASIN were skipped
  wholesale. In book-001 those were 5 of 18 rows and carried the table's
  LARGEST review counts (1,384 / 1,865 / 230 / 52 / 80), i.e. the rows where
  a fabricated number does the most damage. The proxy resolves print ISBNs
  fine (260-280KB per page).

Always read the printed `table rows: N   checked: M`. N > M means rows went
unverified, and an unverified row is where a bad number survives.

Field test 2026-10-01 on book-001: 18 rows parsed (13 under the old
positional parser), 0 REGRESSION anywhere. 6 MATCH, 4 DRIFT (e.g. 24->32 and
1,384->1,427 reviews over six days), 5 ZERO_VS_STARS (new titles that truly
had no ratings at research time), 3 UNVERIFIABLE. Conclusion: book-001's
evidence table contains no fabricated numbers.

## Strings the dashboard parses (change these and the board lies)

State is derived from files, so a brief that changes an artifact's wording
silently breaks the board. Verified against the script 2026-10-01:

- READY TO UPLOAD requires `qa/report.md` to contain BOTH `Verdict` and the
  literal `**PASS**` (bold), AND `manuscript/book.epub` AND `cover/cover.jpg`.
- The publish view renders `publish/package.md` only, labelled "PUBLISH
  RUNBOOK"; without that file the detail page reads "runbook not written
  yet". There is no `runbook.md` anywhere in the whitelist.
- Download whitelist: book.epub, cover.jpg, preview_400.png,
  publish/package.md, seo/listing.md, cover/brief.md, qa/report.md.
- A table cell ending in ` ·copy` renders as a copy-to-clipboard button with
  the suffix stripped. Use it on every value MEKL must paste.
- Book title is scraped from `**Title:**` in `seo/listing.md`.
- LIVE requires a non-PENDING ASIN in `sales/log.csv`, entered through the
  dashboard form by MEKL. No agent writes it.

## scripts/kdp_watch.sh — live-state monitor

Emits STABLE output (no timestamps, no day counters) for the monitor-gated
`kdp-live-detector` cron. Unstable output makes the cron fire every tick.
