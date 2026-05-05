# D-Evidence Maturity Self-Assessment

> Self-assess honestly. The worst answer is to claim a maturity level the program cannot demonstrate. See [Paper 4 §9](../docs/papers/paper-4-d-evidence.md#9-d-evidence-maturity-model).

## Scope of this assessment

| Field | Value |
|-------|-------|
| Workflow under review | `<name + asset_id>` |
| Assessor | `<person>` |
| Assessment date | `<YYYY-MM-DD>` |
| Target maturity for this workflow | Level `<0–4>` |
| Justification for target | `<one sentence — typically tied to data class, action surface, customer impact>` |

## Maturity rubric

| Level | Name | Evidence Behavior | Leadership Risk |
|------:|------|-------------------|-----------------|
| 0 | Blind | AI workflows execute with limited identity, prompt, tool, or data-access logging. | Material AI workflow risk cannot be bounded after an incident. |
| 1 | Fragmented | Some logs exist, but identity, data access, and tool actions are not correlated. | Investigations depend on manual reconstruction and vendor cooperation. |
| 2 | Traceable | Core actions have correlation IDs and enough telemetry to reconstruct high-risk events. | Incident response is possible but may be slow or incomplete. |
| 3 | Decision-grade | Evidence supports control validation, risk decisions, legal review, and audit requests. | Leadership can defend decisions with proof instead of assumptions. |
| 4 | Continuously validated | Findings convert into continuous monitoring, automated evidence collection, and periodic re-hunts. | The program proves ongoing control effectiveness, not one-time compliance. |

## Self-check questions (per level)

A workflow is at Level **N** only if it can answer "yes, with evidence" to every question at level **N** *and below.* Aspirational answers do not count.

### Level 1 — Fragmented (entry threshold)

- [ ] Are at least some identity, prompt, tool, and data-access logs available for this workflow?
- [ ] Are those logs retained for at least 90 days?

### Level 2 — Traceable

- [ ] Does every user-originated request through this workflow carry a correlation ID end-to-end?
- [ ] Can the program reconstruct a high-risk event timeline within four hours, using its own evidence repository, without vendor support?
- [ ] Does the workflow emit state versioning (model, system prompt, agent config, tool registry, policy) on each audit event?

### Level 3 — Decision-grade

- [ ] Can the program produce a [decision-grade evidence package](d-evidence-package.md) for a sample finding without retroactive log gathering?
- [ ] Does the workflow's evidence chain cover all seven domains (identity, intent, action, data, control, state, time) with named log sources for each?
- [ ] Are evidence retention windows aligned with the longest applicable regulatory / contractual / litigation-hold horizon for the affected data classes?
- [ ] Can the program export evidence on request (audit, regulator, customer, counsel) under documented controls?
- [ ] Is the workflow's evidence held in the program's own [evidence repository](../docs/papers/paper-4-d-evidence.md#11-evidence-repository-architecture), not only in the vendor console?

### Level 4 — Continuously validated

- [ ] Are findings from this workflow converted into continuous monitoring (not one-time hunts)?
- [ ] Is evidence collection automated (or at least scheduled) rather than analyst-on-demand?
- [ ] Are containment actions for this workflow validated by re-hunt on a defined cadence?
- [ ] Is at least one tabletop per year run against this workflow's evidence repository, end-to-end?

## Result

| Item | Value |
|------|-------|
| Current maturity | Level `<0–4>` |
| Gap to target | `<description>` |
| Top three instrumentation needs | 1. <br> 2. <br> 3. |
| Owner of each gap | |
| Quarter to close | |

## Logging the result

Record the assessment in the AI Asset Register `notes` field and create one or more evidence-gap findings for unmet level requirements. Reassess on the cadence in [`templates/operating-cadence.md`](operating-cadence.md), or on event-driven triggers.
