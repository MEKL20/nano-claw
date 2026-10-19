# BUGFIX-SPEC: <judul bug>

> Model Kiro: identifikasi root cause, apa yang harus BERUBAH, dan eksplisit apa
> yang TIDAK boleh berubah. Untuk bug kritis/regresi mahal/root cause tak jelas.
> Trivial (typo, one-liner) = quick fix, tidak butuh spec.

## Reproduction steps
<kondisi persis pemicu bug + bukti (log/screenshot/perilaku)>

## 1. Current Behavior (defect)
- WHEN <kondisi> THEN the system <perilaku salah>

## 2. Expected Behavior (correct)
- WHEN <kondisi> THEN the system SHALL <perilaku benar>

## 3. Unchanged Behavior (regression prevention — WAJIB)
> Panen dari: invariant STATE.md + smoke suite yang ada + perilaku sekitar bug.
- WHEN <kondisi> THEN the system SHALL CONTINUE TO <perilaku existing>

## 4. Root Cause (design phase)
<analisis berbasis bukti (baca kode/log, ukur — jangan duga). File:baris penyebab.>

## 5. Fix Approach & Constraints
<pendekatan fix minimal; file/kode yang TIDAK boleh disentuh>

## 6. Regression Checks (task implementasi wajib membuktikan ketiganya)
- [ ] repro test: bug ter-reproduce SEBELUM fix (merah)
- [ ] fix test: perilaku benar SESUDAH fix (hijau)
- [ ] unchanged: semua SHALL-CONTINUE-TO §3 tetap hijau (smoke existing + tambahan baru)
