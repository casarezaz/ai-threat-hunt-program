# Templates

These are the operational artifacts the D-Control loop produces. They are intentionally lightweight: spreadsheets, markdown, JSON Schemas. Plug them into whatever GRC, ticketing, or SIEM tooling already exists.

| File | Purpose | D-Control step(s) |
|------|---------|-------------------|
| `ai-asset-register.csv` | The discovered AI inventory | Discover, Define |
| `ai-asset-schema.json` | JSON Schema for register rows (for tooling) | Discover, Define |
| `ai-risk-register.csv` | Inherent + residual risk per asset, with the D-Control formula | Define, Document |
| `telemetry-requirements-matrix.csv` | Required vs. actual telemetry per asset | Detect |
| `vendor-due-diligence.md` | Vendor questionnaire focused on AI operability | Define, Document |
| `executive-risk-brief.md` | Board / CISO-ready brief template | Document, Decide |
| `operating-cadence.md` | Daily / weekly / monthly / quarterly D-Control cadence | All |
| `decision-log.csv` | Dated decisions: allow / limit / monitor / redesign / pause / replace / terminate | Decide |
| `exception-register.csv` | Risk-accepted deviations with expirations | Deny, Document, Decide |
| `hunt-hypothesis.md` | Hunt hypothesis template (mirrors `hunts/template.md`) | Detect |
