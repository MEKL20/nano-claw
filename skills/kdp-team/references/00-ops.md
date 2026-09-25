# KDP Team Ops Runbook (parent/nano)

Field-tested 2026-09-25 on book-001. Read before dispatching children.

## Autonomous chain (default)

After MEKL approves niche + concept, run the pipeline without re-asking:
research -> SEO skeleton -> production -> parent verify -> QA -> fix loop
-> SEO finalize -> publish package. MEKL gates that remain: niche pick,
final manuscript read, upload click. Report progress, don't ask permission
for the next link in the chain.

## Delegation gotchas (hard-won)

1. **Children need the routing pinned**: delegation.provider must be
   `custom:9router` + delegation.model `sm/glm-5.3-flash`. Empty provider
   fields send children to external fallbacks (gc2/growthcircle) which
   403 instantly; the gateway's "switch to <model>" hint is boilerplate
   and its suggested model 403s too. Parent survives on 9router — pin
   children to the same path. (2026-09-25)
2. **child_timeout_seconds: 1800** for production-size tasks. Default 600
   killed a research run mid-flight with good evidence in context and
   nothing on disk. Config changed 2026-09-25.
3. **Incremental writes are non-negotiable in every child brief**: "write
   files one at a time, never batch at the end; files survive, context
   may not." A timeout loses context but not files. Also: pass prior
   partial findings into the retry brief so nothing is re-derived.
4. **Smoke test the pipe before long dispatches**: one delegate_task
   asking for a fixed reply string costs ~25s and proves model+route.
5. **web_search (Firecrawl keyless) 403s intermittently** — children
   should retry/rephrase, not stall. Say so in the brief.
6. **429 mid-run = resume, not restart**: upstream glm-5.3-flash rate
   limits under long generation load (happened at ch09 of 15 files,
   2026-09-25). Files on disk survive. On retry: inventory the project
   dir first, then dispatch a resume brief that lists exactly what
   exists (do-not-rewrite) and what remains, and tells the child to
   read the last written chapter to match voice and continue.
7. **Tiny fix tasks: parent executes directly.** A 3-patch fix dispatch
   died to 429 twice (2026-09-25); parent doing the patches itself with
   `patch` + grep verification finished in one call. Rule: mechanical
   edits under ~15 minutes with deterministic verification go to the
   parent; dispatch only real reasoning work.
8. **Fix briefs must inventory partial progress first.** Even the
   "failed" 429 run had graded 2 of 5 fixes before dying — grep each
   finding's old/new text in the files before assigning fixes, or the
   child redoes/misses half-done items.
9. **Cross-artifact consistency is a parent check too**: after fixes
   change facts (e.g. 3 → 4 benchmarks), grep the listing description
   and cover brief for the old number — QA checks the book, not the
   listing against the fixed book.

## Proven techniques (reuse verbatim)

- **Amazon data via r.jina.ai**: `curl -sL --max-time 60
  "https://r.jina.ai/https://www.amazon.com/dp/ASIN" -o /tmp/x.txt` then
  regex `Best Sellers Rank` + `(\d[\d,]*) ratings` in execute_code.
  Category bestsellers: same proxy on /gp/bestsellers/digital-text/...
  Works on 2026-09-25. Amazon autocomplete API returns empty; use Google
  suggest (autocomplete) instead.
- **Verification of child evidence**: re-fetch 3 sampled ASINs with the
  same technique and diff BSR/reviews against the child's table.
- **EPUB without pandoc**: ~/kdp/tools/epub_build.py (stdlib zipfile;
  tested self-check). This machine's dpkg is broken for new installs
  (systemd configure errors) — don't apt-install anything for this
  pipeline. Cover: PIL 12 + DejaVu fonts are present.

## Run-state layout used by book-001

manuscript/chapters/chNN.md one file per chapter (resumable), listing.md
carries TODO markers until manuscript exists, sales/log.csv pre-seeded.
