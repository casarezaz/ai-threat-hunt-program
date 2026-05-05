# D-Evidence: Turning D-Control Into Defensible Proof

**Paper 4 in the AI Threat Hunting and Operational Security Series**

*Angie Agee, CISSP — Agee Cyber Advisory — May 2026*

---

## 1. Executive Intent

D-Evidence is the proof layer of the AI Threat Hunt Program. It converts control activity into evidence that can survive executive review, legal review, incident response, audit scrutiny, and post-incident lessons learned.

In traditional security operations, analysts often prove compromise through endpoint, network, identity, and cloud telemetry. In AI-enabled environments, that evidence model must expand. The system may not only move data; it may summarize it, transform it, retrieve it, approve it, send it, or trigger a downstream business process. If the organization cannot reconstruct that chain, it cannot confidently determine whether an AI-enabled workflow behaved as intended or became an attack path.

The purpose of this section is simple:

> **A control that cannot be evidenced is not a defensible control.**

It may reduce some operational risk, but it cannot reliably support incident response, regulatory inquiry, customer notification decisions, board reporting, or contractual accountability. Where D-Control answers *"what should have constrained this behavior?"*, D-Evidence answers *"can we prove whether it did?"* — and the program that can answer the second question is the program that survives an incident, an audit, a deposition, or a board.

D-Evidence is therefore not optional and not an analyst-side concern. It is the operational expression of accountability. It tells leadership which AI-enabled risks are bounded, which are believed to be bounded but are technically unprovable, and which are unbounded by design. Each of those is a different leadership conversation. Without D-Evidence, the conversation collapses into one indistinguishable category — *"we think it's fine."*

## 2. Why D-Evidence Comes After D-Control

D-Control defines the constraints. D-Evidence defines whether the constraints can be proven. The order matters because AI-enabled systems create a uniquely false sense of control when governance artifacts exist but telemetry does not.

A policy may say that agents cannot access sensitive records. The hunt must prove whether access was:

- **Technically impossible** (a hard control, evidenced by configuration + denial logs),
- **Merely discouraged** (a soft control with no enforcement signal),
- **Silently allowed** (no preventive control, no detective control, and therefore no evidence either way), or
- **Allowed through an inherited integration path** (the policy describes the front door; the agent walked in through an OAuth grant nobody mapped).

Only the first of those is a controlled state. The other three are indistinguishable to the program that has D-Control without D-Evidence. They look identical in a board deck. They behave very differently in an incident.

The pairing is the chapter's central argument. D-Control alone is governance theater dressed in operational clothing. D-Evidence alone is forensic curiosity that does not change the program. Together they form the spine of a defensible AI threat hunting program: D-Control defines the constraint; D-Evidence proves the constraint; the loop converts both into a leadership decision.

## 3. The D-Evidence Principle

> **D-Evidence principle:** Every AI-enabled security concern must be traceable across **identity, intent, action, data, control, state, and time**. If any link is missing, the organization should label that missing link as a risk finding, not as an analyst inconvenience.

This principle is the program's working definition of "evidenced." It applies whether the concern is a threat-intel-driven hunt, a regulator inquiry, an internal audit, a customer notification, an executive risk review, or a postmortem.

The seven evidence domains in the principle are not a checklist. They are a chain. A break in any single link has a specific operational meaning, and the program's response to a missing link is the *same* whether the link is missing for benign reasons (the vendor does not log it) or hostile reasons (an attacker tampered with the trail). The program should not have one process for "we cannot prove this because the vendor cannot export the log" and another for "we cannot prove this because the agent cleaned up after itself." Both are evidence gaps; both become risk findings; both demand a leadership decision.

The remainder of this paper operationalizes the principle.

## 4. The Seven Evidence Domains

| Evidence Domain | Question It Must Answer | Minimum Evidence Examples |
|-----------------|------------------------|---------------------------|
| **Identity** | Who or what initiated the action? | Human user, agent identity, service account, app registration, workload identity, delegated token, device/session context. |
| **Intent / Trigger** | Why did the action occur? | Prompt, workflow trigger, scheduled job, ticket, approval record, policy rule, business process context. |
| **Action** | What did the system actually do? | Tool call, API request, data query, file access, message sent, workflow update, admin change, model/tool invocation. |
| **Data** | What information was touched? | RAG retrieval records, document/object access, database query, data classification, egress path, output artifact. |
| **Control** | What allowed, blocked, warned, logged, or escalated it? | Policy decision point, IAM rule, DLP event, CASB/SSE log, model guardrail, approval gate, EDR/network control. |
| **State** | What version/configuration was active? | Model version, system prompt/template version, agent configuration, plugin/tool version, policy version, exception state. |
| **Time** | Can the chain be reconstructed? | Normalized timestamps, correlation IDs, retention period, exportability, chain-of-custody handling. |

Each domain deserves a paragraph of operational expansion. The pattern is the same: the question, the minimum evidence, the failure mode, and what the program treats as a finding.

### 4.1 Identity

The question of *who or what* expanded the moment AI agents started acting under delegated authority. A human user is one identity; the agent the user invoked is another; the service account the agent uses to call a downstream API is a third; the OAuth grant that authorized the call is a fourth; the device and session context is the fifth.

The program's evidence requirement is that, for any material action, the identity chain can be enumerated and walked. The most common failure mode is partial identity — the SaaS audit log records that "App X" took an action, but the program cannot reconstruct *which user's* delegated authority App X was acting under, or which agent inside the application actually selected the action, or which token version was in flight. Each missing layer is a finding. *"We know it was the agent"* is not the same as *"we can name the user, the agent, the token, and the device."*

### 4.2 Intent / Trigger

Intent is the most overlooked evidence domain. In traditional SOC work, intent is often inferred from action and identity. In AI-enabled work, intent has a literal source: the prompt, the workflow trigger, the scheduled job, the upstream ticket, or the policy rule that caused the agent to act.

If the action is a tool call, the program should be able to retrieve the prompt that produced it, the retrieved context that informed it (if RAG is involved), and the upstream business context that justified it. *"The agent decided to send the email"* is not an answer. *"The agent sent the email because the user prompted it to draft and send a follow-up; the draft was approved at 14:02 by user X via Slack approval flow Y"* is an answer. The first is an analyst guess. The second is a defensible evidence chain.

### 4.3 Action

Action is the most commonly logged domain and also the most commonly mis-logged. Application audit logs frequently record the *outcome* of an action ("ticket updated") without the *content* of the action ("ticket updated *by setting Priority from P3 to P1*"). For an agent-driven action, the program needs both, plus the parameters of the call.

This domain also requires distinguishing **planned vs. executed actions**. Many agent platforms log the agent's plan ("I will email customer X with the following draft…") separately from the execution. Both are evidence. The plan tells us what the agent intended; the execution tells us what actually happened to the system. A divergence between the two is itself a high-value signal.

### 4.4 Data

Data is the most regulated of the seven domains and the one most likely to drive notification decisions during an incident. The minimum bar is that the program can name the data the action touched: which document, which database row, which retrieval chunk, which classification, and which destination.

For RAG and vector-layer systems, [Paper 3](paper-3-rag-vector-security.md) defines the evidence requirements in detail: chunk IDs, source document IDs, ACL snapshots at ingest, current ACL state, and the authorization decision applied at retrieval time. For non-RAG flows, the bar is the same: a defensible answer to *"what data was involved, who was authorized to read it, and what happened to the output?"*

### 4.5 Control

Control evidence is what distinguishes a working program from one that hopes. The question is not only *what control was supposed to apply* but *what control fired, what control silently passed, and what control was bypassed.* Each is a different alert and a different remediation.

Programs commonly have logs that record control firings ("DLP blocked upload") but lack logs that record control non-firings ("DLP scanned upload, classified as Internal, allowed"). Both are evidence. The first tells the program the control worked. The second tells the program the control was active and made a defensible decision. A control that produces no log either way — for any outcome — is a control that cannot be evidenced and therefore cannot be defended.

### 4.6 State

State is the AI-specific addition to the classical evidence model. Conventional incident response assumes that the system under investigation has a stable identity over time: this server, this binary, this configuration. AI-enabled systems are not stable in that sense. The model version changes. The system prompt version changes. The agent configuration changes. The plugin or tool set changes. The policy version changes. Any of these can change the meaning of an action.

The program's state evidence requirement is that, at any material moment in the action timeline, the program can answer: *what model, what prompt template, what agent configuration, what tool versions, and what policy state were live?* This usually requires versioning artifacts — model digest, system-prompt hash, agent config snapshot, tool registry version, policy version — that the application emits with every audit event, not retrieved by inference after the fact.

### 4.7 Time

Time is what makes the other six domains usable. Without normalized timestamps and correlation IDs, the chain breaks even when every individual link exists. The program cannot reconstruct an evidence chain from six different log sources unless they share a clock and an identifier.

The minimum bar is: every audit event from every component of an AI-enabled workflow shares a normalized timestamp (UTC, sub-second precision) and propagates a correlation ID from the originating user request through the agent, the model gateway, the tool calls, the data accesses, and the response. The program also needs retention long enough to support the longest plausible incident timeline (typically 13 months for regulated industries; longer for litigation hold) and an export path that does not depend on vendor cooperation during a live incident.

## 5. The D-Evidence Signature Loop

The program loop should now read as follows:

1. Threat intelligence or control concern identifies a plausible AI-enabled abuse path.
2. The hunt team writes a hypothesis that can be tested against available telemetry.
3. **D-Control** defines which preventive, detective, corrective, or compensating controls should constrain the behavior.
4. **D-Evidence** proves whether the behavior occurred, whether the control acted, whether the control was bypassed, and what residual risk remains.
5. Leadership makes a documented risk decision: **accept, avoid, mitigate, or transfer.**
6. The program improves the control, detection, telemetry, ownership model, or procurement standard.
7. The hunt is re-run or converted into continuous monitoring.

This is the practical difference between hunting for interesting anomalies and operating a defensible threat hunting program. The output is not only an alert. The output is a decision-quality evidence package.

The loop is recursive in two ways. First, every hunt produces both findings and *evidence-gap findings*. The findings populate the AI Risk Register; the evidence-gap findings populate a parallel telemetry / instrumentation backlog that funds the next quarter's detection-engineering work. Second, the leadership decision in step 5 is itself evidence — a dated, owned, accountable record that the program preserves alongside the technical artifacts. *Decisions are evidence.*

## 6. Hunt Questions for D-Evidence

Use these as the standing question set for any AI-enabled environment. Each maps to one or more existing hunts in this repository; the parenthetical references identify them.

- Which AI agents, plugins, automations, or integrations have standing access to sensitive systems or regulated data? (anchors to [H-001 Shadow AI](../../hunts/starter/H-001-shadow-ai-discovery.md), [H-002 Excessive OAuth Agency](../../hunts/starter/H-002-excessive-oauth-agency.md))
- Which actions can be performed by a non-human identity without a fresh human approval record? (anchors to [H-008 Workflow Automation Drift](../../hunts/starter/H-008-workflow-automation-drift.md))
- Which OAuth grants, API tokens, service principals, or delegated permissions are older than the business purpose that created them? (anchors to [H-002](../../hunts/starter/H-002-excessive-oauth-agency.md))
- Which agent actions lack a correlation ID that ties prompt/request, tool call, identity, and data access into one timeline? (anchors to [H-004 Agent Tool-Call Anomaly](../../hunts/starter/H-004-agent-toolcall-anomaly.md); see §10 for the instrumentation pattern)
- Which controls generate alerts but do not preserve enough evidence for incident response or audit review? (anchors to [H-010 Security-Agent Overreach](../../hunts/starter/H-010-security-agent-overreach.md))
- Which model, prompt, policy, or agent configuration changed shortly before an abnormal action? (state-domain hunt; see §4.6)
- Which logs are available only inside a vendor console and cannot be exported into the organization's evidence repository? (procurement / vendor due-diligence finding; see [Vendor DDQ §4](../../templates/vendor-due-diligence.md))
- Which containment actions can be validated through a re-hunt rather than assumed from a ticket closure? (anchors to all containment playbooks under [playbooks/containment/](../../playbooks/containment/))

These questions should be carried into every quarterly review, every vendor onboarding, and every post-incident lessons-learned exercise. They are the operating questions of D-Evidence.

## 7. The D-Control / D-Evidence Pairing

Every D-Control question implies a corresponding D-Evidence follow-up. The pairing makes the dependency explicit.

| D-Control Question | D-Evidence Follow-Up | Risk Finding if Missing |
|--------------------|---------------------|-------------------------|
| Was the agent supposed to access this SaaS app? | Show the grant, scope, approver, owner, and last-use evidence. | Unknown non-human access path. |
| Was the tool call allowed? | Show the policy decision, request context, response, and correlation ID. | Control may be unenforced or untestable. |
| Was sensitive data retrieved? | Show object access, retrieval source, classification, output path, and retention. | Data exposure cannot be bounded. |
| Was human approval required? | Show approval workflow, approver identity, timestamp, and exception logic. | Delegated automation may bypass accountability. |
| Was containment completed? | Show revocation, session kill, token invalidation, access review, and validation hunt. | Residual access may remain active. |

Each pairing demonstrates the same pattern: the D-Control question, on its own, can be answered with a policy citation. The D-Evidence follow-up forces the program to produce an artifact. The risk finding describes what the program is exposed to when the artifact does not exist. A program that cannot produce the right column for any row in this table has no defensible answer in the left column.

This pairing is also the basis for the **D-Evidence package** that accompanies any material finding (§8). Where the program's normal hunt output is a finding plus an evidence trail, a D-Evidence pairing failure produces a *third* artifact: the missing-evidence finding, which becomes a backlog item for telemetry, procurement, or vendor pressure.

## 8. The Decision-Grade Evidence Package

The evidence package should be small enough for leadership to read and precise enough for analysts to defend. For each material AI threat hunt finding, the program should produce the following:

- **One-sentence finding:** what happened or what could not be proven.
- **Affected asset / process:** system, data flow, business process, user group, customer impact path, or CUI / regulatory boundary.
- **Evidence chain:** identity, trigger, action, data, control, state, and time.
- **Control assessment:** *passed, failed, bypassed, partially effective, not observable, or not applicable.*
- **Risk decision required:** *accept, avoid, mitigate, or transfer.*
- **Owner and deadline:** named accountable owner for remediation, exception approval, or control redesign.
- **Validation method:** re-hunt query, control test, tabletop, access review, log export, or independent evidence check.

The structure deliberately mirrors the structure of a defensible legal record. A finding written in this form is portable across the audiences who will need it: the SOC analyst writing the incident timeline, the GRC analyst preparing for the audit, the legal team scoping a notification decision, the vendor manager raising a contract issue, and the executive who must accept or escalate the risk.

The program should keep these packages in a dedicated evidence repository (see §11) with retention that matches the longest plausible reuse window — typically the longer of (a) the regulatory retention requirement for the affected data class, (b) the contractual retention requirement with the relevant counterparty, and (c) the litigation-hold horizon advised by counsel. *Evidence packages are not analyst notes. They are the operational record of leadership decisions.*

A starter template lives at [`templates/d-evidence-package.md`](../../templates/d-evidence-package.md). Use it for every material finding; copy it into hunt reports under [`hunts/reports/`](../../hunts/).

## 9. D-Evidence Maturity Model

Programs do not arrive at decision-grade evidence on day one. The maturity model describes the path. Self-assess honestly; the worst answer is to claim a maturity level the program cannot demonstrate.

| Level | Name | Evidence Behavior | Leadership Risk |
|------:|------|-------------------|-----------------|
| 0 | **Blind** | AI workflows execute with limited identity, prompt, tool, or data-access logging. | Material AI workflow risk cannot be bounded after an incident. |
| 1 | **Fragmented** | Some logs exist, but identity, data access, and tool actions are not correlated. | Investigations depend on manual reconstruction and vendor cooperation. |
| 2 | **Traceable** | Core actions have correlation IDs and enough telemetry to reconstruct high-risk events. | Incident response is possible but may be slow or incomplete. |
| 3 | **Decision-grade** | Evidence supports control validation, risk decisions, legal review, and audit requests. | Leadership can defend decisions with proof instead of assumptions. |
| 4 | **Continuously validated** | Findings convert into continuous monitoring, automated evidence collection, and periodic re-hunts. | The program proves ongoing control effectiveness, not one-time compliance. |

Most enterprise programs in 2026 sit at Level 0 or 1 for their AI workflows even when their general security telemetry is at Level 3. The reason is structural: AI workflows often live inside SaaS or vendor-managed environments where the customer cannot inspect, export, or correlate the underlying telemetry without a procurement conversation. The maturity gap is not analyst skill. It is **vendor logging access** plus **correlation-ID propagation** plus **state-versioning discipline**.

The program should target Level 3 for any AI workflow that touches regulated data, executes write actions, or has external customer impact. Level 4 is appropriate for the small set of workflows whose abuse would be material to the business — typically agent-driven workflows that can move money, modify customer records, or make security decisions.

A self-assessment checklist lives at [`templates/d-evidence-maturity.md`](../../templates/d-evidence-maturity.md).

## 10. Telemetry and Integration Patterns

Decision-grade evidence is impossible without three integration patterns in place. These are the AI-specific upgrade to the classical SIEM-and-EDR stack.

### 10.1 Correlation ID propagation end-to-end

Every user-originated request that flows into an AI-enabled workflow should be assigned a correlation ID at the front door (UI, API gateway, ChatOps integration) and propagated through every downstream component: model gateway, agent runtime, tool calls, data accesses, callback responses, and the final business-system update. The propagation discipline is the same as distributed tracing in modern web applications. The difference is that for an AI workflow, the trace is *evidence*, not just a debugging aid.

Implementation patterns the program can require:

- A standard header (`X-Hunt-Correlation-Id` or equivalent) that every internal AI-touching service must accept, log, and forward.
- For vendor systems that do not accept custom headers, an outbound proxy that injects the header into request URIs or augments the application's audit context.
- Mandatory propagation rules in agent / orchestration framework code: every tool call carries the upstream correlation ID; every recorded prompt carries it; every output carries it.

A workflow without correlation-ID propagation cannot exit Level 1 of the maturity model.

### 10.2 LLM gateway and agent gateway as audit chokepoints

Programs that route all LLM / agent activity through a controlled gateway gain a single chokepoint where prompts, retrievals, tool calls, model versions, and identity context can be logged consistently. Programs that allow direct vendor SDK calls from arbitrary services do not gain this — and they discover, mid-incident, that they have no consistent audit posture across teams.

The gateway pattern produces three durable evidence artifacts:

- **Prompt logs** with identity, correlation ID, model version, system-prompt hash, tool registry hash, and (where regulated data is in scope) hashed or redacted content.
- **Tool-call logs** with the agent identity, the tool name, the parameters, the response status, and the downstream identity used.
- **Decision logs** for any guardrail, policy, or content-control firing — including non-firings (the control evaluated and chose to allow).

Build or buy the gateway as a program-level control; do not let each team integrate its own.

### 10.3 State versioning at every component boundary

Every AI-relevant component should emit a version stamp with each audit event. Models emit a model digest (or vendor-stable model name + version). System prompts emit a hash. Agent configurations emit a snapshot ID. Tool registries emit a registry version. Policies emit a policy version. The audit pipeline preserves these stamps so that any later reconstruction can answer *"at the moment of this action, what did the system look like?"*

State versioning is the single most overlooked instrumentation change required to move from Level 2 to Level 3. Without it, a postmortem can say *"the agent did X"* but cannot say *"the agent did X under a system prompt that had been changed 14 minutes earlier by an unrelated rollout."* That second sentence is what allows leadership to distinguish a control failure from a configuration regression.

## 11. Evidence Repository Architecture

D-Evidence requires a place to keep evidence packages, hunt reports, control validation records, and the underlying log evidence that supports them. The repository is a program-level system, not an analyst-side scratchpad.

Functional requirements:

- **Write-once / append-only storage** for finalized evidence packages. Edits should produce a new versioned record and preserve the prior.
- **Cryptographic integrity** (signed manifest, hash-tree, or comparable) for any package that may be used in a regulatory inquiry, litigation hold, or external attestation.
- **Retention controls** aligned to the longest applicable retention obligation across the affected data classes and counterparties.
- **Access controls** that restrict reads to the audiences who need them: SOC, GRC, Legal, Privacy, Internal Audit, the named asset owner, and the executive accountable for the decision. *Evidence is not public.*
- **Export controls** that allow controlled extracts (redacted, partial, time-bounded) for outside-counsel review, customer notifications, vendor disputes, or regulator submissions.
- **Linkage** to the AI Asset Register, AI Risk Register, Decision Log, Exception Register, and the originating hunt(s).

The repository should be designed assuming that, at some point, an outside party will read it: a regulator, an auditor, a customer's security team, an acquirer, or counsel. *The repository is a defense; it should be designed like one.*

## 12. 30 / 60 / 90-Day Build Plan

The plan below is a starting point. Adjust the owner labels to match the organization, but do not adjust the cadence: the program loses momentum if D-Evidence is treated as a future state instead of a current build.

| Timeframe | Action | Owner | Output |
|-----------|--------|-------|--------|
| 30 days | Inventory AI agents, app registrations, OAuth grants, plugins, service accounts, and high-risk automations. | IAM + Security Operations + AI Platform Owner | AI identity and integration register. |
| 30 days | Identify the top five workflows where AI can access, transform, send, approve, or trigger business actions. | Business Owner + GRC + Security | High-risk AI workflow map. |
| 60 days | Define minimum evidence fields for each workflow: identity, trigger, action, data, control, state, and time. | Detection Engineering + DFIR | D-Evidence schema. |
| 60 days | Test whether logs can be exported, retained, correlated, and preserved outside vendor consoles. | Security Engineering + Legal/Compliance | Evidence retention and export gap assessment. |
| 90 days | Create re-hunt procedures for OAuth abuse, abnormal tool calls, sensitive data retrieval, and control bypass. | SOC / Threat Hunt Lead | Repeatable D-Evidence hunt pack. |
| 90 days | Convert findings into executive risk memos with accept/avoid/mitigate/transfer decisions. | CISO / Risk Owner | Decision register and remediation roadmap. |

Two implementation notes that matter more than the plan itself:

1. **The 60-day evidence-export gap assessment is the most important deliverable.** It is the program's first honest map of where vendor-locked telemetry creates structural blind spots. Treat the resulting gaps as procurement conversations, not as engineering tickets. Many of them cannot be closed without a vendor commitment.
2. **The 90-day decision register is the artifact leadership will most use.** It is also the artifact most likely to atrophy after the initial build. Schedule a recurring quarterly review of the register before the 90-day mark passes.

## 13. D-Evidence and DFIR for AI

Digital forensics and incident response for AI-enabled environments is an emerging discipline, but the program does not need to wait for the discipline to settle. The seven evidence domains map directly onto the standard DFIR phases.

- **Preparation:** the gateway, the correlation-ID standard, the state-versioning discipline, the evidence repository, and the seven-domain schema. All must exist before the incident.
- **Detection and analysis:** hunts and detections produce findings and evidence-gap findings; evidence packages are drafted as analysis proceeds, not retrofitted afterward.
- **Containment, eradication, recovery:** containment actions (Paper 2 ladder, plus C-RAG-1..5 from Paper 3) are themselves evidence. Each containment step adds a record to the package; recovery is evidenced by re-hunt, not by ticket closure.
- **Post-incident activity:** the lessons-learned tracker references the evidence package, the decision, the residual risk, and the program improvements that follow. Decisions made during the incident are preserved with their justifications.

NIST SP 800-61 Revision 3 provides the canonical guidance for integrating incident response into the broader cybersecurity risk-management activities; D-Evidence operationalizes that integration for AI-enabled workflows specifically. NIST AI RMF / GenAI Profile and the draft NIST Cyber AI Profile add the AI-aware overlay. Together, the three documents set the policy floor; D-Evidence is the program-level operating model that turns them into running practice.

## 14. D-Evidence in Audit, Regulatory Inquiry, and Customer Notification

A maturing AI program will be tested by parties outside the security team. The forms of the test are predictable:

- **Internal audit** asks for evidence of control effectiveness across a sample of AI-enabled workflows.
- **External audit** asks for evidence aligned to a control framework (SOC 2, ISO 27001, FedRAMP, HITRUST, or sector-specific controls).
- **Regulatory inquiry** asks for evidence of who acted, what data was involved, what controls applied, and how leadership responded.
- **Customer notification** decisions ask whether the organization can rule out exposure of specified data classes to specified parties within a specified time window.
- **Litigation discovery** asks for the full chain across identity, action, data, control, state, and time, preserved through hold.

D-Evidence is what allows the program to respond to all five with the same artifacts. The evidence package format is portable; the underlying log evidence is preserved in the evidence repository; the decision log shows what leadership chose and when; the exception register shows what was knowingly accepted and why.

The argument for D-Evidence is therefore not only technical. It is also commercial. A vendor's enterprise customers increasingly ask for AI-specific evidence in their security questionnaires, in their pre-renewal reviews, and in their incident-response tabletop participation. The organizations that can answer those questions will close deals and renewals faster. The organizations that cannot will increasingly cede ground to the ones that can.

## 15. Anti-Patterns

A short list of common failure modes the program should refuse to ship.

- **"The vendor logs it; we're fine."** If the program cannot export, retain, and correlate the vendor's logs into its own repository under its own retention policy, the evidence is not the program's. It is the vendor's. That is a procurement finding.
- **"Ticket closed; the issue is resolved."** Containment that is not validated by re-hunt is assumed, not proven. Tickets close; access remains. The program treats post-containment validation as a required evidence artifact, not an analyst nicety.
- **"The agent decided…"** Identity collapsed into a single name ("the agent") strips the full identity chain. The program insists on the chain: human, agent, service account, token, device, session.
- **"We don't log prompts for privacy reasons."** A reasonable concern, but not an evidence answer. The program should hash, redact, or class-level-summarize prompts to preserve evidence while addressing privacy. *No evidence at all is not a privacy posture; it is an audit posture.*
- **"It's a one-time exception."** Exceptions without expiration become standing risk. Every exception in the register has an owner, a reason, a compensating control, and a date. The program reviews exceptions on a cadence; expired exceptions are escalations, not housekeeping.
- **"We'll instrument it once we have an incident."** AI incidents move through systems faster than analysts can retrofit telemetry. Instrumentation that does not exist before the incident does not exist during the incident.

## 16. In Three Voices

The program speaks in three voices to three audiences. Use whichever fits the room. They say the same thing.

> **The blunt version:** AI threat hunting cannot stop at *"we saw something unusual."* It must answer whether the organization can prove who or what acted, why the action occurred, what data was touched, which control made the decision, what state the system was in, and whether leadership has enough evidence to make a defensible risk decision.

> **The executive version:** D-Evidence turns threat hunting into governance-grade security intelligence. It helps leaders distinguish between a contained event, a control failure, an evidence gap, and an accepted business risk.

> **The practitioner version:** If the finding cannot be tied to identity, action, data, control, state, and time, the next hunt should not be for more alerts. It should be for the missing evidence.

The three voices are intentionally redundant. The blunt version exists because some rooms only respond to direct language. The executive version exists because some decisions only get made when the value is framed in governance terms. The practitioner version exists because the people doing the work need an operating principle they can apply at 2 a.m. *Do not pick one. Use all three.*

## 17. What This Paper Sets Up

D-Evidence creates the proof record. The next discipline in the series is **D-Decision**: the operating model for converting threat hunt findings into executive action. D-Decision defines how leaders document whether they accept, avoid, mitigate, or transfer the risk, and how analysts avoid the common failure mode where technically valid findings die inside ticket queues without a clear owner or business decision.

If D-Control constrains and D-Evidence proves, then D-Decision binds the work to the business. Together they form the core operating triplet of the AI Threat Hunt Program — each its own discipline, each its own paper, each its own running practice.

## 18. Source Notes / Anchors

- **Internal program anchor:** AI-Securing Threat Hunt Program, structured around hypotheses, telemetry, detections, response actions, and leadership reporting (this repository).
- **Internal topic anchor:** DFIR for AI-Enabled Environments — evidence model for prompts, outputs, tool calls, identity, data access, approvals, and model/version state.
- **NIST AI RMF Generative AI Profile:** supports the need to manage generative AI risks according to organizational goals and priorities.
- **NIST SP 800-61 Rev. 3:** supports integrating incident response considerations into cybersecurity risk-management activities.
- **NIST Cyber AI Profile (draft):** supports the *Secure, Defend, and Thwart* framing for AI-aware cybersecurity.
- **MITRE ATT&CK cloud / OAuth techniques:** supports identity, application integration, token, and persistence-oriented threat modeling.

## 19. References

- NIST AI Risk Management Framework and Generative AI Profile: https://www.nist.gov/itl/ai-risk-management-framework
- NIST SP 800-61 Revision 3, Computer Security Incident Handling Guide: https://csrc.nist.gov/pubs/sp/800/61/r3/final
- NIST Cybersecurity, Privacy, and AI Program: https://www.nist.gov/cybersecurity
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Agentic AI Threats and Mitigations: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- MITRE ATLAS: https://atlas.mitre.org/
- MITRE ATT&CK: https://attack.mitre.org/
- Cloud Security Alliance AI Controls Matrix: https://cloudsecurityalliance.org/artifacts/ai-controls-matrix
- NCSC / CISA / NSA Guidelines for Secure AI System Development: https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development
- This repository: Paper 2 (D-Control), Paper 3 (RAG and Vector-Layer Security), Hunts H-001..H-010, RAG-001..RAG-006, Containment ladder L1..L7, Vendor Due Diligence Questionnaire, Executive Metrics.

## About the Author

**Angie Agee, CISSP** is the principal of **Agee Cyber Advisory** and the architect of the AI-Securing Threat Hunt Program — a blue-team operating model for finding, defining, detecting, denying, defending, containing, documenting, and deciding on the AI systems already running inside the enterprise.

Her work pairs governance frameworks (NIST AI RMF / GenAI Profile, MITRE ATLAS, OWASP LLM and Agentic AI, CSA AI Controls Matrix, NCSC / CISA / NSA secure AI lifecycle guidance, Google SAIF) with the operational artifacts security teams actually need: asset registers, hunt hypotheses, telemetry requirements, containment playbooks, evidence packages, and executive metrics. The doctrine is direct — *evidence, controls, hunts, response* — and intentionally anti-theater.

Reach: Agee Cyber Advisory · LinkedIn · GitHub — [github.com/casarezaz/ai-threat-hunt-program](https://github.com/casarezaz/ai-threat-hunt-program)
