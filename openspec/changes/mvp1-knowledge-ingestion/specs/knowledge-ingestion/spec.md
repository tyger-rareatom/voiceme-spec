## ADDED Requirements

### Requirement: Multi-format document ingestion
The system SHALL accept PDF, DOCX, Markdown, and web URLs, chunk them, embed the chunks, and index
them in the tenant's RAG store scoped by `tenant_id`.

#### Scenario: Tenant uploads an FAQ PDF
- GIVEN an authenticated tenant admin
- WHEN they upload an FAQ PDF
- THEN the document is chunked, embedded via the configured embedding provider, and indexed
- AND the chunks are tagged with the tenant_id and source metadata

### Requirement: Continuous re-index on update
The system SHALL re-index changed documents so updates are reflected within one hour.

#### Scenario: FAQ is updated
- GIVEN a previously ingested document
- WHEN the tenant uploads a new version
- THEN stale chunks are replaced and retrieval reflects the new content within one hour
