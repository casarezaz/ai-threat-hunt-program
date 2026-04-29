# H-006 — IDE / CLI agent secret exposure

| Field | Value |
|-------|-------|
| Hunt ID | H-006 |
| D-Control step(s) | Detect, Defend |
| Asset class(es) | IDE / CLI coding agents |
| OWASP LLM / Agentic AI | LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling |
| MITRE ATLAS | AML.T0024 — Exfiltration via Inference (with prompt context) |
| Owner | _to assign_ |
| Cadence | Continuous |

## Hypothesis

Generated code, commits, shell commands, logs, or prompts produced by IDE/CLI agents contain credentials, tokens, private keys, or internal endpoint details.

## Why this matters

Coding agents see source, environment files, and shell history. They can also generate code that hardcodes secrets, exposes endpoints, or downgrades crypto. Their outputs land in repos and prod.

## Data sources

- Pre-commit / pre-receive secret scanners (gitleaks, trufflehog, custom)
- IDE plugin telemetry (where available)
- Shell history (where lawful and in scope)
- CI/CD logs
- Prompt/session logs from sanctioned coding-agent gateways

## Query / detection logic

```text
secret_scan.match in {aws_access_key, gcp_sa_key, slack_token, github_pat, openai_key, anthropic_key, ssh_private_key, jwt}
  AND source in {agent_generated_code, agent_session_log, ide_paste_buffer}
```

## Expected normal vs. abnormal

- **Normal:** Agent code uses environment variables / secret managers; no plaintext credentials in commits.
- **Abnormal:** Agent suggests code with hardcoded keys; agent paste history contains live credentials; agent commits include `.env` files.

## Evidence to capture

- Repo, branch, commit, file path
- Secret type (no plaintext value in evidence)
- Author identity + agent identity
- Whether the secret is live (rotate immediately if so)

## Findings / Control gaps / Decision

_(filled in per run)_
