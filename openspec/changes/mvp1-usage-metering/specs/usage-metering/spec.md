## ADDED Requirements

### Requirement: Per-tenant real-time metering
The system SHALL meter, per tenant and per session, voice minutes, STT/TTS seconds, LLM tokens (by
model), and retrieval calls, available in near real time.

#### Scenario: A call is fully metered
- GIVEN a completed call on any backend
- WHEN the session ends
- THEN a metering record captures minutes, STT/TTS seconds, tokens by model, and retrieval count
- AND the tenant's running usage updates within minutes

### Requirement: Non-blocking, lossless usage emission
The system SHALL emit usage events from the live-call turn loop without any synchronous
durability write: events go to a non-blocking in-process buffer backed by a locally durable
spool, delivered to the collector at-least-once. A collector or sink outage SHALL NOT add
latency to any turn and SHALL NOT lose usage events.

#### Scenario: Collector outage adds no turn latency
- GIVEN the metering collector is unreachable
- WHEN calls proceed
- THEN per-turn latency is unaffected
- AND usage events accumulate in the local durable spool

#### Scenario: No event loss across an outage
- GIVEN usage events spooled during a collector outage
- WHEN the collector recovers
- THEN all spooled events are delivered and reconcile with the calls that occurred
- AND duplicates are tolerated downstream (at-least-once, idempotent ingestion)

#### Scenario: Spool pressure triggers admission policy, never turn degradation
- GIVEN the local spool exceeds its configured threshold
- WHEN new sessions are requested
- THEN the configured admission policy applies (MVP-1 default: alert-only; block-new-sessions
  available behind a flag)
- AND in-flight calls and their turn latency are never affected

### Requirement: Cap enforcement
The system SHALL enforce tier minute/conversation caps and flag overage.

#### Scenario: Tenant hits cap
- GIVEN a Starter tenant at its monthly cap
- WHEN another call begins
- THEN the system applies the tenant's overage policy (block or bill-overage) per configuration

### Requirement: Billing reconciliation and margin visibility
The system SHALL reconcile collected usage against vendor invoices and expose per-tenant margin
visibility so billing integrity and unit economics can be audited.

#### Scenario: Vendor invoice reconciliation
- GIVEN vendor invoices for STT, TTS, LLM, and embedding/retrieval usage
- WHEN reconciliation runs for a billing period
- THEN metered tenant usage is compared with vendor-reported usage
- AND mismatches above the configured tolerance are flagged for investigation

#### Scenario: Tenant margin review
- GIVEN a tenant with subscription revenue and metered vendor consumption
- WHEN an operator opens the margin dashboard
- THEN revenue, vendor cost, overage, and gross margin are visible for that tenant
