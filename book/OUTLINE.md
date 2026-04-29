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

## Part III — Asset Classes Covered by D-Control

| Ch | Asset class | Anchor hunt(s) |
|----|-------------|----------------|
| 12 | SaaS LLMs (browser-driven) | H-001, H-003 |
| 13 | Embedded copilots | H-002, H-008 |
| 14 | Enterprise agents | H-004 |
| 15 | Custom / internal agents | H-004, H-009 |
| 16 | IDE / CLI coding agents | H-006 |
| 17 | Browser / computer-use agents | H-005 |
| 18 | RAG systems and vector databases | H-007 |
| 19 | Model APIs and AI gateways | H-009 |
| 20 | Workflow / RPA agents | H-008 |
| 21 | Customer-facing AI agents | _new chapter_ |
| 22 | Security operations agents | H-010 |

## Part IV — Operating the Program

| Ch | Title | Source artifact |
|----|-------|-----------------|
| 23 | Telemetry that actually answers questions | `templates/telemetry-requirements-matrix.csv` |
| 24 | Risk scoring without theater | `templates/ai-risk-register.csv` |
| 25 | Graduated containment | `playbooks/containment/` |
| 26 | Vendor due diligence | `templates/vendor-due-diligence.md` |
| 27 | Executive metrics and the board narrative | `metrics/executive-metrics.md`, `templates/executive-risk-brief.md` |
| 28 | Cadence and event-driven re-trigger | `templates/operating-cadence.md` |

## Part V — Going Deeper

Future-paper hooks (each can spin off as a paper before becoming a chapter):

- Paper 3 candidate: **AI-Specific Detection Engineering Patterns** (queries, sigma-style rules, gateway parsers).
- Paper 4 candidate: **Browser and Computer-Use Agents in the Enterprise** (deep dive on session-bound agents).
- Paper 5 candidate: **RAG and Vector-Layer Security** (authorization at retrieval time, lineage, poisoning).
- Paper 6 candidate: **Vendor Logging Gaps as a Leadership Decision** (turning the residual-risk argument into procurement leverage).
- Paper 7 candidate: **Tabletop Exercises for AI Incidents** (scenarios, scoring, lessons).

## Process

1. Each chapter is drafted from its source artifact. The repo is the canonical version; the chapter is the long-form expansion.
2. Updates flow chapter ← repo, never repo ← chapter. The repo is the running program; the book documents it.
3. New papers go into `docs/papers/` first, then become chapters.
