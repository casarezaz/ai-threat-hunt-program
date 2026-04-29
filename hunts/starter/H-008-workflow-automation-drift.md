# H-008 — Workflow automation drift

| Field | Value |
|-------|-------|
| Hunt ID | H-008 |
| D-Control step(s) | Detect, Deny, Document |
| Asset class(es) | Workflow / RPA agents, embedded copilots |
| OWASP LLM / Agentic AI | LLM06 Excessive Agency, Agentic AI ATA-005 Cascading hallucinations |
| MITRE ATLAS | (general) Persistence / Impact via automation |
| Owner | _to assign_ |
| Cadence | Weekly |

## Hypothesis

AI-enabled workflow runs are creating, sending, approving, deleting, publishing, deploying, or updating records without the required human approval gate.

## Why this matters

When a workflow gains an AI step, the original approval logic often gets quietly bypassed. The audit trail looks the same; the controls do not work the same.

## Data sources

- Workflow platform run history (Power Automate, Zapier, n8n, Workato, ServiceNow flows, etc.)
- Approval system logs
- Source-of-truth audit logs (the systems the workflow modifies)

## Query / detection logic

```text
workflow_run.action in {create, send, approve, delete, publish, deploy, update}
  AND workflow_run.actor in ai_agents_or_service_accounts
  AND NOT exists(approval_event linked to workflow_run)
```

## Expected normal vs. abnormal

- **Normal:** Every high-impact action has a recorded approval event with an identified human approver.
- **Abnormal:** Approval-required actions executing under a service account; previously human-approved steps now executing autonomously.

## Evidence to capture

- Workflow ID, version, last editor, timestamp
- Action(s) taken
- Records modified (IDs, before/after where in scope)
- Whether prior runs had a human approver

## Findings / Control gaps / Decision

_(filled in per run)_
