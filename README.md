# AI Threat Hunt Program

> **Doctrine:** *If AI has access, agency, or influence, it needs D-Control.*

This repository is the working version of the **AI-Securing Threat Hunt Program** — a blue-team operating model for finding, defining, detecting, denying, defending, containing, documenting, and deciding on the AI systems already running inside the enterprise.

It is also the source body of work for a planned field guide / book.

## Why this exists

AI security is split between two weak positions: AI as a magical productivity layer to adopt fast, and AI as a compliance problem to manage with policy language. Both are incomplete. AI is a connective layer — it can read documents, summarize messages, generate code, trigger workflows, call APIs, enrich tickets, triage incidents, interact with customers, and operate through authenticated user context.

This program treats AI as **operational security**, not paperwork.

> AI governance without threat hunting is paperwork.
> AI threat hunting without governance becomes chaos.

## What's in this repo

```
docs/
  papers/            Series papers (Paper 1: launch; Paper 2: D-Control; Paper 3: RAG; Paper 4: D-Evidence)
  d-control/         Per-step pages of the D-Control loop (Paper 2)
  d-evidence/        Per-domain pages of the D-Evidence proof model (Paper 4)
  launch/            LinkedIn launch post + share-bait phrases
  source/            Original .docx source documents
hunts/
  starter/           H-001..H-010 — the starter hunt backlog from Paper 2
  rag/               RAG-001..RAG-006 — RAG and vector-layer hunts from Paper 3
  template.md        Hunt template (every hunt produces findings/evidence/gaps/decision)
  reports/           Completed hunt reports (date-stamped per run)
playbooks/
  containment/       L1 Monitor → L7 Terminate graduated containment ladder
templates/
  ai-asset-register.csv
  ai-asset-schema.json
  ai-risk-register.csv
  telemetry-requirements-matrix.csv
  vendor-due-diligence.md
  executive-risk-brief.md
  operating-cadence.md
  decision-log.csv
  exception-register.csv
  hunt-hypothesis.md
  d-evidence-package.md       Decision-grade evidence package per material finding (Paper 4)
  d-evidence-maturity.md      Per-workflow self-assessment against the maturity model L0–L4 (Paper 4)
metrics/
  executive-metrics.md
scripts/
  asset-inventory/   Python tools for the Discover step (LLM/MCP/key/RAG discovery)
  lib/               Shared helpers
book/
  OUTLINE.md         Field guide outline mapping chapters to repo artifacts
```

## D-Control + D-Evidence in one paragraph

**D-Control** is a continuous loop, not an annual assessment: **Discover → Define → Detect → Deny → Defend → Degrade/Contain → Document → Decide.** Each step forces a measurable output. If an AI system cannot be discovered, it cannot be governed. If its capabilities are undefined, its blast radius is unknown. If telemetry is missing, abuse becomes invisible. If denial and containment paths do not exist, the organization is relying on hope instead of control.

**D-Evidence** pairs with D-Control as the proof layer: every D-Control question implies a D-Evidence follow-up. Where D-Control asks *"what should have constrained this behavior?"*, D-Evidence asks *"can we prove whether it did?"* Every concern must be traceable across **identity, intent, action, data, control, state, and time** — and a missing link is itself a risk finding.

Read [`docs/d-control/00-overview.md`](docs/d-control/00-overview.md) and [`docs/d-evidence/00-overview.md`](docs/d-evidence/00-overview.md) for the operating models, then [Paper 2](docs/papers/paper-2-d-control.md) and [Paper 4](docs/papers/paper-4-d-evidence.md) for the full doctrines.

## Quick start for a defender

1. Read the [D-Control overview](docs/d-control/00-overview.md).
2. Run a Discover pass against your codebase: `python3 scripts/asset-inventory/scan_repo_for_ai.py <path>`.
3. Drop discovered assets into [`templates/ai-asset-register.csv`](templates/ai-asset-register.csv).
4. Pick one starter hunt from [`hunts/starter/`](hunts/starter/) and run it against your existing telemetry.
5. Record the decision in [`templates/decision-log.csv`](templates/decision-log.csv).

That is the loop, in miniature.

## Frameworks this aligns with

NIST AI Risk Management Framework + GenAI Profile · OWASP Top 10 for LLM Applications · OWASP Agentic AI Threats and Mitigations · MITRE ATLAS · Cloud Security Alliance AI Controls Matrix · NCSC / CISA / NSA Guidelines for Secure AI System Development · Google Secure AI Framework (SAIF).

D-Control does not replace these frameworks. It operationalizes them. Each principle has to produce an operational artifact in this repository.

## Series papers

- [Paper 1 — Launch and Fast-Track](docs/papers/paper-1-launch.md)
- [Paper 2 — D-Control: The Signature Loop](docs/papers/paper-2-d-control.md)
- [Paper 3 — RAG and Vector-Layer Security](docs/papers/paper-3-rag-vector-security.md)
- [Paper 4 — D-Evidence: Turning D-Control Into Defensible Proof](docs/papers/paper-4-d-evidence.md)
- *Paper 5 onwards: see `book/OUTLINE.md` for candidate topics.*

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Small additions welcome: a new hunt hypothesis, a new asset class, a sharper containment step. Keep the tone practitioner-first and anti-theater.

## License

This repository is released under the [Apache License 2.0](LICENSE).
