# Hunt Catalog

Hunts in this repository follow the **D-Control** hunt convention: every hunt produces four outputs.

> **Findings. Evidence. Control gaps. Decision.**

If a hunt cannot produce all four, it is exploration, not a hunt.

## Layout

- `starter/` — the 10 starter hunts from Paper 2 (D-Control). Run these first when standing up a program.
- `reports/` — completed hunt reports. Naming: `<YYYY-MM-DD>-<asset-or-scope>-<hunt-id>.md`.
- `template.md` — the hunt template. Copy it when adding a new hunt.

## Hunt ID convention

`H-NNN` for the master backlog. Starter hunts use `H-001` through `H-010`. Asset-class-specific hunts can use a prefix (e.g., `BRW-001` for browser/computer-use agent hunts).

## Tagging

Each hunt should tag:

- **D-Control step(s)** it supports (Discover, Define, Detect, Deny, Defend, Degrade, Document, Decide).
- **OWASP LLM Top 10 / Agentic AI** category if applicable.
- **MITRE ATLAS** technique if applicable.
- **Asset class** from the D-Control asset class list.

## Decision template

Every hunt run ends with a one-line decision:

> Allow / Limit / Monitor / Redesign / Pause / Replace / Terminate — `<reason>` — `<owner>` — review by `<date>`.
