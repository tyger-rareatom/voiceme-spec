# Design: mvp1-agent-configuration

## Approach
- Agent config persisted per tenant; consumed by the audio runtime at session setup (not mid-call).
- Persona/voice selection constrained to voices available on the tenant's configured audio backend.
