# D-Control: The Signature Loop for AI Threat Hunting and Operational Security

**Paper 2 in the AI Threat Hunting and Operational Security Series**

**Core loop:** Discover -> Define -> Detect -> Deny -> Defend -> Degrade/Contain -> Document -> Decide

## Executive Summary

AI security is moving faster than traditional governance, and the most dangerous gap is not always the model itself. The operational risk sits in the space where AI systems touch enterprise data, identities, browser sessions, SaaS integrations, APIs, developer tools, workflow automation, RAG pipelines, and autonomous agents. A policy may say AI use is approved or prohibited, but a threat hunt program needs to answer a harder question: can the organization see, limit, detect, and contain what AI is doing inside the environment?

D-Control is a defensive operating loop for AI threat hunting and operational security. It converts AI governance from an abstract review process into repeatable outputs: discovered assets, defined capabilities, detection logic, denial controls, defensive hardening, containment options, evidence, and executive decisions. It is intentionally simple enough to brief to a board and practical enough to drive a hunt backlog.

The loop is: Discover, Define, Detect, Deny, Defend, Degrade/Contain, Document, and Decide. Each step forces a measurable output. If an AI system cannot be discovered, it cannot be governed. If its capabilities are undefined, its blast radius is unknown. If telemetry is missing, abuse becomes invisible. If denial and containment paths do not exist, the organization is relying on hope instead of control.

This paper is the second artifact in the AI Threat Hunting and Operational Security series. The first paper established the need for an AI-securing threat hunt program. This paper defines the signature loop that makes the program operational.

## Why D-Control Exists

Most enterprise AI conversations split into two weak positions. One side treats AI as a magical productivity layer that should be adopted quickly. The other treats AI as a compliance problem that can be managed with policies, attestation, and acceptable-use language. Both views are incomplete.

AI is not just a tool. In modern enterprise environments, AI is increasingly a connective layer. It can read documents, summarize messages, generate code, trigger workflows, call APIs, enrich tickets, triage incidents, interact with customers, search internal knowledge bases, and operate through authenticated user context. In agentic forms, it can plan, select tools, execute steps, and produce outputs that influence business decisions.

That means AI security must be treated as operational security. The problem is not simply whether a model is trustworthy. The problem is whether the organization can control the full chain of action: user, prompt, model, tool, identity, data source, output, workflow, and decision.

D-Control exists because enterprises need a practical way to measure whether AI is operating inside defensible boundaries. It is built for defenders, threat hunters, SOC leaders, GRC leaders, architects, and executives who need the same vocabulary for AI risk, detection, and containment.

The doctrine is direct: if AI has access, agency, or influence, it needs D-Control.

## Framework Alignment

D-Control is not intended to replace existing AI security and risk frameworks. It operationalizes them for threat hunting and control validation.

It aligns well with NIST AI RMF and the Generative AI Profile because those resources emphasize risk management across governance, mapping, measurement, and management. It aligns with OWASP LLM and Agentic AI security work because those resources identify concrete application risks such as prompt injection, sensitive information disclosure, supply-chain exposure, excessive agency, insecure output handling, data and model poisoning, and unbounded consumption. It aligns with MITRE ATLAS because ATLAS provides an adversary-focused language for threats to AI-enabled systems. It aligns with CSA's AI Controls Matrix because cloud AI must be assessed through control objectives, accountability, architecture, and shared responsibility. It aligns with secure AI lifecycle guidance from NCSC, CISA, NSA, and partner agencies because secure operation requires logging, monitoring, incident response, update management, and responsible deployment.

The practical difference is that D-Control forces each principle to produce an operational artifact. A framework can tell the organization what should matter. D-Control asks whether the evidence exists.

## The Signature Loop

D-Control is a continuous loop, not a one-time assessment. AI systems change too quickly for annual governance. New tools appear in browser histories, OAuth consent logs, SSO apps, SaaS audit trails, procurement records, developer workstations, Git repositories, notebooks, workflow platforms, and ticketing systems. New integrations can quietly expand capability. New prompts can expose sensitive data. New agents can add write action where only read action was expected.

The loop repeats across every AI asset class:

1. Discover: Find the AI system or AI-enabled workflow.
2. Define: Classify what it is, what it can access, and what it can do.
3. Detect: Build visibility, logging, alerts, and hunt hypotheses.
4. Deny: Block unsafe access, action, and data movement.
5. Defend: Harden the identity, data, workflow, model, and integration surfaces.
6. Degrade/Contain: Reduce or isolate capability when risk rises.
7. Document: Preserve evidence, decisions, residual risk, and control gaps.
8. Decide: Make an explicit business/security decision: allow, limit, monitor, redesign, pause, replace, or terminate.

Every AI system should be able to survive this loop. If it cannot, the issue is not AI maturity. It is operational exposure.

## The D-Control Steps

### Discover

**Objective:** Find the AI attack surface before it finds the organization.

**Key actions:**
- Inventory sanctioned and unsanctioned AI usage across SaaS, cloud, endpoint, browser, developer, messaging, ticketing, and workflow platforms.
- Identify AI embedded inside existing products, not only obvious standalone chat tools.
- Collect owners, business processes, vendors, tenants, models, connectors, API keys, OAuth grants, and data sources.

**Artifacts and telemetry:**
- SSO and IdP application lists
- CASB/SSE and SWG logs
- Browser history and extension inventories
- SaaS audit logs
- Cloud service inventory
- Endpoint process and network telemetry
- Git and CI/CD secrets scans
- Procurement and expense data

**Hunt pivots:**
- New AI domain accessed by multiple users in the last 30 days
- OAuth grant to AI application with file/email/calendar scope
- Developer workstation connecting to unapproved model API
- Browser extension using AI with broad page-read permissions

### Define

**Objective:** Classify capability, data access, agency, identity, and blast radius.

**Key actions:**
- Classify the asset type: SaaS LLM, embedded copilot, enterprise agent, custom/internal agent, IDE/CLI agent, browser/computer-use agent, RAG system, or workflow/RPA agent.
- Determine whether the system can read, write, execute, transact, publish, delete, deploy, approve, or modify security controls.
- Map sensitive data exposure and identity context.

**Artifacts and telemetry:**
- AI asset register
- Data classification matrix
- Capability/agency scoring
- Identity and permission mapping
- Business process map
- Vendor shared-responsibility notes

**Hunt pivots:**
- AI tool with write access but no named owner
- Agent able to call ticketing and messaging APIs without approval gate
- RAG pipeline indexing restricted documents
- Copilot enabled in a tenant without role-based policy review

### Detect

**Objective:** Create the visibility needed to prove normal and abnormal AI behavior.

**Key actions:**
- Identify minimum viable telemetry for prompts, outputs, tool calls, API calls, data retrieval, identity, admin changes, connector changes, and error/failure paths.
- Build hunt hypotheses around misuse, leakage, tool abuse, prompt injection, excessive agency, anomalous data retrieval, and unauthorized automation.
- Validate whether detections work through testing, purple-team exercises, and controlled simulation.

**Artifacts and telemetry:**
- SIEM queries
- SaaS audit logs
- DLP alerts
- EDR telemetry
- API gateway logs
- Vector DB query logs
- RAG retrieval logs
- Workflow run history
- LLM gateway logs
- Model billing and token usage

**Hunt pivots:**
- Prompt containing secrets or regulated data
- Agent tool-call spike outside business hours
- Unusual vector search against privileged documents
- AI-generated code committed with hardcoded credentials
- OAuth grant followed by mass file access

### Deny

**Objective:** Stop unsafe behavior before it becomes an incident.

**Key actions:**
- Deny unsanctioned AI apps where policy, data exposure, or vendor risk is unacceptable.
- Restrict high-risk connectors, plugins, scopes, browser extensions, autonomous workflow triggers, and data sources.
- Enforce role-based access, conditional access, approval gates, and data-loss prevention.

**Artifacts and telemetry:**
- SSE/SWG policy
- CASB controls
- OAuth app restrictions
- Conditional access rules
- DLP policies
- API allow/deny lists
- Browser extension controls
- Tenant configuration baselines

**Hunt pivots:**
- Block AI upload of restricted data
- Deny third-party AI OAuth app with Gmail/Drive/SharePoint write scopes
- Prevent unmanaged browser agent extension installation
- Disable autonomous approval workflow without human review

### Defend

**Objective:** Harden the environment so approved AI can operate within controlled boundaries.

**Key actions:**
- Apply least privilege to identities, tools, data stores, and connectors.
- Separate read from write actions and require approvals for high-risk action classes.
- Secure model APIs, RAG ingestion, vector stores, CI/CD, secrets, logging, and vendor configurations.
- Add prompt and output handling controls where practical, but do not rely on prompt controls alone.

**Artifacts and telemetry:**
- Reference architecture
- Secure configuration baseline
- Approval workflow
- Prompt/data handling standard
- Secrets management
- Logging standard
- Vendor security requirements
- Red-team test plan

**Hunt pivots:**
- RAG ingestion pipeline validates source authorization
- Agent can draft but not send external email without approval
- IDE agent runs in isolated dev workspace
- Model API keys stored in managed secrets vault

### Degrade / Contain

**Objective:** Reduce capability quickly when risk exceeds confidence.

**Key actions:**
- Create graduated containment actions before an incident occurs.
- Degrade capability rather than choosing only between full access and total shutdown.
- Contain by revoking scopes, disabling connectors, forcing human approval, restricting data sources, sandboxing agents, limiting token volume, or pausing the workflow.

**Artifacts and telemetry:**
- Containment playbooks
- Kill switch procedures
- OAuth revocation process
- Connector disablement paths
- Tenant rollback plans
- SOAR actions
- Evidence preservation checklist

**Hunt pivots:**
- Switch agent from autonomous mode to approval-required mode
- Disable file-system tool for IDE agent
- Revoke calendar/email connector after abnormal sends
- Quarantine RAG index after sensitive data ingestion error

### Document

**Objective:** Turn findings into defensible evidence and repeatable improvement.

**Key actions:**
- Document assets, owners, data flows, decisions, detections, exceptions, risk acceptance, incidents, and lessons learned.
- Keep records understandable to security, legal, privacy, audit, and executive stakeholders.
- Capture both the technical facts and the decision trail.

**Artifacts and telemetry:**
- AI risk register
- Hunt reports
- Exception register
- Control validation records
- Incident timelines
- Vendor due-diligence notes
- Executive risk memo
- Lessons-learned tracker

**Hunt pivots:**
- Hunt found 14 users accessing unsanctioned AI; 3 uploaded sensitive documents
- Vendor cannot provide prompt-level logging; residual risk accepted by business owner
- Agent changed ticket priority automatically; workflow redesigned with approval gate

### Decide

**Objective:** Force a clear business/security decision instead of passive exposure.

**Key actions:**
- Convert findings into a decision: allow, limit, monitor, redesign, pause, replace, or terminate.
- Tie decisions to residual risk, business value, compensating controls, and executive accountability.
- Revisit decisions when the AI system gains new connectors, data access, model capabilities, or autonomy.

**Artifacts and telemetry:**
- Risk acceptance decision
- Go/no-go record
- Exception expiration date
- Remediation plan
- Executive dashboard
- Control maturity score
- Quarterly review packet

**Hunt pivots:**
- Approve SaaS AI for low-risk content only
- Limit enterprise agent to read-only access until logging improves
- Pause browser-agent pilot until session-isolation controls are available
- Terminate vendor due to insufficient auditability

## Asset Classes Covered by D-Control

D-Control should be applied by capability class, not by product name. Product names change, vendors rebrand, and AI features are often embedded inside existing platforms before security teams know they exist. The asset class determines what to monitor and contain.

Key classes include: SaaS LLMs used through a browser; embedded SaaS copilots inside productivity, CRM, ticketing, security, finance, and HR tools; enterprise AI agents with tool access; custom/internal agents built on orchestration frameworks; IDE and CLI coding agents; browser and computer-use agents; RAG systems and vector databases; model APIs and AI gateways; workflow/RPA agents; customer-facing AI agents; and security operations agents.

The risk register should record the class, but the score should be driven by five questions: What data can it access? What identity does it act through? What actions can it take? What telemetry exists? What containment path exists?

## D-Control Risk Scoring

A practical risk score should punish two conditions: high agency and low visibility. An AI system with read-only access and strong logging may be manageable. An AI system with write access, broad OAuth scopes, customer data, and weak audit logs is a different class of risk.

Recommended scoring dimensions:

- Likelihood: probability of misuse, abuse, misconfiguration, prompt-driven error, or adversarial influence.
- Impact: business, legal, privacy, financial, operational, security, or reputational harm if abused.
- Capability / Agency: the system's ability to take actions beyond answering a prompt.
- Data Sensitivity: exposure to regulated, confidential, customer, employee, financial, intellectual property, or security data.
- Identity Context: whether the AI acts as a user, service account, privileged account, shared account, or external vendor system.
- Observability: quality of logs, prompts, outputs, tool calls, retrieval events, admin changes, and vendor audit exports.
- Containment Readiness: ability to revoke, disable, isolate, degrade, or roll back quickly.
- Control Maturity: strength of approval, least privilege, DLP, policy, configuration, and incident response controls.

A simple defensible formula:

Inherent Risk = Likelihood x Impact + Capability/Agency + Data Sensitivity + (6 - Observability)

Residual Risk = Inherent Risk - Control Maturity - Containment Readiness

This is not meant to be mathematically perfect. It is meant to make the ugly facts visible. If AI has more agency than the organization has observability, risk should rise.

## Telemetry and Monitoring Requirements

AI monitoring cannot rely on one log source. The useful picture is assembled from identity, SaaS, browser, cloud, endpoint, data, network, application, and workflow telemetry.

Minimum telemetry categories:

- Identity: sign-ins, conditional access, OAuth grants, service principals, privileged role assignments, MFA changes, impossible travel, token events.
- SaaS: app audit logs, admin changes, file access, message access, connector additions, workflow runs, customer data access.
- Browser: AI domains, extensions, session activity, unmanaged browsers, copy/paste and upload controls where available.
- Endpoint: IDE agent processes, CLI agent usage, model API calls, local file access, secrets exposure, shell history where appropriate and lawful.
- Network: model API destinations, unusual egress, new AI services, DNS to unapproved AI domains, proxy categories.
- Data security: DLP events, file labels, sensitive document access, uploads, downloads, sharing changes.
- RAG/vector: ingestion sources, embedding jobs, retrieval events, query patterns, index permissions, document lineage.
- API and workflow: tool calls, function invocations, webhook activity, automation runs, approval bypass, failed action attempts.
- Cloud: model service use, keys, IAM permissions, storage access, logs, compute resources, cost anomalies.
- Security tooling: agent-generated queries, case actions, containment actions, rule changes, suppression changes, response recommendations.

The monitoring goal is not to record every token forever. The goal is to preserve enough context to answer: who used the AI, what data was involved, what action was taken, what control allowed it, and how fast can it be contained?

## Starter Hunt Backlog

The following hunts are designed to be practical starting points for a D-Control program.

1. Shadow AI discovery: Identify users and devices accessing unapproved AI services.
2. Excessive OAuth agency: Find AI applications with email, calendar, file, ticketing, CRM, or messaging scopes that exceed business need.
3. Sensitive-data prompt exposure: Detect uploads or prompts containing secrets, source code, customer data, employee data, regulated data, incident details, or confidential business records.
4. Agent tool-call anomaly: Hunt for unusual tool-call volume, new tools, failed tool calls, after-hours execution, or high-risk action types.
5. Browser-agent session risk: Identify browser/computer-use agents operating in authenticated enterprise sessions.
6. IDE/CLI agent secret exposure: Find generated code, commits, shell commands, logs, or prompts containing credentials, tokens, private keys, or internal endpoint details.
7. RAG retrieval mismatch: Detect queries that retrieve documents outside expected user authorization or business context.
8. Workflow automation drift: Identify AI-enabled workflow runs that create, send, approve, delete, publish, deploy, or update without required human approval.
9. AI cost and resource abuse: Hunt for model/API usage spikes, abnormal token usage, unusual embedding jobs, or model-denial-of-wallet patterns.
10. Security-agent overreach: Review AI-generated security actions, suppressions, containment recommendations, ticket closures, or detection-rule changes for unsafe automation.

Each hunt should produce four things: findings, evidence, control gaps, and a decision.

## Containment Playbooks

AI containment should be staged. A mature program should not have only two settings: allow everything or shut everything down. D-Control uses graduated containment.

Level 1 - Monitor: Continue operation while increasing logging, alerting, and review.
Level 2 - Limit: Restrict data sources, scopes, user groups, external sharing, model access, or action types.
Level 3 - Approval Gate: Require human approval before send, deploy, delete, transact, publish, or modify.
Level 4 - Degrade: Move the AI from autonomous to assisted mode, from write to read-only, from broad access to curated access, or from production to sandbox.
Level 5 - Isolate: Segment the agent, disable connectors, rotate keys, quarantine RAG indexes, or block external egress.
Level 6 - Suspend: Pause the AI system or vendor integration pending investigation.
Level 7 - Terminate: Remove the system, revoke access, replace the vendor, or retire the use case.

The most important containment question is simple: can the organization reduce capability faster than the AI can expand blast radius?

## Governance Without Theater

D-Control does not reject governance. It makes governance useful. The problem is governance theater: long forms, vague policy language, and AI approval boards that do not produce operational control.

A D-Control governance record should include:

- AI asset name and owner.
- Business use case and value statement.
- Data classification and data flow.
- Identity and permission model.
- Capability and agency rating.
- Required telemetry and actual telemetry.
- Vendor logging and retention limits.
- Detection coverage.
- Denial controls.
- Containment procedure.
- Residual risk.
- Approval, exception, or rejection decision.
- Expiration date for review.

If governance cannot answer what to detect, deny, defend, or contain, it is not governance. It is paperwork.

## Operating Cadence

A D-Control program should run on a cadence that matches AI change velocity.

Daily or continuous: monitor new AI domains, OAuth grants, high-risk prompts/data events, abnormal agent/tool-call behavior, and urgent vendor/security advisories.

Weekly: review new AI assets, exceptions, hunt findings, sensitive-data exposure, high-risk users, high-risk workflows, and containment gaps.

Monthly: update the risk register, validate detections, review vendor changes, run at least one AI-focused hunt, and brief business owners.

Quarterly: conduct executive review, refresh the AI asset inventory, test containment playbooks, validate control maturity, re-score top risks, and update the roadmap.

Annually or after major change: reassess the AI program, threat model, vendor landscape, policies, response playbooks, data flows, and control ownership.

The cadence should also trigger automatically when a system gains a new connector, a new model, a new data source, a new action capability, a new vendor subprocessor, a new privileged role, or a new customer-facing workflow.

## Executive Metrics

Executives do not need token-level noise. They need decision-grade metrics.

Recommended metrics:

- Percent of AI assets discovered and classified.
- Percent of AI assets with named owners.
- Percent of AI assets with defined data classification.
- Percent of high-risk AI assets with usable telemetry.
- Number of AI systems with write/action capability.
- Number of AI systems with excessive OAuth scopes.
- Number of unsanctioned AI services used in the environment.
- Sensitive-data exposure events involving AI.
- High-risk agent actions blocked, approved, or contained.
- Mean time to discover new AI use.
- Mean time to revoke or degrade AI capability.
- Percent of AI assets with documented containment playbooks.
- Residual risk trend for top AI systems.
- Number of vendor logging gaps accepted by leadership.

The executive message should be crisp: where AI has agency, security needs control.

## Implementation Roadmap

A fast-track D-Control implementation can begin immediately.

Phase 1 - Foundation: Create the AI asset register, define asset classes, collect existing logs, identify sanctioned and unsanctioned AI use, and establish scoring criteria.

Phase 2 - Visibility: Validate telemetry from SSO, CASB/SSE, SaaS, browser, endpoint, cloud, DLP, developer tools, workflow automation, and model/API gateways. Identify blind spots.

Phase 3 - Controls: Implement denial controls for unsanctioned AI, excessive OAuth scopes, risky browser extensions, sensitive-data uploads, high-risk connectors, and autonomous actions.

Phase 4 - Hunts: Run starter hunts, document findings, create detection logic, and build a backlog of use-case-specific hunts.

Phase 5 - Containment: Write playbooks for revoke, disable, isolate, degrade, approval-gate, and suspend actions. Test them.

Phase 6 - Executive Loop: Report metrics, decisions, residual risk, and investment needs. Treat unresolved visibility gaps as leadership decisions, not SOC mysteries.

The program does not need to wait for perfect tooling. The first version can be built from existing identity, proxy, DLP, SaaS, cloud, endpoint, and ticketing data. The goal is to start producing D-Control outputs quickly.

## Service and Deliverable Packaging

D-Control can be packaged as a consulting service, internal program, or open-source operating model.

Potential deliverables:

- D-Control AI Asset Register.
- D-Control AI Risk Register.
- AI Agentic and SaaS AI Inventory.
- AI Telemetry Requirements Matrix.
- AI Hunt Backlog.
- AI Vendor Due-Diligence Questionnaire.
- AI Containment Playbooks.
- AI Executive Risk Brief.
- AI Security Operating Cadence.
- AI Detection Engineering Starter Pack.
- AI Governance-to-Operations Mapping.

The strongest market position is not that D-Control is a replacement for NIST, OWASP, MITRE, CSA, or secure AI lifecycle guidance. The position is that D-Control turns those ideas into operational outputs security teams can run.

## Closing Position

AI is useful. AI is dangerous. Both statements can be true without panic or hype.

The organizations that handle AI well will not be the ones with the prettiest AI policy. They will be the ones that can see their AI systems, define their capabilities, detect abnormal behavior, deny unsafe use, defend the surrounding environment, degrade or contain capability when risk spikes, document the evidence, and force clear decisions.

That is D-Control.

AI security without D-Control is policy theater. AI with agency requires operational control.

## References

- NIST AI Risk Management Framework and Generative AI Profile: https://www.nist.gov/itl/ai-risk-management-framework
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Agentic AI Threats and Mitigations: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- MITRE ATLAS: https://atlas.mitre.org/
- Cloud Security Alliance AI Controls Matrix: https://cloudsecurityalliance.org/artifacts/ai-controls-matrix
- NCSC / CISA / NSA Guidelines for Secure AI System Development: https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development
- Google Secure AI Framework: https://saif.google/