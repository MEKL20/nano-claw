#!/usr/bin/env python3
"""Re-verify a KDP research decision table against live Amazon pages.

The parent cannot accept a research child's evidence table on its word. This
re-fetches sampled rows through the reader proxy and diffs the numbers.

    python3 verify_research.py <decision.md> [--sample 3] [--all] [--json]

A decision table is a SNAPSHOT. Review counts grow and BSR swings daily, so
divergence alone is not dishonesty - the verdicts below separate expected
drift from numbers that cannot have come from a real page.

Verdicts per row:
  MATCH          recorded numbers agree with the live page
  DRIFT          live >= recorded reviews: ordinary growth since the research
                 date. Informational, never a failure.
  REGRESSION     live reviews are materially BELOW the recorded figure.
                 Counts do not shrink organically, so the recorded number is
                 the suspect one. This is the real fabrication signal.
  ZERO_VS_STARS  recorded 0 while the page shows a star score. A star score
                 proves ratings exist, so 0 is wrong NOW - but if the book
                 earned its first rating after the research date, 0 was true
                 THEN. Needs human judgment; the honest cell is UNKNOWN.
  UNVERIFIABLE   the page rendered neither field (record UNKNOWN, not 0)
  STUB           proxy returned the ~400-byte "continue shopping" stub, which
                 means the ASIN is wrong, NOT that the proxy is down

BSR is reported but never fails a row: it is far too volatile (a low-ranked
title can move an order of magnitude in a day) to be evidence of anything
at single-sample resolution.

Exit 1 only on REGRESSION. Drift and render gaps are facts about Amazon, not
faults in the child's work.
"""
import argparse
import json
import random
import re
import subprocess
import sys

PROXY = "https://r.jina.ai/https://www.amazon.com/dp/{}"
RE_BSR = re.compile(r"Best Sellers Rank:\s*#([\d,]+)\s+in\s+([^(\n\[]+)", re.I)
RE_RATINGS = re.compile(r"([\d,]+)\s+global\s+ratings", re.I)
RE_STARS = re.compile(r"([\d.]+)\s+out of 5 stars", re.I)
RE_ASIN = re.compile(r"\b(B0[A-Z0-9]{8})\b")
RE_DP = re.compile(r"/dp/([A-Z0-9]{10})", re.I)
STUB_MARK = "continue shopping"


def num(s):
    return int(s.replace(",", "")) if s else None


def fetch(asin, timeout=55):
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", "50", PROXY.format(asin)],
            capture_output=True, text=True, timeout=timeout)
        return r.stdout
    except subprocess.TimeoutExpired:
        return ""


def cells_of(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_bsr(cell):
    """'#45,120 in Books' | '45,120' | 'unranked' | 'UNKNOWN' -> int|'unranked'|None

    A bare number must parse: tables legitimately put the rank in its own
    column with the category split out, and requiring the '#' nulled every
    BSR in such a table while still printing a confident-looking report.
    """
    c = cell.strip()
    if "unranked" in c.lower():
        return "unranked"
    hit = re.search(r"#\s*([\d,]+)", c) or re.fullmatch(r"([\d,]+)", c)
    return num(hit.group(1)) if hit else None


def read_reviews(cell):
    """Distinguish an absent count from a recorded zero - the whole point.

    UNKNOWN often arrives annotated ("UNKNOWN (stars 4.9 shown, no count
    rendered)"), which is the honest form the brief asks for, so match on the
    prefix rather than the exact word.
    """
    c = cell.strip()
    if c.upper().startswith(("UNKNOWN", "UNK", "N/A")):
        return "UNKNOWN"
    if c in ("", "-", "--", "\u2014", "?"):
        return None
    hit = re.fullmatch(r"([\d,]+)", c) or re.match(r"([\d,]+)\b", c)
    return num(hit.group(1)) if hit else None


def find_asin(line):
    """Prefer an explicit B0 ASIN; fall back to any /dp/<id> (print ISBNs)."""
    m = RE_ASIN.search(line)
    if m:
        return m.group(1)
    m = RE_DP.search(line)
    return m.group(1).upper() if m else None


def parse_rows(md):
    """Pull (asin, recorded_bsr, recorded_reviews) from the evidence table.

    Header-driven: a decision doc holds several tables (scorecards, keyword
    lists), and column order is not fixed. Guessing BSR/review columns by
    position silently skips rows whose BSR is UNKNOWN - and a skipped row is
    an unverified row, which is exactly what a fabricated number needs.
    """
    lines = md.splitlines()
    rows, seen = [], set()
    for i, line in enumerate(lines):
        if i + 1 >= len(lines) or not line.strip().startswith("|"):
            continue
        if not re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
            continue  # not a header (next line is not a separator)
        hdr = [h.lower() for h in cells_of(line)]
        bsr_i = next((j for j, h in enumerate(hdr) if "bsr" in h or "rank" in h), None)
        rev_i = next((j for j, h in enumerate(hdr)
                      if "review" in h or "rating" in h), None)
        ttl_i = next((j for j, h in enumerate(hdr) if "title" in h), None)
        if bsr_i is None and rev_i is None:
            continue  # scorecard or keyword table, not evidence
        for body in lines[i + 2:]:
            if not body.strip().startswith("|"):
                break
            c = cells_of(body)
            asin = find_asin(body)
            if not asin or asin in seen:
                continue
            seen.add(asin)
            rows.append({
                "asin": asin,
                "title": (c[ttl_i][:60] if ttl_i is not None and ttl_i < len(c) else ""),
                "rec_bsr": read_bsr(c[bsr_i]) if bsr_i is not None and bsr_i < len(c) else None,
                "rec_reviews": read_reviews(c[rev_i]) if rev_i is not None and rev_i < len(c) else None,
            })
    return rows


def verify(row):
    body = fetch(row["asin"])
    out = dict(row, live_bsr=None, live_cat=None, live_reviews=None,
               live_stars=None, bytes=len(body))
    if not body:
        out["verdict"] = "UNVERIFIABLE"
        out["note"] = "empty response (timeout)"
        return out
    if len(body) < 2000 and STUB_MARK in body.lower():
        out["verdict"] = "STUB"
        out["note"] = "ASIN likely wrong; proxy itself is fine"
        return out

    b = RE_BSR.search(body)
    if b:
        out["live_bsr"], out["live_cat"] = num(b.group(1)), b.group(2).strip()
    r = RE_RATINGS.search(body)
    if r:
        out["live_reviews"] = num(r.group(1))
    s = RE_STARS.search(body)
    if s:
        out["live_stars"] = float(s.group(1))

    rec, live = row["rec_reviews"], out["live_reviews"]

    # Recorded 0 while the page shows a star score. Ratings exist NOW; whether
    # they existed on the research date is unknowable from one sample, so this
    # is flagged for a human rather than scored as fabrication.
    if rec == 0 and live is None and out["live_stars"]:
        out["verdict"] = "ZERO_VS_STARS"
        out["note"] = (f"recorded 0 but page shows {out['live_stars']} stars: "
                       f"ratings exist now, so the honest cell is UNKNOWN")
        return out

    if isinstance(rec, int) and live is not None:
        if live == rec:
            out["verdict"] = "MATCH"
            out["note"] = ""
        elif live > rec:
            out["verdict"] = "DRIFT"
            out["note"] = f"reviews grew {rec} -> {live} since the research date"
        else:
            # Organic counts do not shrink. Allow a small margin for Amazon
            # purging a review or two, then treat it as the recorded number
            # being unsupported.
            if (rec - live) > max(2, 0.10 * rec):
                out["verdict"] = "REGRESSION"
                out["note"] = (f"recorded {rec} but live shows only {live}: "
                               f"counts do not shrink, so {rec} is unsupported")
            else:
                out["verdict"] = "DRIFT"
                out["note"] = f"reviews {rec} -> {live} (within purge margin)"
        return out

    if out["live_bsr"] is None and live is None:
        out["verdict"] = "UNVERIFIABLE"
        out["note"] = "page rendered neither BSR nor review count"
        return out

    out["verdict"] = "MATCH"
    out["note"] = ""
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decision")
    ap.add_argument("--sample", type=int, default=3)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()

    md = open(a.decision, encoding="utf-8").read()
    rows = parse_rows(md)
    if not rows:
        print("no evidence rows with an ASIN found", file=sys.stderr)
        return 2
    picked = rows if a.all else random.Random(a.seed).sample(
        rows, min(a.sample, len(rows)))

    results = [verify(r) for r in picked]
    bad = [r for r in results if r["verdict"] == "REGRESSION"]
    flagged = [r for r in results if r["verdict"] == "ZERO_VS_STARS"]
    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1

    if a.json:
        print(json.dumps({"rows_in_table": len(rows), "checked": len(results),
                          "regressions": len(bad), "zero_vs_stars": len(flagged),
                          "tally": tally, "results": results}, indent=2))
    else:
        print(f"table rows: {len(rows)}   checked: {len(results)}\n")
        for r in results:
            print(f"  {r['asin']}  {r['verdict']:14} "
                  f"rec_bsr={str(r['rec_bsr']):>10} live_bsr={str(r['live_bsr']):>10} "
                  f"rec_rev={str(r['rec_reviews']):>8} live_rev={str(r['live_reviews']):>6} "
                  f"stars={str(r['live_stars']):>4}")
            if r["note"]:
                print(f"      {r['note']}")
        print("\n  " + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())))
        print(f"\nregressions (fail): {len(bad)}")
        if flagged:
            print(f"zero-vs-stars (needs human judgment): {len(flagged)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
