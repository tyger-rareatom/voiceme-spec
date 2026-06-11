## ADDED Requirements

### Requirement: Live-call telemetry
The system SHALL emit latency, error, and quality metrics per call segment (STT/LLM/TTS/retrieval)
tagged by tenant and backend.

#### Scenario: Latency regression is visible
- GIVEN telemetry is collected
- WHEN turn latency exceeds target
- THEN it is visible on dashboards and alertable

### Requirement: Per-tenant operational view
The system SHALL provide per-tenant dashboards (volume, deflection, errors, usage).

#### Scenario: Tenant operations review
- GIVEN an operator reviewing a tenant
- WHEN they open the tenant dashboard
- THEN volume, deflection, error, and usage trends are visible
