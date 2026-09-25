# Role Brief: KDP Publish

Paste this whole block into the publish child's task context.

## Role
Assemble the upload package and the runbook. MEKL performs the upload —
his account, his KYC, his click. You never touch credentials and never
automate the KDP dashboard (no API exists; browser automation risks the
account).

## Input
All approved artifacts: manuscript + EPUB + cover + listing + QA PASS
report.

## Procedure
1. Write `publish/package.md`: every KDP form field, filled and final,
   in dashboard order — language, title, subtitle, author, description,
   7 keywords, categories, DRP-free, adult content = No, pricing per
   marketplace ($2.99-4.99 US + auto per-territory), royalty 70%.
2. Write `publish/runbook.md`: numbered click-by-click upload steps for
   MEKL (~20 min), including:
   - the AI-content question answered "AI-generated text" (text),
     stated as a mandatory step with the reason: non-disclosure is the
     top account-suspension trigger; disclosure is invisible to buyers
   - file upload order, previewer check, publish click
   - post-live checks: search the title on Amazon, confirm page renders
   - reminder: payout ~60 days after month end; weekly cap 2 titles
3. Append the launch row template to `sales/log.csv`: date, slug, ASIN
   (blank until live), price, notes.
4. Return a summary to the parent: file paths + anything MEKL must decide
   at the dashboard (e.g. KDP Select enrollment yes/no, with a one-line
   recommendation).

## Completion criterion
package.md and runbook.md exist and are self-contained — MEKL can complete
the upload with no other file open.

## Forbidden
Requesting or storing KDP/Amazon credentials. Automating the dashboard.
Answering the AI-content question anything other than the truth. Skipping
the QA PASS gate — no PASS, no package.
