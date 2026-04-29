# Step 3 — Detect

**Objective:** Create the visibility needed to prove normal and abnormal AI behavior.

## Key actions

- Identify minimum viable telemetry for prompts, outputs, tool calls, API calls, data retrieval, identity, admin changes, connector changes, and error / failure paths.
- Build hunt hypotheses around misuse, leakage, tool abuse, prompt injection, excessive agency, anomalous data retrieval, and unauthorized automation.
- Validate whether detections work through testing, purple-team exercises, and controlled simulation.

## Artifacts and telemetry

- SIEM queries
- SaaS audit logs
- DLP alerts
- EDR telemetry
- API gateway logs
- Vector DB query logs
- RAG retrieval logs
- Workflow run history
- LLM gateway logs
- Model billing and token usage

## Hunt pivots

- Prompt containing secrets or regulated data
- Agent tool-call spike outside business hours
- Unusual vector search against privileged documents
- AI-generated code committed with hardcoded credentials
- OAuth grant followed by mass file access

## Starter backlog

The 10 starter hunts are catalogued under [`hunts/starter/`](../../hunts/starter/). Each one produces four artifacts: findings, evidence, control gaps, and a decision.

## The detection question

> Who used the AI, what data was involved, what action was taken, what control allowed it, and how fast can it be contained?

If the answer requires guessing on any of those five, telemetry is insufficient.

## Outputs

- Confirmed log-source coverage row in the **Telemetry Requirements Matrix** (`templates/telemetry-requirements-matrix.csv`)
- At least one hunt hypothesis filed under `hunts/`
- Detection rule, query, or signal mapped to the asset

## Exit criteria for this step

You may move on to **Deny** when:

1. The asset's telemetry coverage is rated against the requirements matrix.
2. At least one detection or hunt hypothesis is in production or in a tested state.
3. Known telemetry gaps are escalated as residual risk, not silently accepted.
