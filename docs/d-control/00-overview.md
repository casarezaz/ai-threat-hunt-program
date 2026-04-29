# D-Control: The Signature Loop

> **Doctrine:** If AI has access, agency, or influence, it needs D-Control.

D-Control is a defensive operating loop for AI threat hunting and operational security. It converts AI governance from an abstract review process into repeatable outputs: discovered assets, defined capabilities, detection logic, denial controls, defensive hardening, containment options, evidence, and executive decisions.

The loop runs continuously across every AI asset class:

1. [**Discover**](01-discover.md) — Find the AI system or AI-enabled workflow.
2. [**Define**](02-define.md) — Classify what it is, what it can access, and what it can do.
3. [**Detect**](03-detect.md) — Build visibility, logging, alerts, and hunt hypotheses.
4. [**Deny**](04-deny.md) — Block unsafe access, action, and data movement.
5. [**Defend**](05-defend.md) — Harden the identity, data, workflow, model, and integration surfaces.
6. [**Degrade / Contain**](06-degrade-contain.md) — Reduce or isolate capability when risk rises.
7. [**Document**](07-document.md) — Preserve evidence, decisions, residual risk, and control gaps.
8. [**Decide**](08-decide.md) — Force an explicit business/security decision: allow, limit, monitor, redesign, pause, replace, or terminate.

Every AI system should be able to survive this loop. If it cannot, the issue is not AI maturity — it is operational exposure.

## Why a loop, not a checklist

AI systems change faster than annual governance can keep up with. New tools appear in browser histories, OAuth consent logs, SSO apps, SaaS audit trails, procurement records, developer workstations, Git repositories, notebooks, workflow platforms, and ticketing systems. New integrations quietly expand capability. New prompts expose sensitive data. New agents add write action where only read action was expected.

D-Control runs on a cadence that matches AI change velocity (see [`operating-cadence.md`](../../templates/operating-cadence.md)) and re-triggers automatically whenever an AI asset gains a new connector, model, data source, action capability, vendor subprocessor, privileged role, or customer-facing workflow.

## How D-Control aligns with existing frameworks

D-Control does not replace NIST AI RMF, OWASP LLM / Agentic AI, MITRE ATLAS, CSA AI Controls Matrix, Google SAIF, or NCSC/CISA/NSA secure AI lifecycle guidance. It operationalizes them.

A framework can tell the organization what *should* matter. D-Control asks whether the *evidence* exists.

## Outputs every loop must produce

| Step | Required output |
|------|-----------------|
| Discover | A new or updated entry in the AI Asset Register |
| Define | A capability/agency rating and identity/data mapping |
| Detect | Telemetry confirmed and at least one hunt hypothesis recorded |
| Deny | A denial control implemented or an exception with expiration |
| Defend | A hardening change or a documented compensating control |
| Degrade/Contain | A graduated containment playbook tested or updated |
| Document | Risk register entry, hunt report, or exception record |
| Decide | A dated business decision: allow, limit, monitor, redesign, pause, replace, or terminate |

If a loop cycle does not produce these outputs, the program is doing governance theater.

## Reading order

1. Start with this overview.
2. Read [Paper 2](../papers/paper-2-d-control.md) for the full doctrine and rationale.
3. Use the per-step pages (`01-discover.md` … `08-decide.md`) when running the loop on a real asset class.
4. Use the [hunts/](../../hunts/) catalog for the starter backlog and the [playbooks/containment/](../../playbooks/containment/) directory for graduated response.
