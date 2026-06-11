## MODIFIED Requirements

### Requirement: Audio backend failover
The system SHALL detect failure or sustained degradation of the Gemini backend and fail affected
sessions over to the cascaded backend, recording the event.

#### Scenario: Gemini outage mid-session
- GIVEN an active session on the Gemini backend
- WHEN the backend fails or exceeds degradation thresholds
- THEN the session fails over to the cascaded backend with minimal disruption
- AND the failover event is recorded in telemetry and metering (split usage attribution)

#### Scenario: New sessions during outage
- GIVEN a detected Gemini outage
- WHEN new sessions start for Gemini-flagged tenants
- THEN they are routed directly to cascaded until health recovers
