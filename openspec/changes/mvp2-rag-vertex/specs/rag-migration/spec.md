## ADDED Requirements

### Requirement: Tier-upgrade content migration
The system SHALL migrate a tenant's indexed content from pgvector to Vertex AI RAG Engine on
Growth→Scale upgrade without answer-quality regression.

#### Scenario: Growth tenant upgrades to Scale
- GIVEN a Growth tenant with indexed content in pgvector
- WHEN their upgrade to Scale completes
- THEN content is re-indexed into Vertex AI RAG Engine
- AND a parity evaluation confirms retrieval quality within the agreed tolerance
- AND retrieval cuts over with zero data loss

#### Scenario: Migration failure is safe
- GIVEN a migration job that fails mid-run
- WHEN the failure occurs
- THEN retrieval continues uninterrupted on pgvector and the job can be re-run idempotently
