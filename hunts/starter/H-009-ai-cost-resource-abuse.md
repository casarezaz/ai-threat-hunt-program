# H-009 — AI cost and resource abuse

| Field | Value |
|-------|-------|
| Hunt ID | H-009 |
| D-Control step(s) | Detect, Degrade |
| Asset class(es) | Model APIs, AI gateways, RAG ingestion pipelines |
| OWASP LLM / Agentic AI | LLM10 Unbounded Consumption ("denial of wallet") |
| MITRE ATLAS | AML.T0034 — Cost Harvesting |
| Owner | _to assign_ |
| Cadence | Daily (alert) + Weekly (review) |

## Hypothesis

Model / API usage is spiking abnormally — token volume, embedding jobs, or request rate — consistent with abuse, runaway agent loops, or denial-of-wallet.

## Why this matters

Cost is a security signal. Abnormal spend is often the first detectable symptom of compromise, prompt-injection loops, or stolen API keys.

## Data sources

- Model provider billing exports
- LLM gateway request logs
- Cloud bill / cost-anomaly detection
- Vector DB / embedding pipeline run history

## Query / detection logic

```text
tokens_per_hour > p99(baseline_per_owner)
  OR cost_per_day > 2 * 7d_avg
  OR new_api_key.first_use.region NOT IN expected_regions
  OR embedding_job.input_size > p99(baseline)
```

## Expected normal vs. abnormal

- **Normal:** Predictable per-team spend; embedding jobs run on schedule with bounded input.
- **Abnormal:** Sudden spend spike; new key / new region; embedding pipeline ingesting unexpected sources.

## Evidence to capture

- API key, owner team, region
- Time series of usage
- Recent agent / pipeline changes
- Error / retry rate

## Findings / Control gaps / Decision

_(filled in per run)_
