# KDP Team

A five-role Amazon KDP publishing pipeline, shipped as installable agent skills.
Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent), portable
to any agent framework with a spawn/delegate primitive. On the reference host
each role is a persistent Hermes profile (`kdp-{research,production,seo,qa,publish}`)
dispatched through the kanban board; `roles/<profile>/SOUL.md` is the role
profiling — identity plus absolute gates — and its portable backup.

Research a niche, write the book, build the cover and EPUB, QA it, and hand the
human a finished package. Every rule here was learned by running the pipeline,
not by planning it.

## Roles

| Role | Profile | Does | Never does |
|---|---|---|---|
| Research | kdp-research | niche screening, competitor evidence, demand/competition verdict | pick the niche alone |
| SEO | kdp-seo | title, subtitle, 7 keywords, categories, chapter plan, description | edit the manuscript |
| Production | kdp-production | chapters, front matter, cover, EPUB | certify its own output |
| QA | kdp-qa | evidence-first testing, verdict that gates publish | fix anything |
| Publish | kdp-publish | the KDP field package + click-by-click runbook | write an ASIN or a "published" flag |
| Parent | nano (orchestrator) | decides, verifies, routes fixes, runs mechanical work | delegate verification |

## The cycle

12 stages (0-11): skeleton, research, niche decision, SEO skeleton, production,
QA, fix loop, SEO finalize, package, acceptance, **upload (human)**, tracking.

**One human gate: the upload itself.** KDP has no publishing API, the account and
KYC belong to the human, and browser-automating the KDP dashboard is the top
suspension risk. Everything before it is autonomous; the human receives a
finished package and spends ~20 minutes pasting fields.

No agent may write an ASIN or mark a book published. An agent that fabricates
that flag fabricates a fact nobody can detect as false later.

## Non-negotiables

1. **Self-report is not evidence.** Recompute every number a child reports from
   its own cells. Children miscount in a consistent direction: favourably.
2. **The producer never certifies.** QA does not fix. The parent may run
   mechanical fixes, but then a fresh QA round re-tests *every* check.
3. **Physical-harm claims are never sampled.** For food, medical, dosage or
   tool-limit content, enumerate every safety number exhaustively and cite a
   named authority. The temperature you skip is the one that hurts a reader.
4. **Grep the built artifact, not only the sources.** A rendering bug passes
   every source-level check, and a builder bug is retroactive across every
   artifact it ever produced.
5. **Label each constraint PLATFORM or STRATEGY.** The 70% royalty band is
   $2.99-$12.99; "$2.99-4.99 for a zero-review launch" is strategy. Conflating
   them makes a child reason from a false premise.
6. **Context dies, files survive.** Children write incrementally; resume briefs
   inventory partial progress first.

## Context protocol (SOUL + CAG + RAG)

Workers start every task without conversation context: no chat history, no
parent memory, no ask-user tool. **SOUL** travels with the profile (identity,
hard rules, absolute gates) and pins the role brief's live path — the worker
reads its own brief first. **CAG** is the kanban task body the parent writes:
project dir, exact files to read/write, cached host facts, constraints, the
numbers that gate completion. **RAG** is what the worker retrieves from disk
(`research/decision.md`, `seo/listing.md`, `manuscript/chapters/*.md`).
Anything missing from the task body does not exist for the worker. Frameworks
without persistent profiles: paste brief + gates verbatim instead (the
delegate fallback in references/00-ops.md).

## What's inside

```
SKILL.md                 router + cycle + decision authority (start here)
references/00-ops.md     parent-only runbook: routing, failure table, lessons
references/01-research.md niche screening, proxy technique, distinct-book counting
references/02-production.md chapter writing, cached safety facts, cover template
references/03-seo.md     listing rules, KDP's 12-tag description allowlist
references/04-qa.md      check list, verdict format the dashboard greps
references/05-publish.md package + runbook contract
references/06-tools.md   bundled script docs and install paths
scripts/                 epub_build, cover_build, kdp_dashboard, kdp_watch,
                         verify_research
roles/<profile>/SOUL.md  role profiling (identity + absolute gates), one per
                         Hermes profile; portable backup of the live SOULs
```

## Install (Hermes)

```bash
REPO=https://raw.githubusercontent.com/MEKL20/nano-claw/main/skills/kdp-team
SKILL=~/.hermes/skills/productivity/kdp-team

mkdir -p $SKILL/references $SKILL/scripts
curl -sL $REPO/SKILL.md -o $SKILL/SKILL.md
for r in 00-ops 01-research 02-production 03-seo 04-qa 05-publish 06-tools; do
  curl -sL $REPO/references/$r.md -o $SKILL/references/$r.md
done
for s in epub_build.py cover_build.py kdp_dashboard.py verify_research.py kdp_watch.sh; do
  curl -sL $REPO/scripts/$s -o $SKILL/scripts/$s
done
for r in kdp-research kdp-production kdp-seo kdp-qa kdp-publish; do
  mkdir -p $SKILL/roles/$r
  curl -sL $REPO/roles/$r/SOUL.md -o $SKILL/roles/$r/SOUL.md
done

# Tools run from ~/kdp/tools/, NOT from the skill dir: the briefs and the cron
# job both resolve them there, and a relative scripts/ path only works when the
# parent happens to be sitting in the skill directory.
mkdir -p ~/kdp/tools
for s in epub_build.py cover_build.py kdp_dashboard.py verify_research.py; do
  cp $SKILL/scripts/$s ~/kdp/tools/$s
done

# Exception: the live-book detector is resolved from ~/.hermes/scripts/ by cron.
mkdir -p ~/.hermes/scripts
cp $SKILL/scripts/kdp_watch.sh ~/.hermes/scripts/kdp_watch.sh
chmod +x ~/.hermes/scripts/kdp_watch.sh
```

### Profiles (Hermes — canonical dispatch on the reference host)

```bash
for r in kdp-research kdp-production kdp-seo kdp-qa kdp-publish; do
  hermes profile create $r --description "kdp-team role: ${r#kdp-}"
  cp $SKILL/roles/$r/SOUL.md ~/.hermes/profiles/$r/SOUL.md
done
```

Copy `providers` + `fallback_providers` from the parent `~/.hermes/config.yaml`
into each profile's config.yaml — children without them fail with "Unknown
provider". Dispatch through a per-book kanban board; the full recipe lives in
SKILL.md §Role profiles & kanban dispatch.

### Dashboard (optional, LAN-only)

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(24))" > ~/kdp/dashboard.token
chmod 600 ~/kdp/dashboard.token
python3 ~/kdp/tools/kdp_dashboard.py --port 8791   # read-only file browser over ~/kdp
```

It serves a URL-token path and binds locally. There is no login: treat the token
as the credential, keep it off the public internet, and do not expose the port.

### Per-book skeleton (stage 0, parent does this)

```bash
SLUG=book-001
mkdir -p ~/kdp/$SLUG/{research,seo,manuscript/chapters,cover,qa,publish,sales}
printf 'date,slug,asin,price,notes\n' > ~/kdp/$SLUG/sales/log.csv
```

Also write `publish/ai-disclosure.md` at stage 0 answering **AI-generated text**
— QA checks it at stage 5, long before the package exists. Non-disclosure is an
account-level suspension trigger; correct disclosure appears nowhere on the
product page and costs nothing.

## Host assumptions

Written for a host with python3 + Pillow and **no** pandoc, epubcheck, calibre,
tesseract, `zip`, or vision model. The EPUB builder is stdlib-only and every
visual check is a computed number (PIL sizes, WCAG contrast arithmetic) rather
than an opinion about an image. On a richer host these still work; they are
floors, not ceilings.

## Install (other agents)

Any framework with (a) spawned sub-conversations, (b) file read access for
children, and (c) a human channel for the upload relay. Paste each role brief
from `references/` as the child's task preamble. The stage contracts — one
owner, one artifact, one exit gate — are framework-agnostic.

## License

MIT.
