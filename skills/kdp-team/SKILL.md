---
name: kdp-team
version: 1.11.0
description: "Five-role KDP subagent team: research to publish pipeline."
---

# KDP Team: research - produce - seo - qa - publish

Subagent team for Amazon KDP self-publishing, run by nano (parent). Children
cannot load skills or read memory: nano pastes the matching reference brief
from this skill into each `delegate_task` context. Every book run is one
project directory under `~/kdp/<slug>/`.

Skill dir: `~/.hermes/skills/productivity/kdp-team/` — paths below are
relative to it.

| Role | Brief | Does | Never does |
|---|---|---|---|
| Research | references/01-research.md | niche + trend validation, BSR/competition evidence, book decision | write, promise sales |
| Production | references/02-production.md | manuscript chapters, cover, EPUB | self-certify, invent facts |
| SEO | references/03-seo.md | title/subtitle, 7 keywords, categories, description, price | rewrite manuscript body |
| QA | references/04-qa.md | guidelines, fact spot-check, EPUB + cover checks, verdict | fix anything |
| Publish | references/05-publish.md | package.md: KDP field table + inlined click-by-click runbook | touch credentials, automate dashboard, split the runbook into its own file |

Parent (nano): verify children, route fixes, run analytics, relay MEKL.

## Context protocol (what a child knows: CAG + RAG)

Children start blind — no skills, no memory, no chat history, no ask-user
tool. Two channels, both owned by the parent.

**CAG — pasted verbatim into the brief, cached by the parent, never
re-derived by the child:**

1. the role brief from `references/`;
2. project dir path + exact files to READ and to WRITE;
3. the host facts this task touches (see below) — tool availability is
   settled knowledge here, not something to discover by trial;
4. hard constraints and forbidden actions;
5. the numbers that gate completion (word count floor, char limits, cover
   pixel dims).

**RAG — the child retrieves from disk when it needs it:**

- `research/decision.md` = the validated niche and keyword evidence;
- `seo/listing.md` = the title/keyword skeleton written BEFORE the manuscript;
- `manuscript/chapters/*.md` = the book as it exists (read the last written
   chapter to match voice before continuing);
- `qa/report.md` = known findings and their status.

Three rules keep retrieval honest:

- **Artifact outranks summary.** The file on disk beats prose about it,
  including the parent's.
- **Inventory before re-dispatch.** Before any fix or resume brief, grep what
  already exists and list done / not-done explicitly. Half-done work gets
  redone or silently skipped otherwise.
- **Write incrementally**, one chapter/file at a time, never batched at the
  end. Files survive a timeout; context does not.

## Non-negotiables

1. **Self-report is not evidence.** Parent re-verifies: word counts, EPUB
   validation, keyword char limits, cover pixel dims, sampled facts. Nothing
   reaches MEKL on a child's word alone.
2. **Separation of duties.** QA never fixes; production never certifies its
   own work; whoever fixes never re-checks the fix.
3. **The parent decides; MEKL receives finished work.** Niche, concept,
   title, keywords, price, fixes, and manuscript acceptance are the parent's
   calls on evidence (see Decision authority). The KDP AI-content question is
   still answered "AI-generated text" on EVERY title — that is compliance, not
   a preference: non-disclosure is the top account-suspension trigger
   (account-level enforcement since 2025), while correct disclosure shows
   nowhere on the product page and carries no commercial penalty.
4. **The upload gate is physical, and no agent may forge it.** KDP has no
   publishing API; the account and KYC are MEKL's; browser-automating the
   dashboard risks the account. So the upload click and the live-ASIN entry
   are his. An agent writing an ASIN or a "published" flag fabricates a state
   nobody can detect as false later — the one failure this pipeline cannot
   recover from.
5. **Escalation guards.** Same failure twice = stop, report with evidence.
   Scope change (new niche mid-book) = back to a fresh decision doc.
6. **Durable docs.** Every phase writes files into the project dir; chat only
   notifies.
7. **No invented numbers.** BSR, review counts, and sales figures are cited
   or absent. A plausible number in a decision doc is worse than a gap,
   because the next stage builds on it.

## Project layout

```
~/kdp/<slug>/
  research/decision.md
  research/*.json               fetch provenance (raw scraped rows, ASIN pools)
  seo/listing.md
  manuscript/chapters/chNN.md   one file per chapter (resumable)
  manuscript/book.epub
  manuscript/PROGRESS.md        chapter-by-chapter word counts
  cover/brief.md, cover.jpg, preview_400.png, thumb_100.png
  qa/report.md
  qa/acceptance.md              parent's stage-9 sign-off (replaces a human read)
  publish/package.md            field table + runbook section in ONE file
  sales/log.csv
```

`book.md` as a single monolith is NOT the layout — chapters are separate files
so a timeout costs one chapter, not the book.

**Stage 0, parent creates the skeleton before dispatching anyone** (one call,
so no child invents its own layout):

```sh
SLUG=book-00N
mkdir -p ~/kdp/$SLUG/{research,seo,manuscript/chapters,cover,qa,publish,sales}
printf 'date,slug,asin,price,notes\n' > ~/kdp/$SLUG/sales/log.csv
```

Seed `log.csv` with the HEADER ONLY. The weekly-digest cron reads
`sales/log.csv` for every `book-*` dir it finds, so a missing file forces that
job to guess about a book that is simply pre-launch. The launch row is
Publish's job (stage 8) — writing one earlier means inventing a slug and price
before stage 2 has decided them.

After touching anything the board or a monitor reads, re-run
`bash ~/.hermes/scripts/kdp_watch.sh` and confirm the output hash is unchanged;
otherwise the edit itself pages MEKL at 09:00 WIB.

Sweep stray files before declaring a phase done, but **provenance is not
litter**: a research child's raw scrape dumps under `research/*.json` let the
parent re-check numbers without ~13 fresh proxy fetches, and they are the only
record of candidates that were screened and rejected. Keep them. Delete probe
scripts, nested `<slug>/<slug>/` dirs, and editor backups.

## Cycle

One stage = one owner, one durable artifact, one exit gate the parent can
verify by running something.

| # | Stage | Owner | Artifact | Exit gate (parent runs it) | Board |
|---|---|---|---|---|---|
| 0 | Skeleton | parent | project dirs + `sales/log.csv` header | dirs exist, log.csv has a header and zero data rows, monitor hash unchanged | SETUP |
| 1 | Research | child | research/decision.md | >=10 rows, >=6 real BSRs; `python3 ~/kdp/tools/verify_research.py <dir>/research/decision.md --all` exits 0, and the DISTINCT BOOKS screen still passes | RESEARCHED |
| 2 | Niche decision | parent | verdict appended to decision.md (niche + concept + why) | verifier exits 0; >=3 DISTINCT books under 300k BSR; competition SCREENED, or UNSCREENED stated as a risk; no overlap with an existing `book-*`; not fiction or generic self-help | RESEARCHED |
| 3 | SEO skeleton | child | seo/listing.md (TODO markers for TOC fields) | title + 7 keywords present, every char count computed with `len()` | WRITING |
| 4 | Production | child | manuscript/chapters/, cover/, book.epub | word count >=10,000 counted by parent; EPUB zipfile self-check; cover is 1600x2560 | PACKAGING |
| 5 | QA | child | qa/report.md | `## Verdict` + literal `**PASS**` (bold — the board greps it), zero BLOCKER/MAJOR, every check backed by evidence | IN QA |
| 6 | Fix loop | production/SEO fixes, fresh QA re-checks | updated files + report status | re-run ALL checks, not just the fixed one; fixer never re-checks | IN QA |
| 7 | SEO finalize | child | seo/listing.md complete | zero TODO markers; banned-term grep clean | IN QA |
| 8 | Publish package | child | publish/package.md (runbook is a section inside it) | MEKL can upload with no other file open; AI-disclosure step present; `·copy` suffixes on paste-able cells | READY TO UPLOAD |
| 9 | Acceptance | parent | `qa/acceptance.md` | parent read ch01 + final chapter end-to-end; grep clean for TODO/lorem/placeholder/"as an AI"; listing bullets trace to real chapters; disclaimers present where the niche needs them; EPUB + cover re-checked by command | READY TO UPLOAD |
| 10 | Upload | **MEKL** | ASIN entered in the dashboard | the one human step: ~20 min, his account, no API exists | LIVE |
| 11 | Analytics | parent | sales/log.csv, sales/review-30d.done | 30-day sequel/kill decision | LIVE |

Stages 0-9 run end to end without asking: each gate is a command the parent
runs, not a message it sends. Stage 10 is MEKL's single click.

Any fix after stage 8 invalidates the package: re-run Publish, then re-verify.

## Decision authority (MEKL's standing order, 2026-10-01)

"Ga perlu approval dari gw, gw tinggal terima hasil jadi aja." The parent
therefore decides and reports afterwards: niche and concept, title/subtitle/
keywords/categories, launch price (strategy band $2.99-4.99; platform 70% band
is $2.99-$12.99), KDP
Select enrolment, every fix routing call and scope cut, manuscript acceptance,
and the 30-day sequel/kill verdict.

**Notify, don't ask.** Progress messages are statements. The only message that
requests anything is "package ready — runbook here", and the only question
worth sending is one whose answer no artifact can supply.

### STOP and report instead of deciding when

1. **A gate fails twice** — verifier REGRESSION, the same QA finding surviving
   a fix, a generator wall. Report with evidence; never lower a gate to let
   the chain continue. A gate the parent can relax is not a gate.
2. **The demand screen fails on distinct books** — report the 3 finalists with
   their data instead of forcing a winner to keep moving.
3. **The niche needs a regulated claim** (medical, legal, financial advice)
   that a disclaimer cannot honestly cover — or a PHYSICAL-HARM instruction
   (food safety temperatures, dosages, tool limits) that no named authority
   confirms. A disclaimer transfers liability, not risk: if the number cannot
   be sourced, the instruction gets cut, and if the book cannot exist without
   it, the niche is wrong.
4. **A decision would spend money, touch account credentials, or write outside
   `~/kdp/`.**
5. **Stage 8 would build a SECOND package while one still awaits upload.**
   Hold at stage 7 and report; do not stop earlier stages. Local work spends no
   KDP capacity — the 2-per-format weekly cap is consumed when MEKL CREATES the
   title in the dashboard, not when the parent writes files — so research,
   writing, and QA may proceed on the next book. What packaging early does cost
   is freshness: any later fix invalidates the archive, and every queued
   package is another ~20 minutes of MEKL's time.

## Fix loops (who fixes what)

- QA BLOCKER/MAJOR on content -> **Production** fixes -> fresh QA re-runs all
  checks. QA never fixes.
- QA finding on the listing -> **SEO** fixes -> fresh QA re-checks char limits
  and banned terms.
- Mechanical edits under ~15 min with deterministic verification: the
  **parent** does them directly with `patch` + grep. Dispatch costs more than
  the work and dies to rate limits on short tasks.
- Cross-artifact drift is a parent check: when a fix changes a fact (3 -> 4
  benchmarks), grep the listing description and cover brief for the old value.
  QA checks the book, not the listing against the fixed book.
- Same failure twice -> stop, report with evidence.

## Host facts (cached — paste what the task touches)

- **No `pandoc`, no `epubcheck`, no `calibre`, no `zip` CLI, no
  `tesseract`.** `dpkg` is broken for new installs — nothing gets
  apt-installed for this pipeline. `unzip` exists for verification.
- EPUB is built by `scripts/epub_build.py` (stdlib `zipfile`), cover by
  `scripts/cover_build.py` (Pillow). Both field-tested; details in
  references/06-tools.md. Install copies to `~/kdp/tools/`.
- PIL/Pillow present. DejaVu fonts ship with the OS; `~/kdp/tools/
  Montserrat.ttf` is already downloaded.
- **No vision model on this host.** Never ask anyone to look at an image.
  Cover legibility is proven with numbers: pixel dims, margin math,
  grayscale contrast, a 100px thumbnail rendered and measured.
- Market facts: Amazon.com, nonfiction how-to, 10-20k words, payout ~60 days
  after month end.
- **Royalty band (platform constraint, verified at kdp.amazon.com 2026-10-01):**
  70% royalty requires a list price of **$2.99-$12.99** — the ceiling rose from
  $9.99 on 2026-07-07. 35% applies outside that range, and 70% carries an
  average $0.06/unit delivery cost.
- **Launch band $2.99-4.99 is OUR STRATEGY, not the platform's limit** — a
  deliberate choice for a zero-review title, not a rule. Because the band
  actually reaches $12.99, raising price after reviews accumulate keeps the 70%
  rate; plan that as the normal path rather than treating $4.99 as a ceiling.
  **Upload cap: 2 new titles per FORMAT per week, reset Sundays 00:00 UTC**
  (tightened from 10 on 2026-09-21) — ebook/paperback/hardcover each have
  their own allowance. The cap is spent at TITLE CREATION in the dashboard, so
  pipeline work on this machine never consumes it; check the window against the
  `date` column in each `sales/log.csv`, not against local file mtimes.
- Delegation routing, timeouts, and the resume protocol: references/00-ops.md.
  Read it before every dispatch.

## Reference index

| Reference | Pasted into | Parent-only |
|---|---|---|
| 00-ops.md | nobody — parent reads before EVERY dispatch | yes |
| 01-research.md | Research child | |
| 02-production.md | Production child | |
| 03-seo.md | SEO child (both dispatches) | |
| 04-qa.md | QA child | |
| 05-publish.md | Publish child | |
| 06-tools.md | whoever runs the builders (often the parent) | |

Bundled so the pipeline needs nothing external: `scripts/epub_build.py`,
`scripts/cover_build.py`, `scripts/kdp_dashboard.py`, `scripts/kdp_watch.sh`,
`scripts/verify_research.py` (parent's evidence verifier — run it on every
research table before accepting the niche).

## Cost discipline

New book = full cycle. Trend scan only = research brief alone. Cover/format
fix = production + QA only, then re-run Publish because the package went
stale. Skip roles whose risk is absent — never skip parent verification, the
upload gate, or the AI disclosure.

Dispatch one child per stage, sequentially: each one's input is the previous
stage's artifact. Never two writers in the same directory.

## Analytics (parent role, no subagent)

30 days post-launch: parent reads KDP reports (MEKL pastes numbers or
screenshots), ranks titles by revenue, decides kill vs sequel per title. No ad
spend in v1. Add a marketing role only once a book earns.
