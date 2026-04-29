# H-001 — Shadow AI discovery

| Field | Value |
|-------|-------|
| Hunt ID | H-001 |
| D-Control step(s) | Discover, Detect |
| Asset class(es) | SaaS LLM, embedded copilots, browser-agent extensions |
| OWASP LLM / Agentic AI | LLM02 Sensitive Information Disclosure (downstream) |
| MITRE ATLAS | Reconnaissance / Resource access (general) |
| Owner | _to assign_ |
| Cadence | Weekly |

## Hypothesis

Users and devices are accessing AI services that the organization has not sanctioned, classified, or instrumented.

## Why this matters

Unknown AI usage = unknown blast radius. Sensitive data, credentials, and IP can leave the environment through tools that no policy or detection covers. This is the floor of every other hunt: you cannot detect, deny, or contain what you have not discovered.

## Data sources

- SSO / IdP application list
- CASB / SSE / SWG categorized AI domains
- DNS and proxy logs
- Browser extension inventory (managed browser or MDM)
- Endpoint network telemetry (EDR)
- OAuth grant logs

## Query / detection logic

```text
domain in known_ai_domains_list
  AND distinct_users(domain) >= 3
  AND first_seen(domain) within last 30 days
  AND domain NOT IN sanctioned_ai_apps
```

## Expected normal vs. abnormal

- **Normal:** Sanctioned AI services with established baselines.
- **Abnormal:** New AI domain accessed by multiple users in last 30 days; AI domain spike on an unmanaged endpoint; AI domain reached via a non-corporate browser profile.

## Evidence to capture

- User, device, IP, time
- AI service / vendor / domain
- OAuth scope (if any)
- Data signal (DLP triggers, file uploads, paste size)

## Findings / Control gaps / Decision

_(filled in per run — see hunts/template.md)_
