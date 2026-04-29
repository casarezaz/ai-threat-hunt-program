# AI Vendor Due Diligence Questionnaire

The questions a D-Control program needs answered before allowing a third-party AI to operate inside the environment.

## 1. Identity and access

- What identity does the AI act through (per-user OAuth, service account, vendor service principal)?
- What scopes are required for minimum function vs. requested by default?
- How are tokens stored and rotated?

## 2. Data

- Where is customer data processed (region, sub-processors)?
- What data is used for training, fine-tuning, or evaluation? Is opt-out available and verifiable?
- How is regulated data (PII, PHI, PCI, IP) handled, segregated, and deleted?
- Retention defaults and configurability?

## 3. Capability and agency

- What actions can the system take on the customer's behalf (read, write, send, deploy, delete, approve)?
- Can capabilities be reduced post-deployment without losing core function?
- Are there autonomous loops, and how are they bounded?

## 4. Telemetry and audit

- What logs are produced for prompts, outputs, tool calls, retrieval, admin changes?
- How are logs exported (SIEM-ingestible format, latency, retention)?
- Is prompt-level logging available without changing tier?

## 5. Containment

- Kill-switch / pause-of-service: who can invoke, how fast, what is preserved?
- Per-tenant rollback for connectors, model versions, or RAG indexes?
- Customer-controlled disablement of high-risk features?

## 6. Security posture

- SOC 2 Type II / ISO 27001 / FedRAMP status, with letter date.
- Pen-test cadence, last test date, summary of high/critical findings, remediation status.
- Vulnerability disclosure / bug-bounty program?

## 7. Incident response

- Notification SLA for incidents affecting customer data or operability.
- Subprocessor change notification process.
- Tabletop participation: will the vendor join a customer-led tabletop?

## 8. AI-specific

- Defenses against prompt injection (direct and indirect / data-source).
- Output handling controls for code execution, link rendering, file writes.
- Model supply chain: provenance of base / fine-tuned models, mechanisms against poisoning.
- Vector / embedding security: who can read indexes; how authorization is enforced at retrieval time.

## 9. Vendor logging gap acknowledgement

If any of sections 4 / 5 / 8 cannot be answered concretely, the gap is recorded as a residual risk in the AI Risk Register and routed to the business owner for explicit acceptance, redesign, or rejection.
