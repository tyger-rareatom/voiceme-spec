# Design: mvp1-knowledge-ingestion

## Approach
- Ingestion worker (async queue). Chunker → embeddings (Voyage for Standard tier) → pgvector upsert.
- Idempotent re-index keyed by document hash; soft-delete superseded chunks.
- Embedding provider behind an interface (Voyage now; Vertex path arrives in MVP 2).

## Hot-path note
Ingestion is off the live-call path; no latency budget interaction. Status surfaced asynchronously.
