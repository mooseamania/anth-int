---
name: model-notebook-to-pipeline
description: Use when a data scientist wants to turn an exploratory Jupyter notebook (fraud, credit scoring, customer behavior) into a reproducible, reviewable pipeline with documented validation. Covers pandas/scikit-learn/TensorFlow workflows.
---

# Notebook to pipeline (data scientists)

Goal: keep the science, remove the manual re-running. Never change modeling choices silently.

## Step 1: Read and summarize
- Read the notebook top to bottom. Produce a short plain-English summary: data sources, features, target, split strategy, model, metrics.
- List anything that makes it non-reproducible: hard-coded paths, unseeded randomness, cell-order dependencies, leaked columns, manual fixes.

## Step 2: Extract
- Move to modules: `data.py` (load + validate), `features.py`, `train.py`, `evaluate.py`, plus a thin entry point. Keep notebook cells as the reference and show equivalence by comparing metrics on a fixed seed.
- Add data validation: schema, null rates, and range checks. Fail loudly with a clear message.
- Time-based splits for fraud and credit models; flag any random split on temporal data.

## Step 3: Model-risk documentation (draft for human review)
Generate a model card: intended use, training data window, features and why each is permitted (flag protected-class proxies for fair-lending review), performance by segment, known limitations, monitoring plan. Mark every claim not verified from the notebook as "needs confirmation".

## Step 4: Tests and handoff
- Unit tests for feature logic, a smoke test on a tiny synthetic sample, and a metrics-regression test with a tolerance.
- Produce the orchestration config for the team's existing scheduler. Do not introduce a new platform.

## Guardrails
- Use synthetic or de-identified data in examples. Never print customer records.
- Report metrics exactly as computed; do not tune to improve them unless asked.
- The data scientist signs off on model changes; the model-risk team owns approval.
