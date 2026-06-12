# Design: mvp1-knowledge-ingestion

## Approach
- Ingestion worker (async queue). Chunker → embeddings (**Vertex `gemini-embedding-001`, EU endpoint**) →
  pgvector upsert.
- Idempotent re-index keyed by document hash; soft-delete superseded chunks.
- Embedding provider behind an interface (Vertex EU is the MVP-1 implementation; the interface keeps the
  vendor swappable). **Voyage is not in the MVP-1 path** — dropped for EU residency + hot-path latency
  (query embedding at retrieval time would otherwise be a transatlantic hop) and because
  `gemini-embedding-001` tops the MTEB *multilingual* leaderboard (better fit for African/code-switched text).

## Embedding model & dimension (decided)
- Model **`gemini-embedding-001`** via the **Vertex EU endpoint** (GDPR residency posture).
- **768-dim** output via Matryoshka (MRL) trimming. *Why 768:* the model defaults to 3072 dims, which
  exceeds pgvector's **2000-dim hnsw index limit** — 768 is an officially-recommended MRL size, keeps the
  index lean, and is ample at MVP scale. (Alternative for >2000: `halfvec`, pgvector ≥0.7.)
- **Ingestion and retrieval MUST use the same model + dimension** (shared vector space) — see
  `mvp1-rag-retrieval`. The chosen dim is fixed for the whole index.

## Hot-path note
Ingestion is off the live-call path; no latency budget interaction. Status surfaced asynchronously.
