# Interview kit

- `PREP-GUIDE.md`: run of show, slide copy, demo runbook, Q&A, solutioning framework. Start here.
- `legacy-payments-monolith/`: demo repo (synthetic)
  - `fintechco_core/`: the legacy monolith
  - `tools/analyze_deps.py`: measures coupling; `tools/build_viz.py` builds the graph
  - `outputs/graph.html`: interactive dependency map (pre-generated fallback)
  - `outputs/business-impact.html`: non-technical mobile/ROI view with adjustable assumptions
  - `deploy/eks/`: suggested EKS cluster and manifests
  - `.claude/skills/`: `safe-refactor` (engineers), `model-notebook-to-pipeline` (data scientists), `incident-triage` (SREs)
  - `CLAUDE.md`: project rules Claude Code reads automatically

Regenerate: `cd legacy-payments-monolith && python tools/analyze_deps.py && python tools/build_viz.py`
