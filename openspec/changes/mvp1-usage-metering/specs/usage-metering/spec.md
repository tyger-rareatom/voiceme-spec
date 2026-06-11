## ADDED Requirements

### Requirement: Per-tenant real-time metering
The system SHALL meter, per tenant and per session, voice minutes, STT/TTS seconds, LLM tokens (by
model), and retrieval calls, available in near real time.

#### Scenario: A call is fully metered
- GIVEN a completed call on any backend
- WHEN the session ends
- THEN a metering record captures minutes, STT/TTS seconds, tokens by model, and retrieval count
- AND the tenant's running usage updates within minutes

### Requirement: Cap enforcement
The system SHALL enforce tier minute/conversation caps and flag overage.

#### Scenario: Tenant hits cap
- GIVEN a Starter tenant at its monthly cap
- WHEN another call begins
- THEN the system applies the tenant's overage policy (block or bill-overage) per configuration
