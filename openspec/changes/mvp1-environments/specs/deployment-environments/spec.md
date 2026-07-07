## ADDED Requirements

### Requirement: Environment parity by construction
The system SHALL build staging and production from the same Terraform modules in the same region
(`europe-west3`), differing only by declared per-environment variables (instance counts, quotas,
alert routing). Environments SHALL scale down by replica count, never by omitting components.

#### Scenario: Staging deploys the full topology
- GIVEN the staging environment is provisioned from Terraform
- WHEN provisioning completes
- THEN every production component (control plane, voice runtime, metering collector, RAG store, observability pipeline) exists in staging

#### Scenario: Missing component fails the parity check
- GIVEN a change that removes a component from staging but not production
- WHEN the environment parity check runs in CI
- THEN the check fails and the change is blocked

### Requirement: Per-environment isolation
The system SHALL run staging and production in separate GCP projects with separate vendor API
keys and separate secret stores. No credential SHALL be valid in more than one environment.
Stripe SHALL use test mode in staging; all other vendors use real EU endpoints with
staging-scoped keys.

#### Scenario: Staging credentials cannot reach production
- GIVEN any credential issued to the staging environment
- WHEN it is used against a production resource (GCP API, database, vendor account)
- THEN access is denied and the attempt is logged

#### Scenario: Staging exercises real vendor endpoints
- GIVEN a synthetic call in staging
- WHEN the cascaded pipeline runs
- THEN Deepgram/Cartesia/Vertex EU endpoints are called with staging keys (not mocks)
- AND Stripe interactions use test mode

### Requirement: Gated promotion to production
The system SHALL block promotion of a build to production unless, on that build in staging:
the cross-tenant isolation suite passes, the synthetic-call probe meets the turn-latency SLO,
and a metering smoke test confirms a completed call produced a usage record.

#### Scenario: Isolation regression blocks promotion
- GIVEN a build that fails the cross-tenant isolation suite in staging
- WHEN promotion to production is attempted
- THEN the pipeline blocks it and reports the failing gate

#### Scenario: Un-metered call blocks promotion
- GIVEN a build where a completed staging call produces no usage record
- WHEN promotion to production is attempted
- THEN the pipeline blocks it

#### Scenario: Break-glass is explicit and audited
- GIVEN a production emergency requiring a gate bypass
- WHEN an authorized operator invokes the documented break-glass path
- THEN the bypass is recorded (who, when, which gates) and an alert is raised

### Requirement: Staging data governance
The system SHALL prevent production tenant data (documents, audio, transcripts, PII) from
entering staging. Staging SHALL carry permanent synthetic seed tenants (AcmePay, TelcoOne) that
double as fixtures for the isolation suite.

#### Scenario: Production data import is rejected
- GIVEN an attempt to restore or copy a production datastore into staging
- WHEN the operation runs
- THEN it is refused by policy/tooling and the attempt is logged

#### Scenario: Seed tenants are always present
- GIVEN a freshly provisioned or reset staging environment
- WHEN seeding completes
- THEN AcmePay and TelcoOne exist with distinct documents, configs, and API credentials suitable for cross-tenant isolation testing

### Requirement: Synthetic call probe
The system SHALL provide a scripted caller that places real WebRTC calls against staging, plays
canned audio, and measures per-segment latency (STT/LLM/TTS/retrieval) against the 1.5s p50 turn
budget — running on every deploy and on a schedule.

#### Scenario: Latency regression is caught pre-production
- GIVEN a build that pushes p50 turn latency over budget
- WHEN the synthetic probe runs against staging
- THEN the regression is reported per segment and the promotion gate fails

#### Scenario: Scheduled probe feeds observability
- GIVEN the scheduled probe run
- WHEN it completes
- THEN per-segment latency metrics are emitted to the observability pipeline tagged as synthetic
- AND synthetic traffic is excluded from tenant billing/metering aggregates

### Requirement: Production durability baseline
The system SHALL configure production Postgres with point-in-time recovery meeting a stated
RPO/RTO, per-project budget alerts, and a pinned widget CDN version (staging tracks latest;
production pins with explicit promotion).

#### Scenario: Widget rollback via version pin
- GIVEN a bad widget bundle promoted to production
- WHEN the pinned version is reverted
- THEN tenant sites serve the prior bundle without tenant-side changes
