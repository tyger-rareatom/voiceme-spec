## MODIFIED Requirements

### Requirement: Vertex backend behind rag_backend
The system SHALL serve retrieval for tenants flagged `rag_backend=vertex` from Vertex AI RAG Engine,
tenant-scoped, meeting the same retrieval contract as pgvector.

#### Scenario: Vertex retrieval is tenant-scoped
- GIVEN a Scale tenant on the Vertex backend
- WHEN retrieve(tenant_id, query) is called
- THEN only that tenant's chunks are returned from Vertex
- AND retrieval latency fits the live-call turn budget
