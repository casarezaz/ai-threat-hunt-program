# Evidence Domain 5 — Control

## Question this domain must answer

> What allowed, blocked, warned, logged, or escalated it?

## Minimum evidence

- Policy decision point output (which policy fired, what verdict)
- IAM rule evaluation (request, principal, scope, decision)
- DLP event (matched or scanned-and-allowed; both are evidence)
- CASB / SSE log entry
- Model guardrail decision (allow, block, transform — including non-firings)
- Approval gate state (required / waived / bypassed)
- EDR / network control decision

## Most common failure mode

Logging only firings. A control that records every block but never records "scanned and allowed" cannot prove non-events. The program needs both: the control fired, and the control evaluated and chose to allow. Otherwise an incident review cannot distinguish *"the control worked"* from *"the control was off."*

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.5](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
