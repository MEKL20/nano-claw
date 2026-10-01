# KDP Tools (bundled scripts)

Companion scripts for the kdp-team pipeline, bundled in the skill's `scripts/`
dir and installed to `~/kdp/tools/`. **Always invoke them by install path**
(`python3 ~/kdp/tools/<script>.py`): a relative `scripts/...` path only
resolves with cwd set to the skill folder, which it never is during a run.
After adding a script here, copy it to `~/kdp/tools/` or every documented
command for it fails. stdlib + Pillow only: this host has no pandoc, no calibre, no
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
  type-forward.
- **Per-book text is inline around lines 45-79, not a constant block, and the
  title string appears TWICE** (`title_lines` for display, `fit("...")` for font
  sizing). Update both or the type is sized for the previous book's title. Full
  edit map in references/02-production.md.
- **Treat the installed file as a read-only template: copy it to
  `<project>/cover/cover_build.py` and edit there.** Editing `~/kdp/tools/cover_build.py` in place rewrites the
  generator every other book shares, makes finished covers unreproducible, and
  makes two concurrent books overwrite each other.
- Output paths come from the environment, never from edited literals:
  `KDP_COVER_OUT` (full path to cover.jpg; thumb and preview land beside it)
  and `KDP_FONT`. An older installed copy hardcoded
  `/home/mekl/kdp/book-001/cover/cover.jpg` — running that from another book
  would have overwritten book-001's finished cover.
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

    python3 ~/kdp/tools/verify_research.py <project>/research/decision.md --all
    python3 ~/kdp/tools/verify_research.py <decision.md> --sample 3 --json

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

It also prints a **DISTINCT BOOKS** section whenever one title appears under
several ASINs (Kindle / paperback / spiral share a review count), and re-runs
the demand and competition screen on distinct books. Row tallies overcount
rivals; the niche verdict must rest on the deduplicated numbers.

Cell formats accepted, because children legitimately write all of these:
`#45,120 in Books`, a bare `45,120` with the category in its own column,
`unranked`, and annotated honesty like `UNKNOWN (stars 4.9 shown, no count
rendered)`. Requiring the `#` once nulled every BSR in a table that split the
category out — while still printing a confident-looking report.

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

**Install exception: this one goes to `~/.hermes/scripts/`, NOT `~/kdp/tools/`.**
Cron resolves a job's `monitor_script` from that directory, so a copy anywhere
else is never executed. Honours `$KDP_ROOT` (default `~/kdp`) so it can be
tested against a fixture dir instead of live data.

Emits STABLE output (no timestamps, no day counters) for the monitor-gated
`kdp-live-detector` cron: one `SLUG|ASIN|live_date|review_due` line per LIVE
book. Unstable output makes the cron fire every tick.

**No live book = empty output = the sha256 of the empty string**
(`e3b0c442...b852b855`). That state is ambiguous by construction: "nothing is
live yet" and "the script is missing or broken" look identical in the stored
monitor hash. So never conclude the detector works from a quiet hash — prove
it with a fixture:

    KDP_ROOT=$(mktemp -d) # then write book-001/sales/log.csv with a real ASIN
    bash ~/.hermes/scripts/kdp_watch.sh

Verified 2026-10-01: a fixture ASIN yields
`book-001|B0ABCDEFGH|2026-10-01|2026-10-31`, whose hash differs from the quiet
state — so the detector does fire when MEKL enters an ASIN.
