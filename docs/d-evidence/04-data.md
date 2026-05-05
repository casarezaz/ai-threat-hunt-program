# Evidence Domain 4 — Data

## Question this domain must answer

> What information was touched?

## Minimum evidence

- Document / object / row identifiers (stable, not URLs)
- Source system and source classification
- For RAG: chunk IDs, source document IDs, ACL snapshot, current ACL state, retrieval-time authorization decision
- Output artifact (where it went, who saw it, how long it persists)
- Egress path (which destination, which channel, which network egress point)

## Most common failure mode

Output without lineage. The model produced an answer; the program cannot say which sources fed it. Citation fabrication compounds the problem. For RAG-driven flows, see [Paper 3 §Document Lineage and Provenance](../papers/paper-3-rag-vector-security.md#document-lineage-and-provenance) for the detailed evidence requirements.

## Findings the program files when this evidence is missing

The pattern is the same regardless of the cause:

- A specific named instrumentation gap.
- An owner.
- A target maturity level (Level 2 to Level 3 is the most common ask).
- A quarter-end date.

Treat each missing-evidence finding the way the program treats a missing control: as a risk that has to be owned and dated, not a backlog item that can drift.

## Reference

See [Paper 4 — D-Evidence §4.4](../papers/paper-4-d-evidence.md#4-the-seven-evidence-domains) for the full operational treatment.
