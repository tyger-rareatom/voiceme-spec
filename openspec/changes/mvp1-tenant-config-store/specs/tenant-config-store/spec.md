## ADDED Requirements

### Requirement: Authoritative tenant config
The system SHALL store per-tenant flags and entitlements and expose them to the router at session setup.

#### Scenario: Router reads config at setup
- GIVEN a tenant config with audio_backend and rag_backend set
- WHEN a session starts
- THEN the router reads the flags once and selects backends accordingly

#### Scenario: Config change applies on next session
- GIVEN a config change made mid-call
- WHEN the current session continues
- THEN the change takes effect on the next session, not mid-call
