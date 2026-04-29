# Contributing

Small additions welcome. This is a working program *and* the source for a field guide, so changes have to clear two bars:

1. **Operationally useful.** Could a defender act on this in their environment within a quarter? If not, rework it.
2. **Anti-theater.** No vague risk language, no marketing-driven framework name-drops, no checkbox content.

## Good first additions

- A new hunt hypothesis. Copy `hunts/template.md` to `hunts/starter/H-NNN-<short-name>.md` (or to an asset-class-prefixed file like `hunts/RAG-001-...md`). Include data sources, query logic, and the decision template.
- A new asset class entry in `templates/ai-asset-schema.json` with rationale.
- A more concrete containment action under `playbooks/containment/L*-*.md` for a specific asset class.
- A new metric in `metrics/executive-metrics.md` with definition, data source, target, and cadence.

## Style

- Prefer short, declarative sentences. Defenders read these under pressure.
- Use the project's vocabulary: Discover / Define / Detect / Deny / Defend / Degrade / Document / Decide.
- Tag artifacts with the relevant D-Control step(s), OWASP LLM / Agentic AI category, and MITRE ATLAS technique where applicable.

## What this repo does not accept

- Vendor pitches.
- Hunts whose only output is "investigate further." Every hunt has to produce findings, evidence, control gaps, and a decision.
- Risk language without a decision template attached.

## Pull requests

- One concept per PR.
- Reference any source paper (e.g., "supports Paper 2 §Detect").
- If the change introduces a new template column, update both the CSV header and the JSON schema.
