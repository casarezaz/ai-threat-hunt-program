# H-003 — Sensitive-data prompt exposure

| Field | Value |
|-------|-------|
| Hunt ID | H-003 |
| D-Control step(s) | Detect, Deny |
| Asset class(es) | SaaS LLM, embedded copilots, IDE agents |
| OWASP LLM / Agentic AI | LLM02 Sensitive Information Disclosure |
| MITRE ATLAS | AML.T0024 — Exfiltration via Inference |
| Owner | _to assign_ |
| Cadence | Continuous |

## Hypothesis

Users are pasting or uploading secrets, source code, customer data, employee data, regulated data, incident details, or confidential business records into AI tools.

## Why this matters

This is the most direct AI-to-data-loss path. It maps cleanly to existing DLP pipelines but the AI destination categories must exist in policy.

## Data sources

- DLP (endpoint paste / upload, network, email, SaaS)
- LLM gateway logs
- Browser-agent / extension telemetry
- IDE plugin logs (Copilot-style)

## Query / detection logic

```text
dlp.match.category in {pii, phi, pci, secret, source_code, internal_doc}
  AND destination.category in {ai_chat, ai_coding_assistant, ai_browser_agent, ai_rag}
```

## Expected normal vs. abnormal

- **Normal:** Sanctioned AI tools with content controls + DLP classification on egress.
- **Abnormal:** Customer PII into a consumer chatbot; private repo code into an unsanctioned coding assistant; incident timelines pasted into a public LLM.

## Evidence to capture

- User, device, AI destination
- Data classification + sample (redacted)
- Channel (paste, upload, API call, IDE)
- Outcome (allowed, blocked, allowed-with-warning)

## Findings / Control gaps / Decision

_(filled in per run)_
