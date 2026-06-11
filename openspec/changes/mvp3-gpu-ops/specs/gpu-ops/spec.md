## ADDED Requirements

### Requirement: Concurrency-aware autoscaling
The system SHALL autoscale GPU capacity based on concurrent call load, maintaining latency SLOs
within agreed scale-up time.

#### Scenario: Load approaches capacity
- GIVEN concurrent NVIDIA-backend calls nearing provisioned capacity
- WHEN the autoscale threshold is crossed
- THEN capacity scales up within the SLO window and no in-flight call degrades beyond SLO

### Requirement: Model lifecycle management
The system SHALL version deployed models (ASR/TTS/LLM) and support rollback without platform changes.

#### Scenario: Bad model rollback
- GIVEN a newly deployed model version causing quality regression
- WHEN rollback is triggered
- THEN the prior version serves traffic and the event is recorded

### Requirement: GPU cost telemetry
The system SHALL attribute GPU cost per tenant and per session into the metering plane and margin
dashboard.

#### Scenario: GPU cost visible per tenant
- GIVEN NVIDIA-backend traffic
- WHEN the margin dashboard is viewed
- THEN per-tenant GPU cost attribution is visible alongside vendor costs

### Requirement: Inflection routing input
The system SHALL compute per-tenant volume against the self-host inflection threshold and expose it
to the router.

#### Scenario: Tenant crosses the inflection
- GIVEN a tenant whose sustained volume crosses the threshold
- WHEN routing eligibility is recomputed
- THEN the tenant becomes eligible for self-host routing (subject to language/tier rules)
