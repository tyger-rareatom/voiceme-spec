## ADDED Requirements

### Requirement: Graceful degradation on vendor failure
The system SHALL detect a failed STT, retrieval, LLM, TTS, or transport dependency and fail the call
gracefully (clear message + escalation/callback path) rather than hanging or creating dead air.

#### Scenario: TTS provider outage
- GIVEN the TTS provider is unavailable
- WHEN a turn needs synthesis
- THEN the call degrades gracefully (e.g., escalation/offer callback), not a dead-air hang

#### Scenario: Retrieval dependency outage
- GIVEN the retrieval dependency is unavailable
- WHEN a grounded answer requires tenant context
- THEN the system does not invent an answer
- AND it routes to the graceful degradation/escalation path

#### Scenario: Silent retry budget exhausted
- GIVEN a dependency is timing out on the live-call path
- WHEN retries would exceed the turn latency budget
- THEN the system stops retrying silently and follows the graceful degradation path

### Requirement: Circuit-breaker trip parameters
The system SHALL trip a dependency's circuit breaker when the dependency times out on two
sequential calls OR exceeds a per-dependency hot-path latency threshold (default 800ms for TTS),
and while tripped SHALL fail fast to the graceful-degradation path instead of waiting on the
dependency. Thresholds SHALL be configuration, not code constants.

#### Scenario: Slow TTS trips the breaker
- GIVEN the TTS vendor exceeds its 800ms latency threshold on two sequential synthesis calls
- WHEN the next turn needs synthesis
- THEN the breaker is open and the call follows the graceful-degradation path immediately
- AND no synthesis call is attempted while the breaker is open

#### Scenario: Transient-class breaker recovers via half-open probe
- GIVEN a breaker tripped by transient timeouts
- WHEN the cool-down elapses
- THEN a single half-open probe call is allowed
- AND the breaker closes on success or re-opens on failure

#### Scenario: Open breaker bounds caller-perceived silence
- GIVEN an open breaker on any live-call dependency
- WHEN a turn would have used that dependency
- THEN the graceful path (spoken failure message / escalation / callback offer) begins within
  the turn latency budget rather than after stacked vendor timeouts

### Requirement: Transport resilience baseline
The system SHALL document and mitigate the LiveKit single-point-of-failure (health checks,
reconnection, capacity headroom).

#### Scenario: Transient transport drop
- GIVEN a transient LiveKit connection drop
- WHEN the client reconnects within the window
- THEN the session resumes without restarting the conversation
