# Step 5 — Defend

**Objective:** Harden the environment so approved AI can operate within controlled boundaries.

## Key actions

- Apply least privilege to identities, tools, data stores, and connectors.
- Separate read from write actions and require approvals for high-risk action classes.
- Secure model APIs, RAG ingestion, vector stores, CI/CD, secrets, logging, and vendor configurations.
- Add prompt and output handling controls where practical, but **do not rely on prompt controls alone**.

## Artifacts and telemetry

- Reference architecture
- Secure configuration baseline
- Approval workflow
- Prompt / data handling standard
- Secrets management
- Logging standard
- Vendor security requirements
- Red-team test plan

## Hunt pivots

- RAG ingestion pipeline validates source authorization
- Agent can draft but not send external email without approval
- IDE agent runs in isolated dev workspace
- Model API keys stored in managed secrets vault

## The hardening priority order

1. Identity (who is the AI, and through whose context does it act?)
2. Action surface (read vs. write, draft vs. send, plan vs. execute)
3. Data ingress and egress (RAG sources, prompts, outputs, file paths)
4. Connector and tool surface (OAuth scopes, API allow-lists, sandboxing)
5. Prompt / output handling (last line of defense, not the only line)

## Outputs

- A documented hardening change against the asset
- An updated Reference Architecture or Secure Configuration Baseline
- A red-team or purple-team finding with a follow-up ticket

## Exit criteria for this step

You may move on to **Degrade / Contain** when:

1. The asset operates with the minimum identity, scopes, and data access required.
2. High-risk actions have an approval gate or are blocked.
3. Logging and secrets are managed centrally, not per-developer.
