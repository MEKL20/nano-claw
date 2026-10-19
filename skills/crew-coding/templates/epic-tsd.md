# EPIC-TSD: <nama epic> v<N>

> Deliverable lead. Derived dari PRD §x / FEATURE-SPEC-y (+ SDD bila ada).
> Satu unit = satu task kanban. Kata vague dilarang; semua terukur.

## 0. Analyze-Requirements Pass (WAJIB sebelum unit breakdown)
> Reasoning LINTAS requirement set, bukan per-requirement.
| # | Finding | Tipe | Keputusan final |
|---|---|---|---|
| 1 | <inkonsistensi/ambiguitas/konflik FR-NFR/asumsi tak tertulis/edge case bolong> | <tipe> | keputusan final: <keputusan + alasan> |

## 1. Technical Context
<stack fit, modul terdampak, kondisi repo saat ini (kerja in-progress yang harus
didahulukan — sequencing)>

## 2. Unit Breakdown (ordered)
### Unit 1: <nama>
- Cakupan file: <persis>
- Sumber: PRD §x / FEATURE-SPEC §y (uncitable = scope creep, jangan dibuat)
- AC (EARS): WHEN… THE SYSTEM SHALL…
- Verify: <command: cargo test / npm run build / smoke>
- Demo: <SATU baris bukti observable selesai — command + output harapan, atau perilaku UI>
- Deps: — | after Unit N (<alasan>)
- Wave: <n> (wave sama = file-disjoint, boleh paralel; same-file = serialize)

## 3. Testing Strategy
<unit + smoke additions; bugfix unit → 3 regression check (repro/fix/unchanged);
property-style check utk invariant murni bila relevan>

## 4. Rollout & Rollback
<urutan merge, flag, rollback path>

## 5. Risks & Pitfalls
<sitasi STATE.md §Risks & waivers + pitfall repo yang dikenal>
