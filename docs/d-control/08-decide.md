# Step 8 — Decide

**Objective:** Force a clear business / security decision instead of passive exposure.

## Key actions

- Convert findings into a decision: **allow, limit, monitor, redesign, pause, replace, or terminate.**
- Tie decisions to residual risk, business value, compensating controls, and executive accountability.
- Revisit decisions when the AI system gains new connectors, data access, model capabilities, or autonomy.

## Artifacts and telemetry

- Risk acceptance decision
- Go / no-go record
- Exception expiration date
- Remediation plan
- Executive dashboard
- Control maturity score
- Quarterly review packet

## Hunt pivots / illustrative decisions

- "Approve SaaS AI for low-risk content only."
- "Limit enterprise agent to read-only access until logging improves."
- "Pause browser-agent pilot until session-isolation controls are available."
- "Terminate vendor due to insufficient auditability."

## The decision menu

| Decision | When |
|----------|------|
| **Allow** | Residual risk is within policy; controls and telemetry are in place |
| **Limit** | Residual risk is acceptable only with reduced scope, data, or audience |
| **Monitor** | Residual risk is acceptable only with elevated logging and review |
| **Redesign** | The asset can be safe but not as currently architected |
| **Pause** | A specific control / telemetry gap must be closed before continuing |
| **Replace** | Another asset / vendor provides the same value at lower risk |
| **Terminate** | The asset cannot be operated safely; remove it |

## Outputs

- A dated, signed decision in `templates/decision-log.csv`
- A review date and an owner
- An update to the **Executive Risk Brief** if material

## When the loop re-triggers

D-Control re-runs from Discover whenever the asset gains:

- A new connector
- A new model
- A new data source
- A new action capability
- A new vendor subprocessor
- A new privileged role
- A new customer-facing workflow

The loop is not annual. It is event-driven.

## Closing thought

> AI security without D-Control is policy theater. AI with agency requires operational control.
