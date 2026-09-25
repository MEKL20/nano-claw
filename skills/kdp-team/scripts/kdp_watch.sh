#!/bin/bash
# KDP live-book state: STABLE output unless a book gains/loses an ASIN
# Lines: "SLUG|ASIN|live_date|review_due"
KDP_ROOT="${KDP_ROOT:-$HOME/kdp}"
for log in "$KDP_ROOT"/book-*/sales/log.csv; do
  slug=$(echo "$log" | sed "s|$KDP_ROOT/||;s|/sales/log.csv||")
  tail -n +2 "$log" | while IFS=, read -r date sl asin price notes; do
    [ -z "$asin" ] && continue
    [ "$asin" = "PENDING" ] && continue
    [ -z "$date" ] && continue
    due=$(date -d "$date +30 days" +%Y-%m-%d 2>/dev/null)
    echo "$slug|$asin|$date|$due"
  done
done
