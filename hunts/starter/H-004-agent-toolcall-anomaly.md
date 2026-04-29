# H-004 — Agent tool-call anomaly

| Field | Value |
|-------|-------|
| Hunt ID | H-004 |
| D-Control step(s) | Detect, Degrade |
| Asset class(es) | Enterprise agent, custom/internal agent, IDE/CLI agent |
| OWASP LLM / Agentic AI | LLM06 Excessive Agency, Agentic AI ATA-007 Goal manipulation |
| MITRE ATLAS | AML.T0050 — Command and Scripting Interpreter (analogous tool exec) |
| Owner | _to assign_ |
| Cadence | Continuous (alert) + Weekly (review) |

## Hypothesis

An agent is making tool calls that are unusual in volume, type, time, or failure pattern — a signal of misuse, prompt injection, or runaway autonomy.

## Why this matters

Tool calls are the agent's physical actions. Anomalous tool calls are how a benign agent becomes a compromised insider.

## Data sources

- LLM / agent gateway logs (tool invocation)
- API gateway logs
- SaaS audit logs for the systems the agent touches
- Token / billing telemetry (volume signal)

## Query / detection logic

```text
tool_calls_per_session > p99(baseline_per_agent)
  OR tool_in_call NOT IN agent.allowed_tools
  OR call_time outside agent.business_hours
  OR tool_call.failure_rate > p95(baseline)
```

## Expected normal vs. abnormal

- **Normal:** Bounded session length, allowed-tool list, predictable failure rate.
- **Abnormal:** New tool used for the first time; sustained off-hours execution; loops of failed calls (often a sign of prompt injection / goal hijack).

## Evidence to capture

- Agent identity, session ID
- Sequence of tool calls
- User context (was a human in the loop?)
- Triggering prompt(s) and any retrieved context

## Findings / Control gaps / Decision

_(filled in per run)_
