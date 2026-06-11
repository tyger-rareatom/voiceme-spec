## ADDED Requirements

### Requirement: Swahili pack meets the same bars as Pidgin
The Swahili pack SHALL meet the same style-guide, ASR-quality, voice-approval, and eval requirements
as the Pidgin pack, with Swahili-specific targets.

#### Scenario: Swahili ASR evaluated
- GIVEN the fine-tuned Swahili ASR
- WHEN evaluated on held-out Swahili support calls
- THEN WER meets the agreed Swahili target

### Requirement: Regional routing
The system SHALL route Swahili-language tenants to the NVIDIA backend with the Swahili pack,
respecting regional residency where contracted.

#### Scenario: Kenyan tenant served regionally
- GIVEN a Kenyan tenant with language = Swahili and a regional residency contract
- WHEN sessions run
- THEN the Swahili pack serves them within the contracted region
