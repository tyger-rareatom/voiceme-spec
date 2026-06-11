# Design: mvp1-rag-retrieval

## Approach
- `retrieve()` requires `tenant_id` (contract-enforced). Backend behind the `rag_backend` interface
  (pgvector implementation now; Vertex in MVP 2).

## Hot-path sequence note
Caller turn → STT text → retrieve(tenant_id, query) → context → LLM. Retrieval latency is metered as
its own segment and must fit the sub-1.5s end-to-end turn budget.
