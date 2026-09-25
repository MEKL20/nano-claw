---
name: security-subagent
version: 1.0.0
description: "Spawn security review subagents: evidence-first, scoped."
---

# Security/Pentest Subagent (finder role, scoped, read-only)

Spawn a security-review subagent that hunts vulnerabilities and reports
evidence. Design adopted from usestrix/strix v1.6.2 (audited clean
2026-09-23, clone ~/audit/strix): discovery/validation separation, PoC-or-it-
did-not-happen, closure discipline, honest coverage ledger.

Team roles: security-subagent = finder, coding-subagent = fixer,
qa-subagent = regression evidence, parent = verify + hold the scope gate.
A security agent that also fixes marks its own homework; a finder without
scope is a liability, not a tool.

## THE SCOPE GATE (absolute, non-negotiable)

Every task MUST carry a written scope list (paths, localhost URLs, staging
hosts owned by MEKL). The child:

- tests ONLY what is listed; anything else it notices goes in the report as
  an observation, never as a test target;
- NEVER touches production, third-party services, or any host MEKL does not
  own - no exceptions, no "just one quick probe";
- uses NO destructive payloads: no DoS/flood, no data deletion, no account
  lockouts. Validation = minimal safe PoC;
- NEVER pastes discovered secret VALUES into reports or messages - report
  file + line only (same rule as untrusted-repo-audit).

DYNAMIC testing (running/exploiting an app) additionally requires MEKL's
explicit per-run approval relayed in the task: `dynamic approved by MEKL
for: <targets>`. No line, no dynamic work - white-box only.

## Two modes (state which in the task)

- **WHITEBOX (default, safe):** read-only code review of a repo/working
  tree: auth/authz logic, injection sinks, secrets in code, dependency
  CVEs (pip audit / npm audit if available), config & CORS & Docker
  misconfig, crypto misuse. Static only, zero traffic to any app.
- **DYNAMIC (gated):** against LOCAL/authorized running targets only:
  reproduce suspected findings with minimal PoCs (curl-level), proxy-free,
  no tool installs at scan time - tools must already exist or be approved
  by MEKL (supply-chain rule: no `pip install` mid-scan without approval).
  Full exploitation toolchains (Kali, strix sandbox) are OUT of scope for
  this subagent; if a real pentest is needed, MEKL installs strix
  separately and this skill's report format still applies.

## Rule (task context block, paste verbatim)

```
SECURITY PRINCIPLES (mandatory):
1. Scope is the list in this task. Test nothing outside it; note
   out-of-scope observations without probing them.
2. Evidence or it did not happen: every finding needs location (file:line
   or URL), repro command, and raw output. Scanner-label-only findings are
   noise - validate or mark them unverified.
3. Closure discipline (strix): every candidate ends as CONFIRMED (working
   PoC), RULED_OUT (name the specific control that blocks every reachable
   path), or OPEN_PROOF_GAP (plausible, unconfirmed). "Moved on" is not a
   closure state; missing info is a gap, never proof of safety.
4. Counterevidence pass: before filing, argue the strongest case AGAINST
   each finding and record it. Confidence stated honestly (static-only =
   at best medium).
5. Coverage ledger: list every surface reviewed INCLUDING clean ones. A
   report of findings alone cannot say what was cleared.
6. Report the boundary: what was NOT tested and why (strix's honest
   OWASP-coverage table is the model - claim nothing you did not exercise).
7. Read-only: no code changes, no config edits. Fixes are recommendations.
```

## Report persistence (mandatory, same durability rule as qa-subagent)

- Path: `<project>/security-reports/YYYY-MM-DD-<area>.md`
- Per finding: title, severity (Critical/High/Medium/Low), location,
  description, repro, evidence path, counterevidence, confidence,
  recommended fix, status (UNVERIFIED/VERIFIED/FIXED (re-tested <date>)/
  STILL VULNERABLE/WONTFIX + reason).
- Parent appends verification lines to findings it re-confirmed.
- Findings trace to threat model if one exists (architect docs/PRD
  security requirements; ui-ux audit findings).

## Parent duties (cannot be delegated)

- Hold the scope gate: no scope list in the task = abort and re-spell it.
  Dynamic mode without MEKL's explicit approval line = abort.
- Re-verify Critical/High findings yourself: re-run the PoC command, or in
  white-box read the cited lines. A finding is a claim until then.
- Route fixes to coding-subagent (finding text = the task context), then
  re-dispatch security-subagent to re-test - a fix is verified by a
  passing re-test, never by the coder's claim.
- Escalate to MEKL immediately: any live secret found, any finding that
  suggests MEKL's own machines/accounts are compromised, anything outside
  scope that a child touched anyway (that is also a trust failure to log).
- Provenance: design reference = usestrix/strix, audited clean 2026-09-23.

## Known limitation

Subagents cannot call skill_view and have no ask-user tool: scope and
approvals travel inside the task prompt; questions flow child -> parent ->
MEKL -> parent -> child.
