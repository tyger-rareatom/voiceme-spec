# Tasks: mvp1-rag-retrieval

## 1. Interface & implementation
- [ ] 1.1 retrieve(tenant_id, query) interface + pgvector impl
- [ ] 1.2 top-k tuning + metadata return

## 2. Quality & latency
- [ ] 2.1 Latency instrumentation (retrieval portion of turn budget — **include the query-embedding step**,
      not just vector search)
- [ ] 2.2 No-match → graceful "I don't have that" path
- [ ] 2.3 Isolation test: cross-tenant retrieval impossibility
