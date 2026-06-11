## ADDED Requirements

### Requirement: No-code agent configuration
The system SHALL let a tenant set persona (name/voice/tone), greeting, business hours, escalation
rules, and human-fallback behavior via the portal.

#### Scenario: Tenant sets business hours
- GIVEN a tenant admin in the portal
- WHEN they set business hours and an out-of-hours message
- THEN calls outside hours use the configured behavior
