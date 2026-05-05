# D-Evidence: The Proof Layer

> **Principle:** Every AI-enabled security concern must be traceable across **identity, intent, action, data, control, state, and time.** If any link is missing, the organization should label that missing link as a risk finding, not as an analyst inconvenience.

D-Control defines what should constrain AI behavior. D-Evidence defines whether the constraint can be proven. Read [Paper 4 — D-Evidence](../papers/paper-4-d-evidence.md) for the full doctrine.

## The seven evidence domains

1. [**Identity**](01-identity.md) — Who or what initiated the action?
2. [**Intent / Trigger**](02-intent.md) — Why did the action occur?
3. [**Action**](03-action.md) — What did the system actually do?
4. [**Data**](04-data.md) — What information was touched?
5. [**Control**](05-control.md) — What allowed, blocked, warned, logged, or escalated it?
6. [**State**](06-state.md) — What version / configuration was active?
7. [**Time**](07-time.md) — Can the chain be reconstructed?

Each page is a one-pager: the question the domain must answer, the minimum evidence, the most common failure modes, and what the program treats as a finding when the evidence is missing.

## The pairing with D-Control

D-Control and D-Evidence are designed to be used together. Every D-Control question implies a D-Evidence follow-up; missing evidence is a risk finding in its own right.

| D-Control Question | D-Evidence Follow-Up | Risk Finding if Missing |
|--------------------|---------------------|-------------------------|
| Was the agent supposed to access this SaaS app? | Show the grant, scope, approver, owner, and last-use evidence. | Unknown non-human access path. |
| Was the tool call allowed? | Show the policy decision, request context, response, and correlation ID. | Control may be unenforced or untestable. |
| Was sensitive data retrieved? | Show object access, retrieval source, classification, output path, and retention. | Data exposure cannot be bounded. |
| Was human approval required? | Show approval workflow, approver identity, timestamp, and exception logic. | Delegated automation may bypass accountability. |
| Was containment completed? | Show revocation, session kill, token invalidation, access review, and validation hunt. | Residual access may remain active. |

## Operational artifacts produced by D-Evidence

- A [**Decision-Grade Evidence Package**](../../templates/d-evidence-package.md) for every material finding.
- A [**Maturity self-assessment**](../../templates/d-evidence-maturity.md) (Levels 0–4) to track program state.
- Evidence-gap findings filed alongside hunt findings, funding the next quarter's instrumentation backlog.
