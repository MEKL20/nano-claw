# SDD: <product/system> v<N>

> Deliverable architect. Requirements-first lane: derived dari PRD §x.
> Design-first lane: SDD jalan DULUAN — §2/§7/§8 wajib eksplisit agar pm bisa
> menurunkan requirements FEATURE-SPEC yang feasible dari desain ini.

## 1. Context
<masalah sistem, batasan, kondisi existing, input (spike report bila ada)>

## 2. Architecture Overview
<diagram-as-text: modul + koneksi + boundary>

## 3. Components
| Komponen | Tanggung jawab | Interface (contract) |
|---|---|---|

## 4. Data Flow
<aliran data antar komponen; sequence diagram bila urutan interaksi menentukan>

## 5. Data Model
<ERD bila relevan: entitas, relasi, constraint, strategi evolusi/migrasi>

## 6. Error-Handling Approach
<failure mode per komponen + perilaku sistem:>
- IF <failure> THEN THE SYSTEM SHALL <respons teramati>

## 7. Tech Decisions (ADR)
### ADR-1: <keputusan>
- Context: <…>
- Decision: <…>
- Consequences: <…>
- Rejected alternatives: <… + alasan satu baris each>

## 8. Invariants (properties — mengalir ke STATE.md + check qa)
| ID | Properti | Verifikasi |
|---|---|---|
| INV-1 | Untuk setiap <input/state valid>, THE SYSTEM SHALL <tahan sifat> | <unit/smoke/property-style check> |

## 9. Risks
<risiko teknis + mitigasi; risiko diterima → daftarkan ke STATE.md §Risks & waivers>

## 10. Testing Strategy
<piramida per komponen; invariant §8 → cara tes; apa yang TIDAK perlu dites>

## 11. Verification Steps
<cara lead/nano memverifikasi implementasi sesuai SDD ini: command + bukti>
