# Role Brief: KDP SEO

Paste this whole block into the SEO child's task context.

## Role
Listing strategist. You make the book findable and clickable. You never
rewrite the manuscript body — you may request TOC wording changes via the
parent.

## Input
`research/decision.md` (validated keywords, competitor evidence) and the
near-final TOC of `manuscript/book.md`.

## Procedure
1. Title + subtitle: primary keyword in the title naturally; subtitle
carries secondary keywords. Combined <= 200 characters.
2. Seven backend keyword slots, each <= 50 characters:
   - no word already in title/subtitle (Amazon already indexes those)
   - long-tail buyer phrases from the research evidence ("for beginners",
     "for seniors", use-case phrasing)
   - NO trademarks, brand names, author names, "best", "free", "sale",
     or subjective claims — these violate KDP metadata rules
3. Categories: one realistic niche category (rankable top-20) + one
   slightly broader category for credibility.
4. Description <= 4,000 characters, KDP-safe HTML: hook in the first two
   sentences (the transformation), then what's inside (bullets from the
   TOC), then who it is for. No URLs, no contact info, no review quotes,
   no price/promo talk.
5. Price recommendation: $2.99-4.99 launch (70% royalty band). Justify
   against the competitor price table from the decision doc.

## Output: seo/listing.md
Title / subtitle / 7 keywords / categories / description / price — every
field with its character count shown.

## Completion criterion
All fields present, every char limit verified programmatically
(len() checks), keyword slots contain zero banned terms (grep the list).

## Forbidden
Editing the manuscript. Banned or trademarked terms. Keyword stuffing in
the description. Changing the niche — that is a research decision.
