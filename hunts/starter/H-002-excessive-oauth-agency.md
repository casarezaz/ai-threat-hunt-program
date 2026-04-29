# H-002 — Excessive OAuth agency

| Field | Value |
|-------|-------|
| Hunt ID | H-002 |
| D-Control step(s) | Discover, Define, Deny |
| Asset class(es) | SaaS LLM, enterprise agent, embedded copilot |
| OWASP LLM / Agentic AI | LLM06 Excessive Agency, LLM08 Vector and Embedding Weaknesses (downstream) |
| MITRE ATLAS | AML.T0044 — Full ML Model Access (analogous: full tenant access) |
| Owner | _to assign_ |
| Cadence | Weekly |

## Hypothesis

AI applications hold OAuth grants that exceed business need — read/write access to mail, drive, calendar, ticketing, CRM, or messaging data.

## Why this matters

OAuth scopes are the action surface. An AI app with `mail.send`, `files.write`, or `chat.write` can move data, send messages, or modify records on behalf of a user. Most orgs grant once and forget.

## Data sources

- Workspace / Microsoft 365 OAuth audit
- IdP enterprise application consent logs
- SaaS app (Slack, Salesforce, Jira, HubSpot, etc.) installed-app exports
- DLP and audit logs for actions taken by app principals

## Query / detection logic

```text
oauth_grant.scopes intersects {
  mail.send, mail.readwrite,
  files.write, drive.write,
  chat.write, channels.write,
  calendar.write,
  tickets.write, deals.write
}
AND grant.app NOT IN approved_ai_apps_with_named_owner
```

## Expected normal vs. abnormal

- **Normal:** Sanctioned AI apps with documented business justification + named owner.
- **Abnormal:** Mass-consent across a department; high-write-scope grants by individual users; new app gaining write scope after operating read-only.

## Evidence to capture

- App name, vendor, app ID, tenant
- Scopes granted
- Granting user(s), department, manager
- Last-used timestamp and action volume

## Findings / Control gaps / Decision

_(filled in per run)_
