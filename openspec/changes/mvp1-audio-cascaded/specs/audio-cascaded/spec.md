## ADDED Requirements

### Requirement: Real-time cascaded voice turn
The system SHALL transcribe caller speech, retrieve context, generate a grounded response, and
synthesize speech within a target end-to-end turn latency of 1.5s (p50).

#### Scenario: Caller asks a grounded question
- GIVEN a configured tenant agent
- WHEN a caller asks a question covered by tenant docs
- THEN the agent responds with a grounded spoken answer within the latency target

### Requirement: Cost-routed inference
The system SHALL route trivial turns to a cheaper model (Haiku) and substantive turns to the anchor
model (Sonnet). For MVP 1, production routing SHALL remain Claude Haiku/Sonnet only unless
`mvp1-llm-routing-spike` records an explicit production-routing verdict for another model.

#### Scenario: Trivial turn routed cheaply
- GIVEN a greeting or acknowledgement turn
- WHEN the router classifies it as trivial
- THEN the cheaper model handles it and the choice is recorded in metering

#### Scenario: Candidate model blocked before verdict
- GIVEN a candidate model under evaluation
- WHEN no recorded production-routing verdict exists
- THEN the live-call router does not send production turns to that model

### Requirement: Barge-in / turn-taking
The system SHALL support caller interruption (barge-in) and voice-activity-based turn-taking.

#### Scenario: Caller interrupts the agent
- GIVEN the agent is speaking
- WHEN the caller starts speaking
- THEN the agent stops and listens
