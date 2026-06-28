# Design: mvp2-rag-vertex

## Approach
- Vertex implementation of the `rag_backend` interface; ingestion pipeline gains a Vertex indexing
  target (embedding provider per backend).
- Migration job: re-index from source documents (not from pgvector vectors) for fidelity; idempotent;
  source index retained until parity eval passes; then cutover via the config flag.
- **Region check is a hard prerequisite task:** confirm Vertex AI RAG Engine availability in the
  target region (`africa-south1` note in project.md); if unavailable, escalate — the sovereign+Vertex
  pairing has a hole and the design must be revisited.
- Cost guard: Vertex node-hours only assigned to Scale tenants (fixed-cost amortization rule).

## Revised direction — AlloyDB Postgres lineage (supersedes the Vertex approach above)

> Decision from exploration: the Scale/sovereign RAG backend should be **AlloyDB AI (ScaNN)**, not
> Vertex AI RAG Engine. This change is flagged for **re-scope/rename** (`mvp2-rag-vertex` →
> `mvp2-rag-alloydb` / `rag-scale-backend`); the spec deltas (`rag-backend`, `rag-migration`) and the
> proposal still name Vertex and must be updated on formal re-scope.

- **One engine family across all tiers** — pgvector (Standard) → AlloyDB + ScaNN (Growth/Scale) →
  AlloyDB Omni (Sovereign). All Postgres, so every tier upgrade is lift-and-shift (vectors copy
  as-is; build a ScaNN index), never a re-architecture.
- **Why AlloyDB over Vertex:**
  - *Migration:* pgvector→AlloyDB is same-family (copy + reindex); pgvector→Vertex is a paradigm jump
    (re-embed + re-integrate). The lineage removes the hard migration entirely.
  - *Workload fit:* tenant-scoped (filtered) retrieval is ScaNN's strength; AlloyDB keeps tenant
    metadata + vectors co-located in SQL.
  - *Sovereign:* **AlloyDB Omni runs in-region** (on Cassava/Kasi), filling the `africa-south1` hole
    that Vertex RAG Engine availability could not guarantee.
  - *Maintenance:* one engine family / one ops + mental model — one fewer backend than pgvector + Vertex.
- **Rejected — Vertex at Standard / AlloyDB above:** places the one paradigm-jump migration at the
  Standard→Growth boundary every growing tenant crosses, and pays Vertex's fixed node-hour floor on
  the lowest-volume tenants. Maximizes the migration/cost/maintenance it was meant to cut.
- **Considered — AlloyDB at every tier (incl. Standard):** one backend, zero migrations ever (just
  resize). Rejected for now — gives up pgvector's marginal-zero cost at the free entry tier, and the
  pgvector→AlloyDB hop is cheap enough (same family) that keeping pgvector at the bottom wins on cost
  without adding migration pain.
- **Migration pattern (unchanged, non-destructive):** build the AlloyDB/ScaNN index in parallel →
  retrieval-parity eval vs pgvector → flip the per-tenant `rag_backend` flag at next session → keep
  pgvector until parity holds (instant rollback). Per-tenant, triggered by the RAM-headroom SLO in
  `mvp1-rag-retrieval` — never fleet-wide.
