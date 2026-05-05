# Evidence Domain 7 — Time

## Question this domain must answer

> Can the chain be reconstructed?

## Minimum evidence

- Normalized timestamps (UTC, sub-second precision) on every audit event
- Correlation ID propagated end-to-end (front door → model gateway → tool calls → data access → response)
- Retention long enough to cover the longest plausible incident timeline (typically 13 months for regulated industries; longer under litigation hold)
- Export path that does not depend on vendor cooperation during a live incident
- Chain-of-custody handling for evidence that may be reused in regulatory or legal proceedings

## Most common failure mode

Six different log sources, six different clocks, no shared identifier. Every individual link exists; the chain cannot be assembled. Without correlation-ID propagation a workflow cannot exit Level 1 of the maturity model. See [Paper 4 §10](../papers/paper-4-d-evidence.md#10-telemetry-and-integration-patterns) for the implementation pattern.

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.7](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
