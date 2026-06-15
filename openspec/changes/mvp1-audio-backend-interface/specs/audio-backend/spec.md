## ADDED Requirements

### Requirement: Stable audio-backend contract
The system SHALL define an audio-runtime interface (start session, stream audio in, stream audio
out, end session, report usage) that any backend implements without changes to the shared platform.

#### Scenario: Backend resolved at session setup
- GIVEN a tenant with audio_backend = "cascaded"
- WHEN a call session starts
- THEN the router resolves the backend once at setup (not per turn)
- AND all turns in the session use that backend

### Requirement: Usage reporting from every backend
The system SHALL require each backend to emit per-session usage (audio seconds, tokens where
applicable) to the metering plane.

#### Scenario: Usage emitted regardless of backend
- GIVEN any registered audio backend
- WHEN a session ends
- THEN a usage record is emitted with tenant_id, backend, and consumption metrics

### Requirement: Backend conformance gate
The system SHALL prevent any audio backend from registering unless it passes the conformance suite
for lifecycle behavior, usage emission, and graceful error behavior.

#### Scenario: Backend missing usage callback
- GIVEN an audio backend implementation without a working usage callback
- WHEN backend registration or conformance runs
- THEN the backend fails conformance
- AND it cannot be selected by the session router
