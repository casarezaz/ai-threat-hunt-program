# Evidence Domain 6 — State

## Question this domain must answer

> What version / configuration was active?

## Minimum evidence

- Model version or model digest
- System prompt version / hash
- Agent configuration snapshot ID
- Plugin / tool registry version
- Policy version
- Exception state (which exceptions were active, who owned them)

## Most common failure mode

State as runtime memory. The program can describe what the agent does *now* but cannot describe what it was *at the moment of the incident*. Without state versioning, a postmortem can say *"the agent did X"* but not *"the agent did X under a system prompt that had been changed 14 minutes earlier by an unrelated rollout."* The second sentence is what allows leadership to distinguish a control failure from a configuration regression.

State versioning is the single most overlooked instrumentation change required to move from Level 2 to Level 3 of the [maturity model](../../templates/d-evidence-maturity.md).

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.6](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
