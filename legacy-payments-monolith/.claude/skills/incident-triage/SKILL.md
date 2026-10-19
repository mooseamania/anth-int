---
name: incident-triage
description: Use when an SRE is investigating an alert or incident: correlate logs, recent deploys and config changes, form ranked hypotheses, and draft a timeline and runbook updates. Read-only by default.
---

# Incident triage (SREs)

Goal: shorten time to a credible hypothesis and leave behind better runbooks. Humans decide and execute remediation.

## Operating mode
- Read-only investigation. Allowed: read logs and manifests, `kubectl get/describe/logs`, `git log/diff`, query dashboards. Not allowed without explicit human approval: `kubectl apply/delete/rollout`, config writes, restarts, scaling, anything against production data.

## Procedure
1. **Scope**: affected service, start time, customer impact, severity. Ask for what is missing; do not guess.
2. **Gather**: error logs around the start time, deploys and config changes in the preceding 24h (`git log --since`), recent infra changes, dependency health.
3. **Hypotheses**: list up to 3, ranked, each with the evidence for it, the evidence against, and the one command or query that would confirm or kill it.
4. **Recommend**: safest mitigation first (rollback, feature flag, scale), with the exact command for a human to run and the expected result. Note blast radius.
5. **Timeline**: maintain a running timeline with timestamps and sources.

## After the incident
- Draft the postmortem: summary, impact, timeline, root cause, what went well, action items with owners. Blameless tone.
- Propose runbook edits as a diff. Add the new detection query or alert that would have caught this earlier.
- Convert repeated manual steps into a script in Python or Go with a dry-run flag, and include a test.

## Guardrails
- Redact tokens, account numbers and personal data from anything written to a ticket or postmortem.
- Mark every statement as observed, inferred, or unknown.
