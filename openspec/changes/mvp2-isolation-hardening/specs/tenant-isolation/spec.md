## MODIFIED Requirements

### Requirement: Dedicated isolation tier
The system SHALL provision sovereign tenants on dedicated VPC and compute with no shared data plane.

#### Scenario: Sovereign tenant provisioned dedicated
- GIVEN a tenant contracted for dedicated isolation
- WHEN provisioning completes
- THEN their voice runtime, RAG store, and storage run on dedicated resources
- AND no shared data-plane component carries their traffic

### Requirement: Noisy-neighbour controls on shared infrastructure
The system SHALL enforce per-tenant resource quotas and fairness on shared infrastructure so one
tenant's load cannot degrade another's latency SLO.

#### Scenario: Tenant traffic spike contained
- GIVEN tenant A spiking to its quota on shared infrastructure
- WHEN tenant B makes calls concurrently
- THEN tenant B's latency remains within SLO

### Requirement: Isolation proven by test, continuously
The system SHALL run the cross-tenant isolation suite as a release gate on every deploy.

#### Scenario: Isolation regression blocks release
- GIVEN a change that breaks tenant scoping anywhere in the stack
- WHEN the release pipeline runs
- THEN the isolation suite fails and the release is blocked
