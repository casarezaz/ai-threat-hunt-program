# H-XXX — `<short hunt name>`

| Field | Value |
|-------|-------|
| Hunt ID | H-XXX |
| D-Control step(s) | Detect / ... |
| Asset class(es) | e.g., SaaS LLM, IDE agent |
| OWASP LLM / Agentic AI | e.g., LLM02 Sensitive Information Disclosure |
| MITRE ATLAS | e.g., AML.T0024 (Exfiltration via inference) |
| Owner | `<name>` |
| Cadence | One-time / Weekly / Monthly / Continuous |

## Hypothesis

State the abnormal behavior in one sentence. *Example:* Users are uploading source code, customer data, or secrets into unsanctioned SaaS LLMs through the browser.

## Why this matters

Plain-language risk statement for an exec / business owner reader.

## Data sources

- ...
- ...

## Query / detection logic

```text
(pseudocode or SIEM query)
```

## Expected normal vs. abnormal

- **Normal:** ...
- **Abnormal:** ...

## Evidence to capture

- Identity (user, device, IP)
- Asset (AI service, app, agent, RAG index)
- Action (read / write / send / publish / approve / deploy / delete)
- Data (classification + lineage where possible)
- Time + business context

## Findings (filled in per run)

- ...

## Control gaps (filled in per run)

- ...

## Decision (filled in per run)

> Allow / Limit / Monitor / Redesign / Pause / Replace / Terminate — `<reason>` — `<owner>` — review by `<date>`.
