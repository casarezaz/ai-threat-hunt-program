# Step 4 — Deny

**Objective:** Stop unsafe behavior before it becomes an incident.

## Key actions

- Deny unsanctioned AI apps where policy, data exposure, or vendor risk is unacceptable.
- Restrict high-risk connectors, plugins, scopes, browser extensions, autonomous workflow triggers, and data sources.
- Enforce role-based access, conditional access, approval gates, and data-loss prevention.

## Artifacts and telemetry

- SSE / SWG policy
- CASB controls
- OAuth app restrictions
- Conditional access rules
- DLP policies
- API allow / deny lists
- Browser extension controls
- Tenant configuration baselines

## Hunt pivots

- Block AI upload of restricted data
- Deny third-party AI OAuth app with Gmail / Drive / SharePoint write scopes
- Prevent unmanaged browser-agent extension installation
- Disable autonomous approval workflow without human review

## Outputs

- A policy / control change with a change ticket and an owner
- An exception register entry (`templates/exception-register.csv`) for any allowed deviation, with expiration
- A test result confirming the deny control fires (positive case + negative case)

## Exit criteria for this step

You may move on to **Defend** when:

1. Unsafe defaults are off; safe defaults are explicit.
2. Every exception has an owner, a reason, a compensating control, and an expiration.
3. Deny controls have been tested at least once (purple-team or tabletop).
