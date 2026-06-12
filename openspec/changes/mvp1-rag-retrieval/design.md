# Design: mvp1-rag-retrieval

## Approach
- `retrieve()` requires `tenant_id` (contract-enforced). Backend behind the `rag_backend` interface
  (pgvector implementation now; Vertex AI RAG Engine in MVP 2).
- **Query embedding is EU-local:** the call-time query is embedded with the **same Vertex
  `gemini-embedding-001` (EU), 768-dim** model used at ingestion (shared vector space — see
  `mvp1-knowledge-ingestion`). Hosting in Frankfurt with the Vertex EU endpoint keeps this embedding
  in-region — no transatlantic hop in the hot path.

## Hot-path sequence note
Caller turn → STT text → **embed query (Vertex EU)** → retrieve(tenant_id, query) → context → LLM.
The query-embedding step is part of the retrieval segment's latency budget (not just the vector search)
and is metered/instrumented as such. The retrieval segment must fit the sub-1.5s end-to-end turn budget.
