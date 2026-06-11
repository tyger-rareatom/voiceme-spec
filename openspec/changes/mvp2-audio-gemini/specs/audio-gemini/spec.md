## ADDED Requirements

### Requirement: Gemini backend conforms to the audio interface
The system SHALL serve sessions for tenants flagged `audio_backend=gemini` via Gemini Live native
audio, passing the backend conformance suite and emitting usage to the metering plane.

#### Scenario: Gemini session served and metered
- GIVEN a tenant with audio_backend = "gemini"
- WHEN a call session starts and completes
- THEN Gemini Live serves all turns of the session
- AND a usage record is emitted with tenant_id, backend="gemini", and consumption metrics

### Requirement: Covered-language guard
The system SHALL prevent selecting the Gemini backend for a tenant whose configured language is not
natively covered by Gemini Live.

#### Scenario: Unsupported language blocked
- GIVEN a tenant whose language is Nigerian Pidgin
- WHEN an admin attempts to set audio_backend = "gemini"
- THEN the system rejects the configuration with a clear explanation
- AND suggests the cascaded or NVIDIA backend instead

### Requirement: Closed-model constraint surfaced
The system SHALL surface that custom voices and language fine-tuning are unavailable on the Gemini
backend wherever voice/persona selection is offered.

#### Scenario: Voice selection on Gemini
- GIVEN a tenant on the Gemini backend
- WHEN they open persona/voice configuration
- THEN only Gemini's fixed voice set is offered, with the constraint explained
