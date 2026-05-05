# RAG and Vector-Layer Security: Authorization, Lineage, and Containment for Retrieval Pipelines

**Paper 3 in the AI Threat Hunting and Operational Security Series**

**Core thesis:** RAG turns the retrieval layer into a side channel around access control. Unless authorization, lineage, and containment are enforced at retrieval time — not at the model — RAG becomes the most expensive data-leakage path the organization has built on purpose.

## Executive Summary

Retrieval-augmented generation has become the default architectural pattern for putting an enterprise's own data behind an LLM. It works because it is simple: chunk documents, embed them, store the embeddings in a vector database, retrieve the top-k similar chunks at query time, and inject them into the model's context. The pattern is so easy to demo that organizations now run RAG over knowledge bases, ticketing systems, contracts, code, HR records, and incident timelines.

The security model is not as easy. RAG quietly breaks three assumptions that the rest of the enterprise depends on:

- **Authorization is enforced at the data store, not at the model.** When documents are pre-embedded into a vector index, the access checks that the source system would have applied at read time are gone. The vector index becomes a flat, permission-free copy of whatever was ingested.
- **Logging is at the application layer.** Source systems log who read what. Vector databases log who queried what *embedding* — a number, not a document, not an identity. Mapping a query back to a real user, a real document, and a real authorization decision is the program's job, not the vendor's.
- **The retrieved content is treated as data, but the model treats it as instructions.** Anything that can land in a chunk that gets retrieved becomes part of the model's prompt. Indirect prompt injection becomes a routine misuse class, not an exotic one.

This paper extends Paper 2 (D-Control) into the RAG and vector layer. It defines the RAG attack surface across five stages — ingestion, embedding, indexing, retrieval, and generation context — and gives defenders a working set of hunts, telemetry requirements, containment options, and architectural rules. The doctrine is direct: if the vector index can answer a question the user could not have asked the source system, the program has a control gap.

## Why RAG Needs Its Own Paper

D-Control already names RAG systems as an asset class. But three properties make RAG worth a dedicated paper:

1. **The control plane is split across several teams.** Document owners control the source. A data team owns ingestion and chunking. A platform team owns the vector store. An application team owns the retrieval and prompt orchestration. A model team owns the LLM. Security is structurally last in line. The decision-making chain that would normally be one team — IAM around the source system — becomes four to six teams, each owning part of the access path. The result is that nobody in the chain is accountable for retrieval-time authorization.
2. **The failure mode is silent.** When a misconfigured RAG returns a document the user should not have seen, the user does not get a 403. They get an answer. There is no error log to chase. The data leak is the *correct* output of an *incorrect* authorization model.
3. **The threat model includes content the org wrote itself.** Indirect prompt injection lives in legitimate documents. A wiki page, a Jira ticket, an email, or a vendor PDF can host instructions that hijack any agent that happens to retrieve it. RAG turns the org's own knowledge base into a writable surface for attackers who can get text into any retrievable corpus.

These properties make RAG a separate operating problem from "general LLM security" and they justify its own playbook.

## Framework Alignment

This paper aligns with and operationalizes:

- **OWASP Top 10 for LLM Applications**, especially LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling, LLM06 Excessive Agency, and LLM08 Vector and Embedding Weaknesses.
- **OWASP Agentic AI Threats and Mitigations**, especially memory poisoning (ATA-001) and cascading hallucinations (ATA-005) when retrieved content drives multi-step agent decisions.
- **MITRE ATLAS**, specifically AML.T0024 Exfiltration via Inference and AML.T0051 LLM Prompt Injection.
- **NIST AI RMF / GenAI Profile**, on data governance, measurement, and management practices applied to retrieval systems.
- **CSA AI Controls Matrix**, on shared-responsibility boundaries with vector DB and embedding-API vendors.
- **NCSC / CISA / NSA Guidelines for Secure AI System Development**, on logging, monitoring, supply chain, and update management for RAG components.

The contribution this paper makes is not novel framework language — it is the operational mapping from these principles to retrieval-layer artifacts a defender can actually run.

## The RAG Attack Surface (Five Stages)

A RAG pipeline is five distinct operations, each with its own threat model. Treat them separately.

### Stage 1: Ingestion

Documents enter the pipeline from source systems: SharePoint / Google Drive / Confluence / Notion / S3 / Box / Slack / Jira / GitHub / databases / email. Ingestion can be one-shot, scheduled, or change-driven via webhooks.

**What can go wrong:**

- The ingestion service runs as a service account with broader access than any individual user. Any document the service account can see lands in the index, regardless of who the eventual reader will be.
- Source-side classification labels (Sensitivity, Retention, Legal Hold) are dropped at ingestion. The index sees plain text.
- Restricted sub-folders, restricted channels, restricted projects are pulled in because the ingestion filter was a directory, not an ACL.
- Soft-deleted, expired, or legal-hold documents are ingested before the source system enforces deletion.

### Stage 2: Embedding

The chunked text is sent to an embedding model — usually a third-party API. Embeddings are produced and either stored back to the vector DB or returned to the application.

**What can go wrong:**

- Embedding APIs receive raw chunk text. Vendor logging policies determine whether that text is retained, used to train, or shared with sub-processors.
- Chunk boundaries can split a redaction or split a security-sensitive sentence across chunks, defeating downstream filtering.
- Failed embeddings get retried; retries can create duplicate, divergent index entries.

### Stage 3: Indexing

Embeddings land in a vector store: Pinecone, Weaviate, Qdrant, Chroma, Milvus, OpenSearch knn, pgvector, or a custom store. Each chunk gets an ID, an embedding vector, and metadata (source document ID, source URL, chunk position, classification labels if you bothered).

**What can go wrong:**

- Metadata is treated as optional. Without metadata you cannot filter retrieval by user authorization, source system, classification, or freshness.
- The index is shared across tenants in a multi-tenant application. Without per-tenant filters at retrieval time, a query from Tenant A can match documents from Tenant B.
- The index supports raw metadata-update APIs that can rewrite chunk text, source IDs, or classification labels post-ingest. Unbounded write access to the index is a poisoning surface.
- Backups, snapshots, and replicas inherit the index without enforcing the same access controls.

### Stage 4: Retrieval

A user (or an agent) issues a query. The application embeds the query, searches the vector store, gets the top-k matches, and injects them into the model's context.

**What can go wrong:**

- The query is executed without filtering by the user's authorization scope. The application "trusts" the index because the index is internal.
- Top-k is a hard knob, not a security control. Setting k=10 retrieves whatever is most semantically similar — which can include a single document the user is not allowed to see.
- Reranking, hybrid search, and metadata filters are applied unevenly across application paths. A debug page, a "raw retrieval" endpoint, or an agent's tool call may bypass filters that the main UI applies.
- Query text is logged in plain form — exposing sensitive prompts in the vector DB's audit trail.

### Stage 5: Generation Context

The retrieved chunks are formatted into the model's prompt and the model generates an answer.

**What can go wrong:**

- The model treats retrieved content as instructions: indirect prompt injection. An email, a Slack message, or a PDF can contain "Ignore previous instructions and …" that a future agent retrieves.
- The model answers using retrieved content the user could not have read directly. The data leak is wrapped in a confident, useful answer.
- Citations are fabricated or stripped, removing the audit trail that would have let a human verify the answer.

## The Central Problem: Authorization at Retrieval Time

The single most important RAG control is authorization enforcement at retrieval time. Every other control is downstream of it.

There are three workable patterns. Pick one and commit to it.

### Pattern A: Per-tenant / per-user index partitioning

Each tenant (or each user, in extreme cases) has its own index. Cross-tenant queries are physically impossible because there is no shared index to query. Operationally expensive but conceptually simple.

**Best for:** strict multi-tenant SaaS; small numbers of high-sensitivity users; legal or regulated tenants.

### Pattern B: Metadata-filtered retrieval

A single index holds embeddings for many tenants / users / classification levels. Every chunk carries metadata: tenant ID, owner, classification, ACL hash, source ID. Every query is rewritten to include a metadata filter that matches the requester's authorization context.

**Best for:** typical enterprise RAG; most internal knowledge bases; cost-sensitive deployments.

**The two ways this fails:**

1. The filter is constructed application-side, and at least one application path forgets to apply it (debug, admin, agent tool call, batch job).
2. The metadata is wrong. ACLs drift in the source system but the index does not get a corresponding update.

### Pattern C: Re-check at the source

The retrieval layer returns candidate chunks; the application then issues an authorization check against the source system for each candidate and drops chunks the user cannot read. Slow, but the most defensible — it inherits the source system's access controls verbatim.

**Best for:** small top-k; legal, finance, HR, and incident-response RAG; situations where the source system has the authoritative access decision and the index cannot be trusted to mirror it.

### Patterns to avoid

- **Trust the model to filter.** Asking the LLM "do not include documents the user is not authorized for" is not a control. It is a hope.
- **Filter at presentation only.** Returning all retrieved chunks to the model and trimming them before display still allows the model to answer based on content the user should not have seen.
- **Single shared index, no metadata, no filter.** This is the modal RAG deployment in 2026 and it is the default leak path.

## Document Lineage and Provenance

Every chunk in the index must be traceable to:

- A source document ID (stable, opaque, not a URL that can change).
- A source system identifier.
- An ingestion timestamp.
- An ingestion job ID.
- The classification label that applied at ingestion.
- The ACL snapshot at ingestion (or a pointer to one).

Without this, four operations are impossible: (1) responding to a takedown / right-to-erasure request, (2) responding to a legal hold, (3) reindexing after an ACL change, and (4) deciding what to quarantine when a sensitive document is discovered to have been ingested by mistake.

Lineage also enables the most useful retrieval-time signal: if a query retrieves a chunk whose source document was modified, deleted, or had its ACL tightened *after* the chunk was indexed, that retrieval should be flagged or blocked.

## Embedding and Index Poisoning

Two distinct attack classes share a name. Treat them separately.

### Embedding poisoning (corpus poisoning)

The attacker influences the corpus that gets ingested. Anything writable that ends up in a retrieval pipeline is a poisoning surface: wiki pages, Slack messages, email threads, Jira tickets, PR descriptions, vendor documents, customer support transcripts, public web pages, GitHub issues. The attacker plants content engineered either to (a) be retrieved for specific queries, or (b) carry indirect prompt injection that will hijack agents that retrieve it.

**Defense priorities:**

- Treat any writable corpus as untrusted. The source system's "internal" label does not equal trust.
- Tag the source system per chunk; surface it to reviewers when high-risk decisions reference retrieved content.
- For agentic use cases, retrieve from segregated indexes by source-trust level. Do not let an admin agent retrieve a low-trust corpus.

### Index poisoning (post-ingest tampering)

The attacker has write access to the vector store directly and modifies metadata, replaces embeddings, or rewrites chunk text. This bypasses the source system entirely. The signal is mismatch between source and index.

**Defense priorities:**

- Tightly scope write access to the vector store. Treat write APIs the way you treat database admin credentials.
- Periodically re-verify a sample of chunks against the source. Drift is the alert.
- Disable raw `update_chunk_text` style APIs in production unless an explicit re-ingestion job is running.

## Indirect Prompt Injection via Retrieved Content

Indirect prompt injection is the most concrete LLM-specific risk in a RAG pipeline. A document the user did not write contains text that influences the model's behavior because the model cannot reliably distinguish "data" from "instruction."

This paper does not relitigate the academic question. The operational question is: *what controls reduce blast radius when, not if, this happens?*

- **Reduce action surface for retrieval-driven agents.** If an agent uses RAG and can also send email, modify tickets, or call APIs, the ingredients for a high-impact compromise are present. Apply Paper 2's containment ladder: read-only by default, approval gate for write actions, kill-switch on the connector.
- **Validate citations.** If the model claims its answer comes from doc X chunk Y, verify it. Mismatch is a signal.
- **Detect retrieved-content patterns.** Sentinel strings like "ignore previous instructions," role-spoofing patterns ("System:", "Assistant:"), tool-call attempts, and sudden language switches should be flagged in retrieved chunks before the model sees them.
- **Treat retrieved-content actions as user actions for audit purposes.** If an agent sent an email because a retrieved document told it to, the audit trail must include the originating chunk ID. Otherwise the postmortem is impossible.

## Telemetry and Monitoring Requirements

RAG telemetry must answer six questions on demand:

1. **Who** queried? (identity, scope, application, agent)
2. **What** was retrieved? (chunk IDs, source document IDs, scores, k)
3. **Was the requester authorized for each retrieved chunk?** (filter applied, source-side authorization result)
4. **What did the model do with it?** (response, citations, tool calls)
5. **What is the lineage of each retrieved chunk?** (source system, ingest job, ingest time, ACL snapshot, current classification)
6. **Has anything in the index changed unexpectedly?** (write events to the vector store, metadata updates, ingestion volume anomalies)

### Minimum log set

- **Ingestion logs:** job ID, source system, document IDs, chunk count, classification labels at ingest, ACL snapshot reference.
- **Embedding logs:** model used, vendor, region, success/failure, retry behavior.
- **Index write logs:** every create/update/delete, with actor identity and source IP.
- **Retrieval logs:** query text (hashed if regulated), embedded query reference, top-k document IDs, scores, metadata filter applied, requester identity and scope.
- **Application authorization logs:** filter construction inputs, source-system authorization checks performed (if Pattern C), drops applied to the result set.
- **Generation logs:** model used, prompt template ID, retrieved chunk IDs, response, citations, tool calls.
- **Drift logs:** scheduled job comparing index metadata to source-system state; output diffs.

### Storage minimums

These logs become evidence during incidents involving sensitive data leaks. Retain them for at least the same period the source systems retain their access logs. If the source retains 12 months and your retrieval logs retain 14 days, your retrieval pipeline has a worse audit posture than the systems it shadows.

## Hunt Patterns

The following hunts extend the H-001..H-010 starter set with RAG-specific patterns. Each follows the same hunt convention: **findings, evidence, control gaps, decision.**

### RAG-001 — Embedding ingestion of unauthorized documents

**Hypothesis:** the ingestion service account is reading documents that no human user in the requesting business unit can read.

**Logic (pseudocode):**

```text
for each ingestion_job in last_24h:
    for each document_id in ingestion_job.documents:
        readers = source_system.who_can_read(document_id)
        consumers = retrieval_app.who_can_query_index(ingestion_job.target_index)
        if not consumers.subset_of(readers):
            flag(document_id, ingestion_job, gap=consumers - readers)
```

**Sigma sketch (for a SIEM with normalized SaaS audit events):**

```yaml
title: RAG ingestion service account reading docs outside consumer scope
id: rag-001
status: experimental
description: Detects ingestion service account reading documents that are not readable by the population of users who will query the resulting index.
logsource:
  product: saas
  service: any
detection:
  ingestion_read:
    actor: '*rag-ingest*'
    action: 'document.read'
  selection_high_sensitivity:
    classification|contains:
      - 'Confidential'
      - 'Restricted'
      - 'Regulated'
  condition: ingestion_read AND selection_high_sensitivity
fields:
  - actor
  - document_id
  - classification
  - source_system
level: high
```

### RAG-002 — Retrieval-time authorization bypass

**Hypothesis:** at least one application path returns retrieval results without the per-user metadata filter being applied.

**Logic (pseudocode):**

```text
for each retrieval_event in window:
    if not retrieval_event.metadata_filter_applied:
        flag(retrieval_event, reason="no filter")
        continue
    for chunk in retrieval_event.results:
        if not source_acl_grants(retrieval_event.identity, chunk.source_document_id):
            flag(retrieval_event, chunk, reason="filter_did_not_match_source_acl")
```

**Sigma sketch:**

```yaml
title: RAG retrieval without authorization filter
id: rag-002
status: experimental
description: Detects retrieval events that returned chunks without an applied metadata filter, or where filter results disagree with the source-system ACL.
logsource:
  product: rag
  service: retrieval
detection:
  unfiltered:
    metadata_filter_applied: false
  acl_mismatch:
    authorization_check_disagreement: true
  condition: unfiltered OR acl_mismatch
fields:
  - identity
  - application_path
  - top_k
  - chunk_ids
  - source_document_ids
level: critical
```

### RAG-003 — Indirect prompt injection in retrieved content

**Hypothesis:** retrieved chunks contain text patterns consistent with injection attempts.

**Logic (pseudocode):**

```text
for each retrieval_event:
    for chunk in retrieval_event.results:
        if injection_patterns.matches(chunk.text):
            flag(chunk, retrieval_event, agent=retrieval_event.agent)
            if retrieval_event.agent.has_write_capability:
                escalate(severity="high")
```

Where `injection_patterns` includes: "ignore (all|previous|the above) instructions", "you are now", "system:", "assistant:", "<\|im_start\|>", base64-encoded tool-call attempts, sudden language switch in a single chunk, and href-bait toward unfamiliar domains.

**Sigma sketch:**

```yaml
title: Likely indirect prompt injection in retrieved chunk
id: rag-003
status: experimental
description: Retrieved-content text matches indirect prompt injection patterns, with elevated severity when the consuming agent has write capability.
logsource:
  product: rag
  service: retrieval
detection:
  injection_pattern:
    chunk_text|re|i:
      - 'ignore (all|the|previous|above) instructions'
      - 'you are (now|hereby) (a|an) '
      - '^\s*(system|assistant)\s*:'
      - '<\|im_start\|>'
  condition: injection_pattern
fields:
  - chunk_id
  - source_document_id
  - source_system
  - agent_id
  - agent_capabilities
level: high
```

### RAG-004 — Index poisoning (post-ingest tampering)

**Hypothesis:** vector index entries have been modified by something other than a sanctioned ingestion job.

**Logic (pseudocode):**

```text
for each index_write_event in window:
    if index_write_event.actor not in approved_ingestion_jobs:
        flag(index_write_event, reason="unsanctioned_writer")
        continue
    if index_write_event.action == "rewrite_text":
        flag(index_write_event, reason="text_rewrite_outside_reingestion")
    sample = sample_recent_chunks(n=100)
    for chunk in sample:
        if hash(chunk.text) != source_system.fetch(chunk.source_document_id).chunk_hash(chunk.position):
            flag(chunk, reason="drift_from_source")
```

**Sigma sketch:**

```yaml
title: Vector index modified outside sanctioned ingestion path
id: rag-004
status: experimental
description: Detects writes to the vector index from actors that are not registered ingestion jobs, or text-rewrite actions outside a re-ingestion window.
logsource:
  product: vector_db
  service: admin
detection:
  unsanctioned_writer:
    actor|not|in: '%approved_ingestion_actors%'
    action:
      - 'upsert'
      - 'update'
      - 'delete'
  text_rewrite:
    action: 'update_text'
  condition: unsanctioned_writer OR text_rewrite
fields:
  - actor
  - source_ip
  - action
  - chunk_id
  - source_document_id
level: high
```

### RAG-005 — Cross-tenant retrieval leakage (multi-tenant)

**Hypothesis:** a query in Tenant A returned a chunk owned by Tenant B.

**Logic (pseudocode):**

```text
for each retrieval_event:
    requester_tenant = retrieval_event.identity.tenant
    for chunk in retrieval_event.results:
        if chunk.metadata.tenant != requester_tenant:
            flag(retrieval_event, chunk, severity="critical")
```

**Sigma sketch:**

```yaml
title: Cross-tenant retrieval leakage
id: rag-005
status: experimental
description: A retrieval event returned at least one chunk whose tenant metadata does not match the requester's tenant.
logsource:
  product: rag
  service: retrieval
detection:
  selection:
    cross_tenant_match: true
  condition: selection
fields:
  - identity
  - requester_tenant
  - chunk_ids
  - chunk_tenants
level: critical
```

### RAG-006 — Stale-permission retrieval

**Hypothesis:** retrieval returned a chunk whose source ACL has tightened since ingestion, and the index still considers the requester authorized.

**Logic (pseudocode):**

```text
for each retrieval_event:
    for chunk in retrieval_event.results:
        ingest_acl = chunk.metadata.acl_snapshot
        current_acl = source_system.current_acl(chunk.source_document_id)
        if requester not in current_acl and requester in ingest_acl:
            flag(chunk, retrieval_event, reason="stale_permission")
```

This is the most common and most-overlooked RAG leak: the document was made restricted three months ago, the index still has it, and nothing reindexes on ACL change.

## Containment Specific to RAG

The Paper 2 containment ladder applies (L1 Monitor → L7 Terminate). RAG adds five containment moves that have no analog in the SaaS-LLM or browser-agent worlds.

### C-RAG-1: Filter override (force-on)

Toggle the application to require metadata filters on every retrieval path. Reject queries that arrive without one. Use when a hunt finds an application path that bypasses authorization filters; useful as a temporary safeguard while the engineering fix lands.

### C-RAG-2: Index-write freeze

Disable all write APIs on the vector store except the sanctioned ingestion job's identity. Use during suspected index poisoning, during incident response, or when investigating drift between source and index.

### C-RAG-3: Partial reindex

Re-embed and re-ingest a subset of documents (a source system, a folder, a tenant, a classification level) from scratch, replacing the existing entries atomically. Use when a control gap is found in past ingestion (e.g., classification was wrong; ACLs were not snapshotted; a confidential folder was indexed).

### C-RAG-4: Index quarantine

Mark a subset of chunks as non-retrievable without deleting them. Preserves evidence and lineage while preventing further retrieval. Use during legal hold, customer-reported leakage, or sensitive-document discovery in an index. Quarantine should be reversible and auditable.

### C-RAG-5: Source-trust segregation

Split a single index into multiple indexes by source-trust level (e.g., "internal-vetted" vs. "external-writable"). High-impact agents only retrieve from the higher-trust index. Use when indirect prompt injection becomes a recurring pattern and tightening upstream trust is impractical.

Each move should have a written runbook before it is needed. The expected duration for revoke-or-quarantine in a RAG incident should match the program's MTTR target — if a sensitive document is found in the index, time-to-quarantine is the metric.

## Hardening Reference Architecture

A defensible RAG pipeline shares the following properties. Use it as a checklist when reviewing existing pipelines and as a baseline when scoping new ones.

- **Ingestion identity is per-source, least-privilege, and named.** No "RAG service" account that reads everything.
- **Source-side classification labels travel with chunks as metadata.** Drop nothing.
- **ACL snapshots are taken at ingestion and refreshed on a defined cadence (and on source ACL change events when subscribable).**
- **Every chunk has metadata for: source system, source document ID, tenant, owner, classification, ACL hash, ingest time, ingest job, position.**
- **Retrieval uses one of Patterns A / B / C. Pattern is documented per-application path.** Debug and admin paths inherit the same enforcement.
- **Vector store write APIs are scoped tightly. Text-rewrite APIs are off by default in production.**
- **Multi-tenant indexes always apply tenant filtering; cross-tenant queries are blocked by default and gated by an explicit, auditable feature.**
- **Retrieval logs include identity, application path, k, filter inputs, chunk IDs, source document IDs, scores, and the authorization check result.**
- **A scheduled drift job compares a sample of index entries to source state and alerts on mismatch.**
- **A "delete from RAG" workflow exists, end-to-end tested, that can remove a document from the index within hours of a takedown / right-to-erasure / legal-hold event.**
- **Indirect-injection screening runs on retrieved chunks before they reach the model — at minimum, on chunks consumed by agents with write capability.**
- **Citations from the model are validated against the actual chunks retrieved. Fabricated citations are an alert.**

## Vendor Due Diligence — RAG Additions

Add to the AI Vendor DDQ in `templates/vendor-due-diligence.md`:

- Does the vector store support per-document and per-chunk metadata, including arbitrary key-value pairs?
- Does the vector store support metadata-filtered queries with hard rejection (not just reranking)?
- Does the embedding API retain the input text? For how long? Used to train? Opt-out path?
- What is the audit log schema for index writes? Does it include actor identity, source IP, action, chunk IDs?
- What is the audit log schema for retrievals? Does it include the metadata filter that was applied?
- Can write APIs (text rewrite, metadata update, deletion) be disabled per-environment or per-token?
- Does the platform support per-tenant or per-namespace isolation? At the storage level or only at the API level?
- What is the documented latency of a "delete chunk" or "delete document" operation? Is it deterministic?
- Backup, snapshot, and replica handling: do they inherit the production ACLs?

If a vendor cannot answer the metadata-filter and audit-log questions, the program should not put regulated data into that vector store without an enforced application-side compensating control.

## Executive Metrics — RAG Additions

Add to `metrics/executive-metrics.md`:

- **% of RAG indexes with documented retrieval pattern (A / B / C)** — target 100%.
- **% of RAG indexes with chunk-level metadata including classification + ACL snapshot** — target 100% for high-risk indexes.
- **Mean time to remove a document from a RAG index** — target ≤ 24 hours for takedown / legal-hold / right-to-erasure events.
- **# of stale-permission retrieval events detected per quarter** — trend down.
- **# of cross-tenant retrieval events detected per quarter** — target zero; any non-zero is a board-level conversation.
- **# of indirect-injection patterns detected in retrieved content per quarter** — trend tracked, with severity weighting based on whether the consuming agent had write capability.
- **% of RAG ingestion identities operating under least-privilege scopes** — target 100%.
- **Coverage of retrieval logging** — % of application paths whose retrievals appear in the SIEM.

## Operating Cadence — RAG-Specific Triggers

In addition to the cadence in `templates/operating-cadence.md`, RAG triggers an out-of-band re-run of D-Control whenever:

- A new source system is added to ingestion.
- An ingestion identity's scope changes.
- A new application path queries an existing index (especially an agent path).
- A vector store version, embedding model, or k value changes.
- A multi-tenant index gains a new tenant or a tenant changes plan.
- A drift job reports above-threshold mismatch between source and index.

## Closing Position

RAG is not safer because the data is "internal." It is more dangerous, because RAG strips the access controls that the organization spent years building, and substitutes a vector index that has none.

The program that handles RAG well will not be the one with the most sophisticated retrieval. It will be the one that can answer, for any chunk in any index: where did this come from, who is allowed to read it today, has it changed, who has retrieved it, and how fast can it be removed.

That is the work. Authorization at retrieval time. Lineage. Quarantine. Drift detection. Containment runbooks that are tested before they are needed.

If your RAG pipeline can leak the answer to a question the user could not have asked the source system, it is not a knowledge platform. It is a side channel.

## References

- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Agentic AI Threats and Mitigations: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- MITRE ATLAS: https://atlas.mitre.org/
- NIST AI Risk Management Framework and Generative AI Profile: https://www.nist.gov/itl/ai-risk-management-framework
- Cloud Security Alliance AI Controls Matrix: https://cloudsecurityalliance.org/artifacts/ai-controls-matrix
- NCSC / CISA / NSA Guidelines for Secure AI System Development: https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development
- Sigma rule format: https://github.com/SigmaHQ/sigma
