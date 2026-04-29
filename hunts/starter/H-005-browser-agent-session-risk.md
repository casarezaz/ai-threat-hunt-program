# H-005 — Browser-agent session risk

| Field | Value |
|-------|-------|
| Hunt ID | H-005 |
| D-Control step(s) | Discover, Detect, Deny |
| Asset class(es) | Browser / computer-use agents |
| OWASP LLM / Agentic AI | LLM06 Excessive Agency, Agentic AI ATA-001 Memory poisoning, ATA-006 Identity spoofing |
| MITRE ATLAS | AML.T0051 — LLM Prompt Injection |
| Owner | _to assign_ |
| Cadence | Continuous |

## Hypothesis

Browser or computer-use agents are operating inside authenticated enterprise sessions — banking, admin consoles, identity providers, source control — where prompt injection or page-content manipulation can drive unintended actions.

## Why this matters

A browser agent inherits the session's authority. The user trusts the page; the agent trusts the page; the page is the threat.

## Data sources

- Browser extension inventory (managed browsers / MDM)
- Browser activity / history
- Identity provider (re-auth, MFA, session events)
- SaaS audit logs for actions performed during the agent session
- Endpoint EDR (process tree, automation drivers)

## Query / detection logic

```text
session.user_agent matches known_browser_agent_signatures
  AND session.scope intersects {admin_console, idp, source_control, finance, hr}
  AND (write_actions_count > 0 OR script_injection_detected)
```

## Expected normal vs. abnormal

- **Normal:** Browser agents pinned to read-only research workflows in unprivileged tabs; no write actions in privileged scopes.
- **Abnormal:** Agent driving an admin console; agent submitting forms in identity / finance / HR systems; pages with hidden / off-screen text influencing agent behavior.

## Evidence to capture

- Agent extension/process, version
- Tab URL, page DOM snapshot if possible
- Sequence of actions (clicks, form submissions)
- Identity context and session age

## Findings / Control gaps / Decision

_(filled in per run)_
