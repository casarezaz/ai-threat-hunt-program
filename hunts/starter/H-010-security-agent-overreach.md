# H-010 — Security-agent overreach

| Field | Value |
|-------|-------|
| Hunt ID | H-010 |
| D-Control step(s) | Detect, Defend, Document |
| Asset class(es) | Security operations agents (AI in SIEM/SOAR/EDR/case mgmt) |
| OWASP LLM / Agentic AI | LLM06 Excessive Agency, LLM05 Improper Output Handling |
| MITRE ATLAS | AML.T0049 — Exploit Public-Facing Application (analog: agent gating SOC) |
| Owner | _to assign_ |
| Cadence | Weekly |

## Hypothesis

AI-driven security tooling is generating, suppressing, closing, or modifying detections, cases, or containment actions in unsafe ways.

## Why this matters

If the AI is the SOC, the AI also becomes the insider risk. Auto-suppression of alerts, premature case closure, or rule changes at scale can blind the program.

## Data sources

- SIEM rule change history
- SOAR action history (containment, suppression, ticketing)
- Case management (open/close, severity changes)
- EDR policy changes

## Query / detection logic

```text
action in {rule_change, suppression_create, case_close, severity_downgrade, containment_revert}
  AND actor in ai_agents
  AND ( volume_per_hour > p95(baseline)
        OR target_severity in {High, Critical}
        OR no_human_review_recorded )
```

## Expected normal vs. abnormal

- **Normal:** AI summarizes, drafts, and recommends — humans approve high-impact changes.
- **Abnormal:** AI closing High/Critical cases at scale; AI broadly suppressing rules; AI reverting containment actions.

## Evidence to capture

- Action, actor (agent ID), target rule/case
- Pre/post state
- Whether a human reviewed
- Linked detections that may have been impacted

## Findings / Control gaps / Decision

_(filled in per run)_
