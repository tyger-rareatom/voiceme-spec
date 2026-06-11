## ADDED Requirements

### Requirement: Consent-governed capture
The system SHALL capture audio for training only where consent is recorded, with configurable
retention and PII redaction.

#### Scenario: No consent, no capture
- GIVEN a caller who has not consented
- WHEN the call occurs
- THEN no training-eligible audio is retained

#### Scenario: Consented capture with retention
- GIVEN recorded consent
- WHEN the call occurs
- THEN audio is stored in a governed store with retention + redaction applied and tenant scoping
