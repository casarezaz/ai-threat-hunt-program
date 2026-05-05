# Evidence Domain 2 — Intent / Trigger

## Question this domain must answer

> Why did the action occur?

## Minimum evidence

- Originating prompt (full text or hashed/redacted with a class summary)
- Workflow trigger (scheduled job, webhook, ticket, event)
- Approval record(s) tied to the action
- Policy rule that selected the path
- Upstream business process context

## Most common failure mode

Intent inferred from action. *"The agent decided to send the email"* is a guess. *"The agent sent the email because the user prompted it to draft and send a follow-up; the draft was approved at 14:02 by user X via Slack approval flow Y"* is evidence. Inference does not survive incident review.

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.2](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
