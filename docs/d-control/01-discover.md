# Step 1 — Discover

**Objective:** Find the AI attack surface before it finds the organization.

## Key actions

- Inventory sanctioned and unsanctioned AI usage across SaaS, cloud, endpoint, browser, developer, messaging, ticketing, and workflow platforms.
- Identify AI embedded inside existing products, not only obvious standalone chat tools.
- Collect owners, business processes, vendors, tenants, models, connectors, API keys, OAuth grants, and data sources.

## Artifacts and telemetry

- SSO and IdP application lists
- CASB / SSE and SWG logs
- Browser history and extension inventories
- SaaS audit logs
- Cloud service inventory
- Endpoint process and network telemetry
- Git and CI/CD secrets scans
- Procurement and expense data

## Hunt pivots

- New AI domain accessed by multiple users in the last 30 days
- OAuth grant to AI application with file / email / calendar scope
- Developer workstation connecting to unapproved model API
- Browser extension using AI with broad page-read permissions

## Outputs

- New or updated entries in the **AI Asset Register** (`templates/ai-asset-register.csv`)
- Source-of-record snapshot saved to the run folder (date-stamped)
- Discovery gaps logged to the **Telemetry Requirements Matrix** with an owner

## Tooling in this repo

- [`scripts/asset-inventory/scan_repo_for_ai.py`](../../scripts/asset-inventory/scan_repo_for_ai.py) — scan a Git repository for LLM SDK usage, MCP servers, prompt files, vector store config, and AI-provider keys.
- [`scripts/asset-inventory/scan_env_for_ai.py`](../../scripts/asset-inventory/scan_env_for_ai.py) — scan environment / config / dotenv files for AI provider references and exposed keys.
- [`scripts/asset-inventory/oauth_grants_to_inventory.py`](../../scripts/asset-inventory/oauth_grants_to_inventory.py) — normalize an OAuth-grants export into asset-register rows.
- [`scripts/asset-inventory/merge_inventory.py`](../../scripts/asset-inventory/merge_inventory.py) — merge multiple discovery passes into a single deduped register.

## Exit criteria for this step

You may move on to **Define** when:

1. Every discovery source above has been queried at least once in the last cadence window.
2. Every discovered asset has at least an asset-class label and a candidate owner.
3. Discovery gaps are logged, not ignored.
