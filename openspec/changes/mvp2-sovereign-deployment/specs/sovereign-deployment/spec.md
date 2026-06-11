## ADDED Requirements

### Requirement: Data residency
The system SHALL process and store a sovereign tenant's data exclusively within the contracted region.

#### Scenario: Sovereign tenant data stays in-region
- GIVEN a sovereign tenant contracted to a region
- WHEN audio, transcripts, documents, or vectors are processed or stored
- THEN all processing and storage occurs within that region
- AND any out-of-region dependency is either eliminated or explicitly contracted

### Requirement: BYOK encryption
The system SHALL encrypt a sovereign tenant's data at rest using the tenant's own key.

#### Scenario: Tenant key used
- GIVEN a sovereign tenant with a provided key
- WHEN their data is written at rest
- THEN encryption uses the tenant's key
- AND key revocation renders the data inaccessible

### Requirement: Immutable audit logging
The system SHALL record an immutable audit trail of administrative and data-access actions for
sovereign tenants.

#### Scenario: Admin action audited
- GIVEN a sovereign tenant
- WHEN any administrative or data-access action occurs
- THEN an append-only audit record captures actor, action, target, and timestamp
