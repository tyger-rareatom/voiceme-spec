# Tasks: mvp2-rag-vertex

## 1. Backend
- [ ] 1.1 Region availability check for Vertex AI RAG Engine (HARD GATE — do first)
- [ ] 1.2 Vertex rag_backend implementation (tenant-scoped)
- [ ] 1.3 Ingestion pipeline Vertex indexing target

## 2. Migration
- [ ] 2.1 Idempotent migration job (re-index from source docs)
- [ ] 2.2 Parity evaluation harness (pgvector ↔ Vertex, agreed tolerance)
- [ ] 2.3 Cutover + source-retention policy

## 3. Guards
- [ ] 3.1 Scale-only assignment guard (cost amortization rule)
- [ ] 3.2 Retrieval latency benchmark within turn budget
