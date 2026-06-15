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
