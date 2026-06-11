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
