# KDP Tools (scripts)

Companion scripts for the kdp-team pipeline. stdlib/PIL only — the target
machine's apt was broken for new installs (systemd packages), so no pandoc,
no calibre, no tesseract. Everything here runs on python3 stdlib (+Pillow
for the cover).

## scripts/epub_build.py — EPUB-3 builder (stdlib only)

    python3 epub_build.py --title "T" --author "A" --out book.epub ch00_front.md ch01.md ... ch13_end.md

- Chapters = simple markdown files (h1 title, paragraphs, h2/h3, ul/ol,
  **bold**, *italic*). Chapter title = first `# ` line.
- Field-tested 2026-09-25: book-001 (14 chapters, 16.7k words) built and
  passed zipfile self-check + KDP previewer.
- Self-check after build (run this, don't trust exit code alone):

      python3 -c "import zipfile; z=zipfile.ZipFile('book.epub'); assert z.read('mimetype')==b'application/epub+zip'; print('docs:', len([n for n in z.namelist() if n.endswith('.xhtml')]))"

## scripts/cover_build.py — eBook cover (Pillow)

- 1600x2560 JPG, type-forward. Edit constants at top (palette, text,
  font path) per book. Fonts: DejaVu ships with the OS; Montserrat
  variable TTF downloadable from google/fonts GitHub raw (set_variation
  by name 'Bold' works).
- Acceptance checks (grep/pixel level, no vision model needed):
  margins (>=5% edges, nothing in bottom 6%), zero text-block overlaps
  (audit with ImageDraw.textbbox math), grayscale contrast (title band
  min vs bg), 100px thumbnail legibility by contrast numbers.
- MEKL eyeballs the final render — keep a 400px preview PNG in the
  project cover/ dir.

## scripts/kdp_dashboard.py — publish console (stdlib http.server)

Token-gated LAN dashboard over the whole `~/kdp/` tree:

    python3 kdp_dashboard.py [--port 8791] [--root ~/kdp]

- First run mints `~/kdp/dashboard.token` (0600). URLs: /<token>/ shelf,
  /<token>/<slug>/ book detail, /<token>/<slug>/publish runbook,
  /<token>/raw/<slug>/<relpath> whitelisted download.
- Shelf status is DERIVED from the project tree (no manual config):
  SETUP -> RESEARCHED (decision.md) -> WRITING (chapters exist) ->
  PACKAGING (book.epub exists) -> IN QA (qa/report.md) -> READY TO
  UPLOAD (QA verdict PASS + epub + cover) -> LIVE (ASIN != PENDING in
  sales/log.csv). A new book-NNN directory appears automatically.
- Whitelist per book: book.epub, cover.jpg, preview_400.png,
  publish/package.md, seo/listing.md, cover/brief.md, qa/report.md.
  Everything else 404s (verified: cross-book fetch, traversal
  `../../`, token-file fetch all 404).
- Deploy as systemd --user service; enable linger so it survives
  logout/reboot. Plain HTTP: home LAN + tailnet only, never expose
  publicly without adding TLS+auth.
