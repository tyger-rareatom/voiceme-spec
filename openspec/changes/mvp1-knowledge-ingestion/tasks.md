# Tasks: mvp1-knowledge-ingestion

## 1. Intake
- [ ] 1.1 Upload endpoint + storage (PDF/DOCX/MD/URL fetchers)
- [ ] 1.2 Chunker with source metadata

## 2. Index
- [ ] 2.1 Embedding provider interface + Vertex `gemini-embedding-001` (EU) implementation, 768-dim MRL
- [ ] 2.2 pgvector upsert + tenant scoping (768-dim vectors; confirm hnsw index config)
- [ ] 2.3 Re-index on update (hash-keyed, idempotent)
- [ ] 2.4 Spike: confirm Vertex single-region `europe-west3` embedding availability (EU multi-region
      endpoint is the default; single-region only needed if a tenant demands named-region)

## 3. Surface
- [ ] 3.1 Ingestion status surfaced in portal
