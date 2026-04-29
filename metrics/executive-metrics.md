# Executive Metrics for an AI Threat Hunt Program

> Executives do not need token-level noise. They need decision-grade metrics.

Each metric below has a definition, data source, target, cadence, and formula. They roll up into the [`executive-risk-brief.md`](../templates/executive-risk-brief.md) template.

## Discovery metrics

### Percent of AI assets discovered and classified
- **Definition:** Of all AI in use, how many are inventoried *and* classified by class, data, identity, capability.
- **Data source:** AI Asset Register vs. independent discovery passes (CASB / SSE, OAuth grants, browser extensions, procurement).
- **Target:** ≥ 95% within 90 days of program start.
- **Cadence:** Monthly.
- **Formula:** `count(classified_assets) / count(discovered_assets) * 100`.

### Percent of AI assets with named owners
- **Definition:** Each asset has an accountable individual (not a team).
- **Data source:** AI Asset Register `owner` field.
- **Target:** 100%.
- **Cadence:** Monthly.

### Percent of AI assets with defined data classification
- **Definition:** Each asset has its data sensitivity recorded (Public / Internal / Confidential / Regulated).
- **Data source:** AI Asset Register `data_classification` field.
- **Target:** 100%.
- **Cadence:** Monthly.

## Telemetry and detection metrics

### Percent of high-risk AI assets with usable telemetry
- **Definition:** Of assets rated High or Critical residual risk, how many produce the minimum-viable telemetry from the [Telemetry Requirements Matrix](../templates/telemetry-requirements-matrix.csv).
- **Data source:** Telemetry Requirements Matrix.
- **Target:** 100% within 90 days of high-risk classification.
- **Cadence:** Monthly.

### Number of AI systems with write/action capability
- **Definition:** Count of inventoried assets that can write, send, deploy, transact, publish, delete, approve, or modify security controls.
- **Data source:** AI Asset Register capabilities columns.
- **Target:** Tracked over time; not a target — a population.
- **Cadence:** Monthly.

### Number of AI systems with excessive OAuth scopes
- **Definition:** AI applications holding write-level scopes against mail / drive / calendar / chat / ticketing / CRM that exceed business need.
- **Data source:** Hunt H-002 output.
- **Target:** Trend toward zero.
- **Cadence:** Weekly.

### Number of unsanctioned AI services used in the environment
- **Definition:** Distinct AI services discovered that are not on the sanctioned list.
- **Data source:** Hunt H-001 output.
- **Target:** Trend toward zero (for high/critical-data exposure cases); steady state acceptable for low-risk research tools under monitor mode.
- **Cadence:** Weekly.

## Exposure metrics

### Sensitive-data exposure events involving AI
- **Definition:** Count of confirmed events where regulated, confidential, IP, customer, or employee data flowed into AI.
- **Data source:** Hunt H-003 output, DLP events with AI destination categories.
- **Target:** Trend down; zero for confirmed regulated-data flows to unsanctioned AI.
- **Cadence:** Weekly (raw), Monthly (rollup).

### High-risk agent actions blocked, approved, or contained
- **Definition:** Count of high-impact agent actions broken down by outcome (blocked / approved with human / contained / executed).
- **Data source:** Workflow + SOAR + LLM gateway logs.
- **Target:** > 80% of high-impact actions have a recorded human approval or block.
- **Cadence:** Monthly.

## Speed metrics

### Mean time to discover new AI use
- **Definition:** Days from first observation in any source-of-truth (SSO, CASB, browser, endpoint, OAuth grant) to entry in the AI Asset Register.
- **Data source:** First-seen timestamp diff vs. asset register `first_seen`.
- **Target:** ≤ 7 days for high-risk classes; ≤ 30 days for others.
- **Cadence:** Monthly.

### Mean time to revoke or degrade AI capability
- **Definition:** Time from decision-to-act to capability change in production (revoke OAuth, disable connector, switch to L4 degrade, etc.).
- **Data source:** Decision log + change tickets + SOAR action timestamps.
- **Target:** ≤ 24 hours for active incidents; ≤ 5 business days for routine reductions.
- **Cadence:** Monthly.

## Containment and decision metrics

### Percent of AI assets with documented containment playbooks
- **Definition:** Each asset has at least L1–L3 documented and one tested in the last quarter.
- **Data source:** `playbooks/containment/` + test records.
- **Target:** 100% for High / Critical residual risk.
- **Cadence:** Quarterly.

### Residual risk trend for top AI systems
- **Definition:** Quarter-over-quarter residual risk for the top 5 / top 10 inventoried assets.
- **Data source:** AI Risk Register.
- **Target:** Trend down or stable; rising trend triggers an executive narrative.
- **Cadence:** Quarterly.

### Number of vendor logging gaps accepted by leadership
- **Definition:** Distinct vendor / capability combinations where the org has formally accepted that telemetry will be insufficient.
- **Data source:** Exception register + Vendor Due Diligence notes.
- **Target:** Tracked, not minimized — visibility into where the org is choosing to fly blind.
- **Cadence:** Quarterly.

## How to brief these

The executive message stays crisp:

> Where AI has agency, security needs control. We can prove what we can see, deny, and contain. The metrics show where we cannot.
