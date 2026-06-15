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

### Requirement: Transport resilience baseline
The system SHALL document and mitigate the LiveKit single-point-of-failure (health checks,
reconnection, capacity headroom).

#### Scenario: Transient transport drop
- GIVEN a transient LiveKit connection drop
- WHEN the client reconnects within the window
- THEN the session resumes without restarting the conversation
