# Step 7 — Document

**Objective:** Turn findings into defensible evidence and repeatable improvement.

## Key actions

- Document assets, owners, data flows, decisions, detections, exceptions, risk acceptance, incidents, and lessons learned.
- Keep records understandable to security, legal, privacy, audit, and executive stakeholders.
- Capture both the technical facts and the decision trail.

## Artifacts and telemetry

- AI risk register
- Hunt reports
- Exception register
- Control validation records
- Incident timelines
- Vendor due-diligence notes
- Executive risk memo
- Lessons-learned tracker

## Hunt pivots / illustrative findings

- "Hunt found 14 users accessing unsanctioned AI; 3 uploaded sensitive documents."
- "Vendor cannot provide prompt-level logging; residual risk accepted by business owner."
- "Agent changed ticket priority automatically; workflow redesigned with approval gate."

## What "good documentation" looks like

A D-Control governance record should include:

- AI asset name and owner
- Business use case and value statement
- Data classification and data flow
- Identity and permission model
- Capability and agency rating
- Required telemetry vs. actual telemetry
- Vendor logging and retention limits
- Detection coverage
- Denial controls
- Containment procedure
- Residual risk
- Approval, exception, or rejection decision
- Expiration date for review

If governance cannot answer what to detect, deny, defend, or contain, it is not governance — it is paperwork.

## Outputs

- An updated entry in `templates/ai-risk-register.csv`
- A hunt report under `hunts/reports/<date>-<asset>-<hunt-id>.md`
- A written exception (with owner + expiration) in `templates/exception-register.csv` if applicable
- A short note added to the lessons-learned tracker

## Exit criteria for this step

You may move on to **Decide** when:

1. The technical record and the decision record both exist.
2. Audit, legal, privacy, and the business owner can each find what they need.
3. The next review date is set.
