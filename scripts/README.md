# Scripts

Operational tooling for the D-Control loop. The first wave focuses on **Discover**: finding the AI attack surface across code, environment configuration, and OAuth grants.

## What's here

| Path | Step | Purpose |
|------|------|---------|
| `asset-inventory/scan_repo_for_ai.py` | Discover | Walk a Git repo (or any directory) and surface LLM SDK usage, MCP servers, prompt files, vector store config, and AI-provider API keys. |
| `asset-inventory/scan_env_for_ai.py` | Discover | Scan `.env`, `.envrc`, shell rc files, JSON / YAML configs for AI provider references and exposed keys. |
| `asset-inventory/oauth_grants_to_inventory.py` | Discover | Normalize an OAuth-grants export (Workspace, M365, Slack, etc.) into AI Asset Register rows. |
| `asset-inventory/merge_inventory.py` | Discover | Merge multiple discovery passes into a deduplicated AI Asset Register. |
| `lib/ai_signatures.py` | shared | The authoritative pattern catalog: SDK imports, model API hostnames, env vars, MCP server hints, vector store SDKs, AI-provider key formats. |
| `lib/inventory.py` | shared | Helpers for emitting Asset Register CSV / JSON aligned to `templates/ai-asset-schema.json`. |

## Conventions

- **Pure stdlib.** No third-party Python. Defenders should be able to drop these on a workstation, jump host, or hardened build agent without `pip install`.
- **Read-only.** Scripts never write outside their output directory.
- **Outputs land in `--out`** as both CSV (Asset Register format) and a JSON sidecar with full match metadata (file, line, snippet).
- **Secrets are flagged, not exfiltrated.** When a script flags a key, it stores the file path, line, and key *type* — not the key value. (You will see `[REDACTED]` in the output.)
- **Exit codes:** `0` success, `1` usage error, `2` partial scan with errors. The number of findings is *not* an exit signal — empty output is a valid result.

## Quick start

```bash
# scan a repo
python3 scripts/asset-inventory/scan_repo_for_ai.py /path/to/repo --out scan-output/

# scan environment / config files
python3 scripts/asset-inventory/scan_env_for_ai.py ~/path/to/configs --out scan-output/

# turn an OAuth export into asset rows (CSV in, CSV out)
python3 scripts/asset-inventory/oauth_grants_to_inventory.py --in oauth_export.csv --out scan-output/oauth_assets.csv

# merge everything into one register
python3 scripts/asset-inventory/merge_inventory.py scan-output/*.csv --out templates/ai-asset-register.csv
```

All scripts support `--help`.

## What "discover" produces here

Each script emits rows that conform to [`templates/ai-asset-schema.json`](../templates/ai-asset-schema.json). The required fields (`asset_id`, `name`, `asset_class`, `owner`, `data_classification`, `identity_context`) are filled in to the extent the source allows; unknown fields are blank rather than guessed. The Define step fills in the rest.

## Roadmap

The next script tracks (already in the program backlog):

- **Telemetry parsers** — LLM gateway / agent log parsers; sigma-style detection rule packs.
- **Hunt runner** — YAML-driven hunt hypothesis runner against CSV / Splunk / Elastic.
- **ATLAS / OWASP mappers** — CLI to map detections and incidents to MITRE ATLAS techniques and OWASP LLM Top 10.

These ship after the asset-inventory track is in operational use.
