---
name: kdp-team
version: 1.0.0
description: "Five-role KDP subagent team: research to publish pipeline."
---

# KDP Team: research - produce - seo - qa - publish

Subagent team for Amazon KDP self-publishing, run by nano (parent).
Children cannot load skills: nano pastes the matching reference brief from
this skill into each `delegate_task` task context. Every book run is one
project directory under `~/kdp/<slug>/`.

| Role | Brief | Does | Never does |
|---|---|---|---|
| Research | references/01-research.md | niche + trend validation, BSR/competition evidence, book decision | write, promise sales |
| Production | references/02-production.md | manuscript, cover, EPUB | self-certify, invent facts |
| SEO | references/03-seo.md | title/subtitle, 7 keywords, categories, description, price | rewrite manuscript body |
| QA | references/04-qa.md | guidelines, fact spot-check, EPUB + cover checks, verdict | fix anything |
| Publish | references/05-publish.md | upload package + MEKL upload runbook | touch credentials, automate dashboard |

Parent (nano): verify children, route fixes, run analytics, relay MEKL.
Autonomous mode: after MEKL approves niche, run the chain without
re-asking; gates stay (niche, final read, upload). Ops lessons,
delegation routing pins, and Amazon-scrape techniques live in
references/00-ops.md — read it before dispatching children.

## Non-negotiables

1. **Self-report is not evidence.** Parent re-verifies: word counts, EPUB
   validation, keyword char limits, sample facts. Nothing reaches MEKL on a
   child's word alone.
2. **Separation of duties.** QA never fixes; production never certifies
   its own work; whoever fixes never re-checks the fix.
3. **MEKL owns risk calls.** Approves: niche pick, final manuscript,
   price, and performs the upload (his account, his KYC). The KDP
   AI-content question is answered "AI-generated text" on EVERY title —
   non-disclosure is the top account-suspension trigger (account-level
   enforcement since 2025); correct disclosure shows nowhere on the
   product page and carries no commercial penalty.
4. **Escalation guards.** Same failure twice = stop, report with evidence.
   Scope change (new niche mid-book) = back to a fresh decision doc.
5. **Durable docs.** Every phase writes files into the project dir; chat
   only notifies.

## Project layout

```
~/kdp/<slug>/
  research/decision.md
  seo/listing.md
  manuscript/book.md, book.epub
  cover/brief.md, cover.jpg
  qa/report.md
  publish/package.md, runbook.md
  sales/log.csv
```

## Pipeline

Brief -> Research -> MEKL gates niche -> SEO skeleton (title + keywords
BEFORE writing; validated demand drives the book) -> Production -> QA
verdict loop until PASS -> SEO finalize -> MEKL final read -> Publish
package -> MEKL uploads manually (~20 min) -> log ASIN -> analytics.

Pacing and format: max 2 titles/week (Amazon upload cap per format).
Nonfiction how-to, 10-20k words, English (Amazon.com market), launch price
$2.99-4.99 (70% royalty band). Payout arrives ~60 days after month end.

## Cost discipline

New book = full pipeline. Trend scan only = research brief alone.
Cover/format fix = production + QA only. Skip roles whose risk is absent —
never skip parent verification, the MEKL gates, or the AI disclosure.

## Analytics (parent role, no subagent)

30 days post-launch: parent reads KDP reports (MEKL pastes numbers or
screenshots), ranks titles by revenue, decides kill vs sequel per title.
No ad spend in v1. Add a marketing role only once a book earns.
