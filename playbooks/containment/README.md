# Graduated Containment Playbooks

D-Control rejects the binary of "allow everything" or "shut everything down." Containment runs on a seven-level ladder. Pick the lowest level that closes the gap.

| Level | Mode | One-line trigger |
|-------|------|------------------|
| [L1](L1-monitor.md) | Monitor | Risk suspected; visibility is the gap |
| [L2](L2-limit.md) | Limit | A specific data, scope, or action class is unsafe |
| [L3](L3-approval-gate.md) | Approval Gate | High-impact action class; humans should be in the loop |
| [L4](L4-degrade.md) | Degrade | Confidence has dropped; reduce mode |
| [L5](L5-isolate.md) | Isolate | Compromise is plausible; cut blast radius |
| [L6](L6-suspend.md) | Suspend | Incident is active; pause |
| [L7](L7-terminate.md) | Terminate | Asset cannot be operated safely; remove |

Every playbook follows the same structure: **Trigger criteria, Owner, Pre-checks, Actions, Evidence to preserve, Communication, Reversal / next-step path.**

> Containment doctrine: *Can the organization reduce capability faster than the AI can expand blast radius?* If not, the asset is uncontained regardless of policy language.
