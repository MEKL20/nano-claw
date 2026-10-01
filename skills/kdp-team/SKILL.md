---
name: kdp-team
version: 1.3.0
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
3. **MEKL owns risk calls.** He approves the niche pick, the final
   manuscript, and the price, and he performs the upload (his account, his
   KYC). The KDP AI-content question is answered "AI-generated text" on EVERY
   title — non-disclosure is the top account-suspension trigger (account-level
   enforcement since 2025); correct disclosure shows nowhere on the product
   page and carries no commercial penalty.
4. **Human gates are human-only.** The upload click and the live-ASIN entry
   are MEKL's actions. An agent writing an ASIN or a "published" flag
   fabricates a state nobody can later detect as false.
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
  seo/listing.md
  manuscript/chapters/chNN.md   one file per chapter (resumable)
  manuscript/book.epub
  manuscript/PROGRESS.md        chapter-by-chapter word counts
  cover/brief.md, cover.jpg, preview_400.png, thumb_100.png
  qa/report.md
  publish/package.md            field table + runbook section in ONE file
  sales/log.csv
```

Nothing else belongs there. `book.md` as a single monolith is NOT the layout —
chapters are separate files so a timeout costs one chapter, not the book.

## Cycle

One stage = one owner, one durable artifact, one exit gate the parent can
verify by running something.

| # | Stage | Owner | Artifact | Exit gate (parent runs it) | Board |
|---|---|---|---|---|---|
| 1 | Research | child | research/decision.md | >=10-row evidence table; parent re-fetches 3 sampled ASINs and diffs BSR/reviews | RESEARCHED |
| 2 | Niche gate | **MEKL** | approval in chat, logged in decision.md | explicit yes on niche + concept. No yes = no writing | RESEARCHED |
| 3 | SEO skeleton | child | seo/listing.md (TODO markers for TOC fields) | title + 7 keywords present, every char count computed with `len()` | WRITING |
| 4 | Production | child | manuscript/chapters/, cover/, book.epub | word count >=10,000 counted by parent; EPUB zipfile self-check; cover is 1600x2560 | PACKAGING |
| 5 | QA | child | qa/report.md | `## Verdict` + literal `**PASS**` (bold — the board greps it), zero BLOCKER/MAJOR, every check backed by evidence | IN QA |
| 6 | Fix loop | production/SEO fixes, fresh QA re-checks | updated files + report status | re-run ALL checks, not just the fixed one; fixer never re-checks | IN QA |
| 7 | SEO finalize | child | seo/listing.md complete | zero TODO markers; banned-term grep clean | IN QA |
| 8 | Publish package | child | publish/package.md (runbook is a section inside it) | MEKL can upload with no other file open; AI-disclosure step present; `·copy` suffixes on paste-able cells | READY TO UPLOAD |
| 9 | Final read | **MEKL** | his verdict | he has read the manuscript | READY TO UPLOAD |
| 10 | Upload | **MEKL** | ASIN entered in the dashboard | ~20 min, his account | LIVE |
| 11 | Analytics | parent | sales/log.csv, sales/review-30d.done | 30-day sequel/kill decision | LIVE |

After the niche gate (2), the chain runs autonomously to stage 8 — report
progress, do not ask permission for the next link. Stages 9-10 are MEKL's.

Any fix after stage 8 invalidates the package: re-run Publish, then re-verify.

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
- Market facts: Amazon.com, nonfiction how-to, 10-20k words, launch price
  $2.99-4.99 (70% royalty band), payout ~60 days after month end.
  **Upload cap: 2 new titles per FORMAT per week, reset Sundays 00:00 UTC**
  (tightened from 10 on 2026-09-21) — ebook/paperback/hardcover each have
  their own allowance.
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
`scripts/cover_build.py`, `scripts/kdp_dashboard.py`, `scripts/kdp_watch.sh`.

## Cost discipline

New book = full cycle. Trend scan only = research brief alone. Cover/format
fix = production + QA only, then re-run Publish because the package went
stale. Skip roles whose risk is absent — never skip parent verification, the
MEKL gates, or the AI disclosure.

Dispatch one child per stage, sequentially: each one's input is the previous
stage's artifact. Never two writers in the same directory.

## Analytics (parent role, no subagent)

30 days post-launch: parent reads KDP reports (MEKL pastes numbers or
screenshots), ranks titles by revenue, decides kill vs sequel per title. No ad
spend in v1. Add a marketing role only once a book earns.
