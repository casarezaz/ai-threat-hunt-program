# Decision-Grade Evidence Package — `<finding short title>`

> Use this template for every material AI threat hunt finding. Small enough for leadership to read; precise enough for analysts to defend. See [Paper 4 §8](../docs/papers/paper-4-d-evidence.md#8-the-decision-grade-evidence-package).

| Field | Value |
|-------|-------|
| Finding ID | EVID-`<YYYY>-<NNN>` |
| Date opened | `<YYYY-MM-DD>` |
| Originating hunt(s) | e.g., H-002, RAG-007 |
| Asset / process | `<system, data flow, business process, user group>` |
| Regulatory boundary | e.g., GDPR / HIPAA / PCI / CUI / none |
| Owner (named) | `<person>` |
| Risk decision required by | `<YYYY-MM-DD>` |

## 1. One-sentence finding

> *What happened or what could not be proven.*

## 2. Affected asset / process

- **System / asset:**
- **Data flow:**
- **Business process:**
- **User group / customer impact path:**
- **Regulatory or contractual boundary:**

## 3. Evidence chain (the seven domains)

| Domain | Evidence captured | Source | Gap (if any) |
|--------|-------------------|--------|--------------|
| Identity | | | |
| Intent / Trigger | | | |
| Action | | | |
| Data | | | |
| Control | | | |
| State | | | |
| Time | | | |

If any row's "Evidence captured" column is blank, the **Gap** column must be populated and a corresponding evidence-gap finding filed (see §6).

## 4. Control assessment

Pick one. Justify in one sentence.

- [ ] Passed
- [ ] Failed
- [ ] Bypassed
- [ ] Partially effective
- [ ] Not observable
- [ ] Not applicable

**Justification:**

## 5. Risk decision required

Pick one. Reference the residual risk and any compensating controls.

- [ ] Accept
- [ ] Avoid
- [ ] Mitigate
- [ ] Transfer

**Decision owner:**
**Decision date:**
**Justification:**
**Review date:**

## 6. Evidence-gap findings filed

For each blank row in §3, file an evidence-gap finding:

| Gap | Owner | Target maturity | Quarter due |
|-----|-------|-----------------|-------------|

These feed the program's instrumentation backlog and are reviewed each quarter against the [maturity self-assessment](d-evidence-maturity.md).

## 7. Validation method

How will the program prove the finding is closed?

- [ ] Re-hunt query (specify hunt ID and expected null result)
- [ ] Control test (specify test plan)
- [ ] Tabletop exercise
- [ ] Access review
- [ ] Log export verification
- [ ] Independent evidence check (named third party / internal audit)

**Re-validation date:**

## 8. Linked records

- AI Asset Register entry: `<asset_id>`
- AI Risk Register entry: `<row reference>`
- Decision Log entry: `<row reference>`
- Exception Register entry (if applicable): `<row reference>`
- Containment playbook(s) invoked: `<L1..L7 / C-RAG-1..5>`
- Hunt report(s): `<paths under hunts/reports/>`
