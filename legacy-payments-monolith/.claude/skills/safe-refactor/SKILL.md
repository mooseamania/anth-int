---
name: safe-refactor
description: Use when a software engineer wants to refactor, extract a module or service, or modernize legacy payments/banking code. Enforces characterization tests first, small reviewable steps, and no change to money-movement behavior.
---

# Safe refactor (software engineers)

Goal: change structure without changing behavior, in steps a reviewer can verify in minutes.

## Before touching code
1. State the target in one sentence (e.g. "extract `fraud` so it no longer imports `payments`").
2. Run `python tools/analyze_deps.py` and quote the edges involved. No boundary is proposed without measured coupling.
3. List the public functions other modules call. Their signatures are frozen unless the user approves a change.

## Characterization tests first
- For each frozen function, write a test that pins current behavior, including error cases (insufficient funds, daily limit, blocked payment).
- Run the tests on the untouched code and show they pass. If they cannot be written, stop and say what is missing.

## Refactor in small commits
- One structural move per commit: introduce interface, switch one caller, delete old path.
- Break cycles by inverting the dependency (pass data in, or define a small interface owned by the caller), never by copying logic.
- After each step: run tests and `python -m compileall`. Re-run the analyzer and report the change in cross-boundary edges and cycles.

## Guardrails (financial services)
- Never alter rounding, currency handling, limits, or ledger posting order without explicit approval and a test.
- No secrets in code, logs or fixtures. Config stays in environment variables.
- Anything touching `ledger` or `payments` gets a "risk notes" section in the PR description: what could go wrong, how it was checked, how to roll back.

## Output
PR-ready summary: what moved, evidence behavior is unchanged (test names), before/after coupling numbers, rollback plan, and open questions for a human owner.
