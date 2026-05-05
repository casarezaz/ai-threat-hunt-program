# RAG-specific hunts

Hunts that target the retrieval-augmented generation pipeline. Each one corresponds to a section in [Paper 3](../../docs/papers/paper-3-rag-vector-security.md). Naming uses the `RAG-NNN` prefix; `H-NNN` (under `starter/`) remains the cross-cutting starter set.

| ID | Title | D-Control | OWASP |
|----|-------|-----------|-------|
| [RAG-001](RAG-001.md) | Embedding ingestion of unauthorized documents | Discover, Define | LLM02, LLM08 |
| [RAG-002](RAG-002.md) | Retrieval-time authorization bypass | Detect, Deny | LLM02, LLM06, LLM08 |
| [RAG-003](RAG-003.md) | Indirect prompt injection in retrieved content | Detect, Defend | LLM01, LLM05, LLM08 |
| [RAG-004](RAG-004.md) | Index poisoning (post-ingest tampering) | Detect, Degrade | LLM03, LLM08 |
| [RAG-005](RAG-005.md) | Cross-tenant retrieval leakage | Detect, Deny | LLM02, LLM08 |
| [RAG-006](RAG-006.md) | Stale-permission retrieval | Detect, Defend | LLM02, LLM08 |
