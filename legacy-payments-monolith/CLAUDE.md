# fintechco_core (legacy payments monolith) - demo repo

Synthetic stand-in for a decade-old Python monolith. Nothing here is real customer code.

## Layout
- `fintechco_core/` - single deployable: auth, accounts, ledger, payments, fraud, notifications, reporting, mobile_api, batch_jobs
- `tools/` - analysis helpers (import graph, boundaries)
- `deploy/eks/` - target Kubernetes manifests (generated during the demo)
- `outputs/` - generated graph + reports

## Conventions
- Python 3.11, stdlib only. No new dependencies without asking.
- Do not change money-movement behavior while refactoring. Preserve public function signatures unless told otherwise.
- Never write secrets to files; config comes from env vars.
- Any proposed service boundary must be justified with measured coupling (edges in/out), not intuition.

## Commands
- `python tools/analyze_deps.py` - rebuild `outputs/graph.json` and `outputs/boundaries.md`
- `python -m compileall fintechco_core` - quick syntax check
