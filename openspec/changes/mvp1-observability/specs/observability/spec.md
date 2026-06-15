## ADDED Requirements

### Requirement: Live-call telemetry
The system SHALL emit latency, error, and quality metrics per call segment (media leg, STT, query
embedding, retrieval, LLM, TTS) tagged by tenant, backend, and model where applicable.

#### Scenario: Latency regression is visible
- GIVEN telemetry is collected
- WHEN turn latency exceeds target
- THEN the breached segment is visible on dashboards and alertable
- AND the full turn can be correlated to usage and model-choice telemetry

#### Scenario: Segment budget review
- GIVEN a completed call turn
- WHEN an operator reviews latency telemetry
- THEN media leg, STT, query embedding, retrieval, LLM, TTS, and end-to-first-audio timings are visible
- AND each timing can be grouped by tenant and backend

### Requirement: Per-tenant operational view
The system SHALL provide per-tenant dashboards (volume, deflection, errors, usage).

#### Scenario: Tenant operations review
- GIVEN an operator reviewing a tenant
- WHEN they open the tenant dashboard
- THEN volume, deflection, error, and usage trends are visible
