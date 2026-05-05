# Evidence Domain 3 — Action

## Question this domain must answer

> What did the system actually do?

## Minimum evidence

- Tool call name + parameters (not just outcome)
- API request method, endpoint, and body summary
- Data query (the actual query, not just the count of results)
- Files accessed, messages sent, tickets modified — with before/after content
- Admin changes (the change content, not just the change event)
- Planned action (agent's stated plan) **and** executed action (what actually happened)

## Most common failure mode

Outcome-only logging. *"Ticket updated"* without the change content is not action evidence. The program also needs the divergence between planned and executed actions — that gap is itself a high-value signal.

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.3](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
