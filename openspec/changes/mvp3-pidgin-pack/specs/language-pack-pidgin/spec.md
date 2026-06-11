## ADDED Requirements

### Requirement: Transcription style guide locked before labelling
The system SHALL adopt a locked Nigerian Pidgin transcription style guide before any labelling
begins, governing all training transcripts.

#### Scenario: Labelling uses the style guide
- GIVEN the locked style guide
- WHEN any audio is transcribed for training
- THEN transcripts conform to the guide (spot-check sampling enforced)

### Requirement: ASR quality bar
The fine-tuned ASR SHALL meet the agreed WER target on a held-out set of real Pidgin support calls,
improving materially over the baseline.

#### Scenario: Fine-tune evaluated on held-out calls
- GIVEN the fine-tuned Parakeet/Canary model
- WHEN evaluated on the held-out support-call set
- THEN WER meets the agreed target and beats baseline by the agreed margin
- AND failure to meet the bar blocks rollout (iterate on data, not ship)

### Requirement: Branded Pidgin voice
The agent SHALL speak with an approved Nigerian Pidgin voice produced via Magpie voice cloning,
licensed for commercial use.

#### Scenario: Voice approved and licensed
- GIVEN candidate cloned voices
- WHEN a voice is selected
- THEN native-speaker review approves naturalness and the talent license covers commercial use

### Requirement: Pidgin tenants routed to the pack
The system SHALL route Pidgin-language tenants to the NVIDIA backend with the Pidgin pack once GA.

#### Scenario: Pidgin tenant after pack GA
- GIVEN a tenant with language = Nigerian Pidgin after pack GA
- WHEN backend selection runs
- THEN the NVIDIA backend with the Pidgin pack serves them (v1 fallback retained)
