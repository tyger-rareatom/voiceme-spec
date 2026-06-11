## ADDED Requirements

### Requirement: NVIDIA backend conforms to the audio interface
The system SHALL serve sessions for tenants flagged `audio_backend=nvidia` via self-hosted Riva
(Parakeet/Canary ASR, Magpie TTS), passing the conformance suite and emitting usage to metering.

#### Scenario: NVIDIA session served and metered
- GIVEN a tenant with audio_backend = "nvidia"
- WHEN a call session starts and completes
- THEN Riva ASR/TTS serve the session via NIM
- AND a usage record is emitted including GPU-time attribution

### Requirement: Swappable LLM slot
The system SHALL allow the NVIDIA backend's reasoning layer to be configured per tenant as Claude
(default) or self-hosted Nemotron (only where the Nemotron spike gate has passed).

#### Scenario: Sovereign tenant on Nemotron
- GIVEN the Nemotron spike gate recorded as PASSED and a sovereign tenant requiring in-VPC inference
- WHEN their llm_slot is set to "nemotron"
- THEN reasoning runs on self-hosted Nemotron within the VPC

#### Scenario: Nemotron blocked without gate
- GIVEN the spike gate not recorded as PASSED
- WHEN an admin attempts llm_slot = "nemotron"
- THEN the configuration is rejected citing the gate

### Requirement: Volume-gated routing
The system SHALL NOT select the NVIDIA self-host backend for tenants below the self-host volume
inflection (fixed GPU cost rule).

#### Scenario: Starter tenant cannot route to self-host
- GIVEN a Starter tenant below the inflection volume
- WHEN backend selection runs
- THEN the NVIDIA backend is not selectable for that tenant (unless language-pack necessity
  explicitly overrides, recorded with cost acknowledgment)
