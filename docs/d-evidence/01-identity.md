# Evidence Domain 1 — Identity

## Question this domain must answer

> Who or what initiated the action?

## Minimum evidence

- Human user (full identity, not just display name)
- Agent identity (which agent, which version, which orchestration framework)
- Service account / app registration / workload identity used downstream
- Delegated token (issuer, scopes, age, last-use)
- Device and session context (managed / unmanaged, MFA state, session age)

## Most common failure mode

Partial identity. The audit log records that "App X" took an action, but the program cannot reconstruct which user's delegated authority App X was acting under, which agent inside the application actually selected the action, or which token version was in flight. Each missing layer is a finding.

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.1](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
