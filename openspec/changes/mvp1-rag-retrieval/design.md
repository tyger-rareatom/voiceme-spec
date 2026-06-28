# Design: mvp1-rag-retrieval

## Approach
- `retrieve()` requires `tenant_id` (contract-enforced). Backend behind the `rag_backend` interface
  (pgvector implementation now; **AlloyDB + ScaNN at Scale/sovereign in MVP 2** — same Postgres
  lineage, see `mvp2-rag-vertex`; Vertex AI RAG Engine dropped).
- **Query embedding is EU-local:** the call-time query is embedded with the **same Vertex
  `gemini-embedding-001` (EU), 768-dim** model used at ingestion (shared vector space — see
  `mvp1-knowledge-ingestion`). Hosting in Frankfurt with the Vertex EU endpoint keeps this embedding
  in-region — no transatlantic hop in the hot path.

## Hot-path sequence note
Caller turn → STT text → **embed query (Vertex EU)** → retrieve(tenant_id, query) → context → LLM.
The query-embedding step is part of the retrieval segment's latency budget (not just the vector search)
and is metered/instrumented as such. The retrieval segment must fit the sub-1.5s end-to-end turn budget.

## Per-tenant indexes + warm-at-session-setup

- Use a **per-tenant index** (table/partition per tenant), not one shared index filtered by
  `tenant_id`. Three reasons:
  - **RAM:** only *active* tenants' indexes need to be hot, so the in-RAM working set is the hot set
    (≈ concurrent calls), not all vectors ever — pushes the pgvector scale ceiling out ~10–20×.
  - **Correctness:** each query is single-tenant by construction, so there is no HNSW filtered-search
    recall/latency degradation.
  - **Re-index cost:** a tenant's doc update rebuilds only their small index — cheap, fast, and
    exactly what the "reflect updates within the hour" requirement wants.
- **Warm the tenant's index at session setup.** A cold (evicted) index pays an SSD read on the first
  retrieve (~tens of ms to ~0.4s depending on size). We already resolve backend/RAG/config at session
  setup (not per turn) — prefetch/pin the tenant's index there, during connect + greeting, so the
  warm-up hides behind "Hi, how can I help?" rather than the caller's first real question.

## Portability invariants (keep future migration cheap — beat data gravity)

> pgvector is chosen partly *because* it is the same Postgres family as the Scale-tier target
> (AlloyDB), so a growing tenant's upgrade is lift-and-shift, not re-architecture. Preserve all three:

- **Stable embedding model + dimension (768-dim).** Vectors copy between engines unchanged — never
  re-embed on migration.
- **Documents are the source of truth.** Any index can be rebuilt from source — the ultimate
  migration fallback and a correctness guard.
- **No pgvector-specific SQL in business logic.** The backend swap stays an impl detail behind
  `rag_backend`, not an application change.

## Scale trigger (when a tenant leaves pgvector)

- Watch **RAM headroom = hot_index_size ÷ instance_RAM** as an SLO (green <50% · amber 50–80% ·
  red >80%). Route an individual tenant to the ScaNN backend (AlloyDB) only when they personally
  approach the limit — realistically a rare mega-tenant on dedicated Scale/sovereign compute. Never a
  fleet-wide migration. See `mvp2-rag-vertex` (Scale backend) for the lineage + migration pattern.
