# L3 — Approval Gate

**Objective:** Require human approval before send, deploy, delete, transact, publish, or modify.

## Trigger criteria

_Document the precise conditions that move an asset to this level. Examples below; replace per asset class._

- ...
- ...

## Owner / on-call

- Primary: _to assign_
- Secondary: _to assign_
- Approver for the move (if level >= L3): _to assign_

## Pre-checks (before action)

- Confirm the asset identity, owner, and current capability.
- Confirm the affected user / data scope.
- Confirm evidence preservation is in flight (see Evidence section).

## Actions

_(replace with concrete, command-level steps for each asset class — SaaS LLM, embedded copilot, enterprise agent, IDE agent, browser agent, RAG, workflow, security agent.)_

- ...
- ...

## Evidence to preserve

- Identity, time, action sequence
- Configuration snapshot before the change
- Logs from the relevant control plane (IdP, SaaS, gateway, vector DB, workflow)
- Decision-maker, justification, and timestamp

## Communication

- Internal: who is told, in which channel, in what form?
- External (vendor / customer): is a vendor support case or customer notice required?
- Executive: does this change a metric reported in the Executive Risk Brief?

## Reversal / next-step path

- Conditions to drop one level (back toward L1)
- Conditions to escalate one level (toward L7)
- Required validation before reversal
