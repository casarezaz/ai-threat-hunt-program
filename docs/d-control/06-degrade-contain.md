# Step 6 — Degrade / Contain

**Objective:** Reduce capability quickly when risk exceeds confidence.

## Key actions

- Create graduated containment actions before an incident occurs.
- Degrade capability rather than choosing only between full access and total shutdown.
- Contain by revoking scopes, disabling connectors, forcing human approval, restricting data sources, sandboxing agents, limiting token volume, or pausing the workflow.

## Artifacts and telemetry

- Containment playbooks
- Kill-switch procedures
- OAuth revocation process
- Connector disablement paths
- Tenant rollback plans
- SOAR actions
- Evidence-preservation checklist

## Hunt pivots

- Switch agent from autonomous mode to approval-required mode
- Disable file-system tool for IDE agent
- Revoke calendar / email connector after abnormal sends
- Quarantine RAG index after sensitive-data ingestion error

## The seven graduated levels

The full ladder lives under [`playbooks/containment/`](../../playbooks/containment/):

| Level | Mode | Use when |
|-------|------|----------|
| L1 | Monitor | Risk is suspected; visibility is the gap |
| L2 | Limit | Specific data, scope, or action class is unsafe |
| L3 | Approval Gate | Action class is high-impact; humans should be in the loop |
| L4 | Degrade | Confidence has dropped; reduce mode (autonomous → assisted, write → read) |
| L5 | Isolate | Compromise is plausible; cut blast radius |
| L6 | Suspend | Incident is active; pause the asset |
| L7 | Terminate | Asset cannot be operated safely; remove it |

## The most important containment question

> Can the organization reduce capability faster than the AI can expand blast radius?

If not, the asset is uncontained regardless of policy language.

## Outputs

- A tested containment playbook for the asset (at least L1–L3 baseline)
- A SOAR action or runbook step that an on-call analyst can execute under pressure
- A validated kill-switch and a rotation/revocation procedure

## Exit criteria for this step

You may move on to **Document** when:

1. The containment ladder for the asset is tested, not theoretical.
2. The on-call analyst knows where the kill-switch is, before they need it.
3. Every level has a clear trigger criterion, owner, and reversal path.
