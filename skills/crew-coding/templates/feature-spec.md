# FEATURE-SPEC: <nama inisiatif> v<N>

> Milik epic produk — sitasi `PRD §x`. EARS untuk semua behavior. Untuk fitur
> kecil yang well-understood, file ini boleh jadi QUICK-SPEC gabungan
> (requirements + design sketch + tasks, tanpa gate antar-fase; gate kode tetap).

## Clarifying Questions (front-loaded — Quick Spec principle)
> Jawab DULU sebelum dokumen dipakai; tiap pertanyaan WAJIB disertai rekomendasi.
1. <scope/constraint/edge case> — rekomendasi: <…> (keputusan final: nano)

## 1. Requirements (EARS)
| ID | Requirement |
|---|---|
| R1 | WHEN <kondisi> THE SYSTEM SHALL <perilaku teramati> |
| R2 | IF <trigger> THEN THE SYSTEM SHALL <respons> |

### Edge cases & error handling
- <boundary, failure mode, konkurensi — yang happy-path lewatkan>

## 2. Design Sketch
<komponen terdampak, data flow, error handling, testing strategy.
Versi penuh = SDD/dok desain terpisah (design-first lane: dokumen desain
divalidasi DULU, requirements di atas DITURUNKAN darinya)>

## 3. Tasks Overview (input backlog lead)
| Unit | Cakupan file | Deps | Demo: (bukti observable selesai) |
|---|---|---|---|
| 1 | <file persis> | — | <command + output harapan> |

## 4. Risks & Pitfalls
<sitasi invariant STATE.md / pitfall yang dikenal>
