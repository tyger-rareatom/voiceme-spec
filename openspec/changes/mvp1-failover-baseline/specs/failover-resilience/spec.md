## ADDED Requirements

### Requirement: Graceful degradation on vendor failure
The system SHALL detect a failed STT/LLM/TTS dependency and fail the call gracefully (clear message
+ escalation) rather than hanging.

#### Scenario: TTS provider outage
- GIVEN the TTS provider is unavailable
- WHEN a turn needs synthesis
- THEN the call degrades gracefully (e.g., escalation/offer callback), not a dead-air hang

### Requirement: Transport resilience baseline
The system SHALL document and mitigate the LiveKit single-point-of-failure (health checks,
reconnection, capacity headroom).

#### Scenario: Transient transport drop
- GIVEN a transient LiveKit connection drop
- WHEN the client reconnects within the window
- THEN the session resumes without restarting the conversation
