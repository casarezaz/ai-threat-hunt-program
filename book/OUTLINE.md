# Field Guide Outline

Working titles (decide one before publishing):

- *AI-Securing Threat Hunting: A Blue-Team Field Guide for Defending AI Systems*
- *The AI Threat Hunt Field Guide: From Governance to Detection and Response*
- *Hunting the AI Attack Surface: Practical Threat Hunting for Agents, Prompts, RAG, and Model Supply Chains*
- *Beyond Prompt Injection: Building a Real AI Security Threat Hunt Program*

## Premise

Every chapter must produce something a defender can use this quarter. The book is the longer-form vehicle for the program; the repository is the working version.

## Part I — The Case for an AI Threat Hunt Program

| Ch | Title | Source artifact |
|----|-------|-----------------|
| 1 | Why governance alone fails | Paper 1 (`docs/papers/paper-1-launch.md`) |
| 2 | The AI attack surface, plainly | Paper 1 |
| 3 | What a threat hunt program owes the business | Paper 1 + new |

## Part II — D-Control: The Signature Loop

| Ch | Title | Source artifact |
|----|-------|-----------------|
| 4 | Discover | `docs/d-control/01-discover.md` |
| 5 | Define | `docs/d-control/02-define.md` |
| 6 | Detect | `docs/d-control/03-detect.md` |
| 7 | Deny | `docs/d-control/04-deny.md` |
| 8 | Defend | `docs/d-control/05-defend.md` |
| 9 | Degrade / Contain | `docs/d-control/06-degrade-contain.md` |
| 10 | Document | `docs/d-control/07-document.md` |
| 11 | Decide | `docs/d-control/08-decide.md` |

## Part III — D-Evidence: The Proof Layer

| Ch | Title | Source artifact |
|----|-------|-----------------|
| 12 | Why D-Evidence pairs with D-Control | Paper 4 §1–2 (`docs/papers/paper-4-d-evidence.md`) |
| 13 | The seven evidence domains | Paper 4 §4 + `docs/d-evidence/01-identity.md` … `07-time.md` |
| 14 | The D-Evidence signature loop | Paper 4 §5 |
| 15 | The decision-grade evidence package | Paper 4 §8 + `templates/d-evidence-package.md` |
| 16 | The D-Evidence maturity model | Paper 4 §9 + `templates/d-evidence-maturity.md` |
| 17 | Telemetry, gateways, and state versioning | Paper 4 §10 |
| 18 | The evidence repository | Paper 4 §11 |
| 19 | DFIR for AI-enabled environments | Paper 4 §13 |
| 20 | D-Evidence in audit, regulator, and customer notification | Paper 4 §14 |
| 21 | Anti-patterns and three voices | Paper 4 §15–16 |

## Part IV — Asset Classes Covered by D-Control

| Ch | Asset class | Anchor hunt(s) |
|----|-------------|----------------|
| 22 | SaaS LLMs (browser-driven) | H-001, H-003 |
| 23 | Embedded copilots | H-002, H-008 |
| 24 | Enterprise agents | H-004 |
| 25 | Custom / internal agents | H-004, H-009 |
| 26 | IDE / CLI coding agents | H-006 |
| 27 | Browser / computer-use agents | H-005 |
| 28 | RAG systems and vector databases | H-007, RAG-001..RAG-006 (Paper 3) |
| 29 | Model APIs and AI gateways | H-009 |
| 30 | Workflow / RPA agents | H-008 |
| 31 | Customer-facing AI agents | _new chapter_ |
| 32 | Security operations agents | H-010 |

## Part V — Operating the Program

| Ch | Title | Source artifact |
|----|-------|-----------------|
| 33 | Telemetry that actually answers questions | `templates/telemetry-requirements-matrix.csv` |
| 34 | Risk scoring without theater | `templates/ai-risk-register.csv` |
| 35 | Graduated containment | `playbooks/containment/` |
| 36 | Vendor due diligence | `templates/vendor-due-diligence.md` |
| 37 | Executive metrics and the board narrative | `metrics/executive-metrics.md`, `templates/executive-risk-brief.md` |
| 38 | Cadence and event-driven re-trigger | `templates/operating-cadence.md` |

## Part VI — Going Deeper

### Existing papers

- **[Paper 3 — RAG and Vector-Layer Security](../docs/papers/paper-3-rag-vector-security.md)** (authorization at retrieval time, lineage, embedding & index poisoning, indirect prompt injection in retrieved content, RAG-specific containment ladder C-RAG-1..5). Anchor hunts: `RAG-001`..`RAG-006`.
- **[Paper 4 — D-Evidence: Turning D-Control Into Defensible Proof](../docs/papers/paper-4-d-evidence.md)** (proof layer; seven evidence domains; decision-grade evidence package; maturity model L0–L4; gateway / correlation-ID / state-versioning patterns; evidence repository; DFIR for AI; audit and regulatory posture). Source for Part III.

### Candidate future papers

- Paper 5 candidate: **D-Decision** — converting findings into accountable executive action (the third leg of the operating triplet, named in Paper 4 §17).
- Paper 6 candidate: **AI-Specific Detection Engineering Patterns** (queries, sigma-style rules, gateway parsers).
- Paper 7 candidate: **Browser and Computer-Use Agents in the Enterprise** (deep dive on session-bound agents).
- Paper 8 candidate: **Vendor Logging Gaps as a Leadership Decision** (turning the residual-risk argument into procurement leverage).
- Paper 9 candidate: **Tabletop Exercises for AI Incidents** (scenarios, scoring, lessons).

## Process

1. Each chapter is drafted from its source artifact. The repo is the canonical version; the chapter is the long-form expansion.
2. Updates flow chapter ← repo, never repo ← chapter. The repo is the running program; the book documents it.
3. New papers go into `docs/papers/` first, then become chapters.
