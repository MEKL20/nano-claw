# TEMPLATE: body task kanban (brief worker)

> Worker = anak tanpa konteks percakapan. Semua yang dibutuhkan harus ada di body.
> PLAN-IN-BRIEF (task medium 15–60 menit): body ini MERANGKAP plan — tidak ada
> doc terpisah; sertakan problem statement + breakdown ber-Demo di CONTEXT.

```
ROLE: <role>

BACA DULU: AGENTS.md, docs/STATE.md (auto-load dari workspace) + <path doc lain
dengan § yang wajib dibaca — sebut eksplisit>

CONTEXT: <2-4 kalimat self-contained: apa yang dikerjakan, kenapa, keputusan
final yang mengikat (jangan buka lagi debat yang sudah ditutup)>

DELIVERABLE: <path file persis ATAU "task result text">

AC (EARS):
- WHEN <kondisi> THE SYSTEM SHALL <perilaku teramati>
- IF <trigger> THEN THE SYSTEM SHALL <respons>

Demo: <SATU baris bukti observable: command + output harapan / perilaku UI>

VERIFY (jalan sendiri sebelum lapor): <commands: test/build/smoke>

DILARANG: git commit/push; menyentuh file di luar deliverable; <larangan
spesifik repo: HTML5 DnD, pasteNormalize, version bump, dst.>

DEPS: — | ready after <task-id> (<alasan>)
```

> Gate: kode app = triple gate (lead review + qa PASS + security clean).
> Docs/CI = verifikasi orkestrator saja. Ragu? Perlakukan sebagai kode.
