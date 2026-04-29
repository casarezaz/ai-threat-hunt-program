# Step 2 — Define

**Objective:** Classify capability, data access, agency, identity, and blast radius.

## Key actions

- Classify the asset type: SaaS LLM, embedded copilot, enterprise agent, custom/internal agent, IDE/CLI agent, browser/computer-use agent, RAG system, or workflow/RPA agent.
- Determine whether the system can read, write, execute, transact, publish, delete, deploy, approve, or modify security controls.
- Map sensitive data exposure and identity context.

## Artifacts and telemetry

- AI asset register
- Data classification matrix
- Capability / agency scoring
- Identity and permission mapping
- Business process map
- Vendor shared-responsibility notes

## Hunt pivots

- AI tool with write access but no named owner
- Agent able to call ticketing and messaging APIs without an approval gate
- RAG pipeline indexing restricted documents
- Copilot enabled in a tenant without role-based policy review

## The five define-step questions

For every asset, force an answer:

1. **Data** — What data can it access?
2. **Identity** — What identity does it act through?
3. **Action** — What actions can it take?
4. **Telemetry** — What logs / signals exist?
5. **Containment** — What containment path exists?

## Outputs

- Capability / Agency rating (Low / Medium / High / Critical)
- Data sensitivity rating (Public / Internal / Confidential / Regulated)
- Identity context (User / Service Account / Privileged / Shared / External Vendor)
- Updated row in **AI Risk Register** (`templates/ai-risk-register.csv`)
- Decision-ready summary suitable for the **Executive Risk Brief** template

## Exit criteria for this step

You may move on to **Detect** when:

1. The asset has class, capability, data, identity, owner, and vendor recorded.
2. The "what could it do on its worst day?" sentence is in writing.
3. Both telemetry and containment fields are populated, even if the answer is "none."
