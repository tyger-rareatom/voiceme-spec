## ADDED Requirements

### Requirement: Tenant-scoped retrieval
The system SHALL expose `retrieve(tenant_id, query)` returning top-k chunks for that tenant only.

#### Scenario: Retrieval never crosses tenants
- GIVEN tenants A and B with distinct documents
- WHEN retrieve(A, query) is called
- THEN only tenant A chunks are returned, regardless of query content

### Requirement: Grounded-answer bounding
The system SHALL pass only retrieved tenant context to the LLM for answer generation.

#### Scenario: No matching content
- GIVEN a query with no relevant tenant chunks
- WHEN the agent responds
- THEN it states it does not have that information rather than inventing an answer
