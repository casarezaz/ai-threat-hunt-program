# H-007 — RAG retrieval mismatch

| Field | Value |
|-------|-------|
| Hunt ID | H-007 |
| D-Control step(s) | Detect, Defend |
| Asset class(es) | RAG systems, vector databases |
| OWASP LLM / Agentic AI | LLM06 Excessive Agency, LLM08 Vector and Embedding Weaknesses |
| MITRE ATLAS | AML.T0024 — Exfiltration via Inference |
| Owner | _to assign_ |
| Cadence | Weekly |

## Hypothesis

RAG queries are retrieving documents the requesting user is not authorized to read, or documents outside the expected business context for the use case.

## Why this matters

RAG can become a side-channel around access controls. If embeddings were generated without authorization checks, retrieval becomes the leak.

## Data sources

- Vector DB query logs
- RAG retrieval audit logs (top-k document IDs)
- Document permission system (SharePoint, Drive, Confluence, Box)
- Identity context for the requesting user / agent

## Query / detection logic

```text
for each retrieval_event:
  retrieved_doc_ids = top_k(retrieval_event)
  for doc_id in retrieved_doc_ids:
    if not user_has_permission(retrieval_event.user, doc_id):
      flag(retrieval_event)
```

## Expected normal vs. abnormal

- **Normal:** Retrieved docs are within the user's authorization scope and the use-case's business context.
- **Abnormal:** HR docs returned to an engineering query; legal docs to a marketing user; old or restricted docs that should not have been ingested.

## Evidence to capture

- Query text, embedding source, top-k IDs, scores
- Requesting identity + scope
- Doc lineage (source, ingestion job, classification)

## Findings / Control gaps / Decision

_(filled in per run)_
